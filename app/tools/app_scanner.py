import os
import json
import shutil
from collections import OrderedDict


class AppScanner:

    def __init__(self, input_file="app/data/apps.json"):
        self.input_file = input_file
        self.cleaned_data = {}


    # =========================
    # LOAD RAW FILE
    # =========================
    def load(self):

        try:
            with open(self.input_file, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            print("Failed to load apps.json:", e)
            return {}


    # =========================
    # VALIDATION CHECK
    # =========================
    def is_valid_exe(self, path: str):

        if not isinstance(path, str):
            return False

        path = path.strip()

        # must be exe or valid command
        if path.endswith(".exe") or shutil.which(path):
            return True

        return False


    # =========================
    # CLEAN KEY
    # =========================
    def normalize_key(self, key: str):

        key = key.lower().strip()
        key = key.replace("_", " ")
        key = key.replace("-", " ")

        return key


    # =========================
    # SCAN + CLEAN
    # =========================
    def scan(self):

        raw = self.load()

        cleaned = OrderedDict()

        for key, value in raw.items():

            norm_key = self.normalize_key(key)

            # skip junk keys
            if len(norm_key) < 2:
                continue

            # validate value
            if not self.is_valid_exe(value):
                continue

            # avoid duplicates
            if norm_key not in cleaned:
                cleaned[norm_key] = value

        self.cleaned_data = cleaned
        return cleaned


    # =========================
    # WRITE CLEAN FILE
    # =========================
    def write_clean(self, output_file="app/data/apps.cleaned.json"):

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.cleaned_data, f, indent=4)

        return output_file


    # =========================
    # RUN FULL PIPELINE
    # =========================
    def run(self):

        print("[Scanner] Loading apps.json...")
        self.scan()

        print("[Scanner] Writing cleaned file...")
        path = self.write_clean()

        print("[Scanner] Done →", path)

        return path