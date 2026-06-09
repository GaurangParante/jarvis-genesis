import os
import json


class AppDiscovery:

    SEARCH_DIRS = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        os.path.expandvars(r"%LOCALAPPDATA%"),
    ]

    OUTPUT_FILE = "app/data/apps.json"

    @classmethod
    def scan(cls):

        apps = {}

        for root_dir in cls.SEARCH_DIRS:

            if not os.path.exists(root_dir):
                continue

            for root, dirs, files in os.walk(root_dir):

                for file in files:

                    if file.endswith(".exe"):

                        name = (
                            file.replace(".exe", "")
                            .lower()
                            .strip()
                        )

                        if name not in apps:

                            apps[name] = os.path.join(
                                root,
                                file
                            )

        os.makedirs(
            "app/data",
            exist_ok=True
        )

        with open(
            cls.OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                apps,
                f,
                indent=4
            )

        print(
            f"{len(apps)} applications indexed."
        )