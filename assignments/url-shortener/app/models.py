# models.py
import time
from threading import Lock

class URLStore:
    def __init__(self):
        # Maps short_code -> data {url, created_at, clicks}
        self.url_map = {}
        self.lock = Lock()

    def add_url(self, short_code, full_url):
        with self.lock:
            if short_code not in self.url_map:
                self.url_map[short_code] = {
                    "url": full_url,
                    "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "clicks": 0
                }

    def get_url(self, short_code):
        with self.lock:
            return self.url_map.get(short_code)

    def increment_clicks(self, short_code):
        with self.lock:
            if short_code in self.url_map:
                self.url_map[short_code]["clicks"] += 1

    def get_stats(self, short_code):
        with self.lock:
            return self.url_map.get(short_code)

# Shared store instance for global use
store = URLStore()
