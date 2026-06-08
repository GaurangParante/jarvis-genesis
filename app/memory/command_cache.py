import json
from pathlib import Path


class CommandCache:

    def __init__(self):

        self.cache_file = Path(
            "app/memory/cache.json"
        )

        if not self.cache_file.exists():

            self.cache_file.write_text(
                "{}",
                encoding="utf-8"
            )

    def load(self):

        try:

            with open(
                self.cache_file,
                "r",
                encoding="utf-8"
            ) as f:

                content = f.read().strip()

                if not content:
                    return {}

                return json.loads(content)

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):

            return {}

    def save(self, data):

        with open(
            self.cache_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

    def get(self, query):

        cache = self.load()

        return cache.get(
            query.lower()
        )

    def set(self, query, execution_plan):

        cache = self.load()

        cache[query.lower()] = execution_plan

        self.save(cache)