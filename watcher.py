# watcher.py
import os
import time
import hashlib
import logging
from queue import Queue, Empty
from threading import Event

import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from bod_parser import parse_bod_file
from render import render_overlay
from config import (
    BOD_PATH,
    OUTPUT_PNG,
    TEMP_OUTPUT,
    DEBOUNCE_SECONDS,
    READ_RETRY,
    READ_RETRY_DELAY,
)

log = logging.getLogger(__name__)


class BodEventHandler(FileSystemEventHandler):
    def __init__(self, queue: Queue, normalized_bod_path: str):
        super().__init__()
        self.queue = queue
        self.normalized_bod_path = normalized_bod_path  # already abspath+lower()

    def on_modified(self, event):
        if event.is_directory:
            return
        try:
            if os.path.abspath(event.src_path).lower() == self.normalized_bod_path:
                self.queue.put(time.time())
        except Exception:
            pass


def _safe_read_and_parse(retries=READ_RETRY):
    for attempt in range(1, retries + 1):
        try:
            return parse_bod_file(BOD_PATH)
        except Exception as e:
            log.debug("Parse attempt %d failed: %s", attempt, e)
            time.sleep(READ_RETRY_DELAY)
    raise RuntimeError("Failed to read/parse .bod after retries")


def watch_loop(stop_event: Event | None = None):
    q = Queue()
    observer = Observer()
    normalized_bod_path = os.path.abspath(BOD_PATH).lower()
    handler = BodEventHandler(q, normalized_bod_path)

    watch_dir = os.path.dirname(BOD_PATH) or "."
    observer.schedule(handler, watch_dir, recursive=False)
    observer.start()
    log.info("Watching %s for changes...", BOD_PATH)

    checksum = None
    try:
        while not (stop_event and stop_event.is_set()):
            try:
                _ = q.get(timeout=1.0)

                # debounce burst
                last = time.time()
                while True:
                    try:
                        _ = q.get(timeout=DEBOUNCE_SECONDS)
                        last = time.time()
                    except Empty:
                        break

                try:
                    parsed = _safe_read_and_parse()
                except Exception as e:
                    log.error("Parsing failed after retries: %s", e)
                    continue

                # change detection on arrays
                h = hashlib.sha256()
                h.update(np.array(parsed["cell_type_array"], dtype=np.uint32).tobytes())
                h.update(np.array(parsed["cell_color_array"], dtype=np.uint32).tobytes())
                new_checksum = h.hexdigest()
                if new_checksum == checksum:
                    log.debug("No changes -> skip render")
                    continue
                checksum = new_checksum

                render_overlay(parsed, OUTPUT_PNG, TEMP_OUTPUT)

            except Empty:
                continue
    finally:
        observer.stop()
        observer.join()
