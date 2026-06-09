import os
import webbrowser
import subprocess
import shutil


class OrbitTools:

    # -------------------------
    # OPEN APPLICATION
    # -------------------------

    @staticmethod
    def open_application(app_name):

        try:

            app_name = app_name.strip()

            path = shutil.which(app_name)

            if path:

                subprocess.Popen(path)

                return f"{app_name} opened"

            subprocess.Popen(
                f'start "" "{app_name}"',
                shell=True
            )

            return f"{app_name} opened"

        except Exception:

            return f"{app_name} not found"

    # -------------------------
    # OPEN WEBSITE
    # -------------------------

    @staticmethod
    def open_url(url):

        webbrowser.open(url)

        return f"Opened {url}"

    # -------------------------
    # GOOGLE SEARCH
    # -------------------------

    @staticmethod
    def google_search(query):

        url = (
            "https://www.google.com/search?q="
            + query.replace(" ", "+")
        )

        webbrowser.open(url)

        return f"Searching Google: {query}"

    # -------------------------
    # YOUTUBE SEARCH
    # -------------------------

    @staticmethod
    def youtube_search(query):

        url = (
            "https://www.youtube.com/results?search_query="
            + query.replace(" ", "+")
        )

        webbrowser.open(url)

        return f"Searching YouTube: {query}"

    # -------------------------
    # FILE EXPLORER
    # -------------------------

    @staticmethod
    def open_file_explorer():

        subprocess.Popen("explorer")

        return "File Explorer opened"

    # -------------------------
    # OPEN FOLDER
    # -------------------------

    @staticmethod
    def open_folder(path):

        if os.path.exists(path):

            os.startfile(path)

            return f"Opened folder: {path}"

        return "Folder not found"

    # -------------------------
    # OPEN FILE
    # -------------------------

    @staticmethod
    def open_file(path):

        if os.path.exists(path):

            os.startfile(path)

            return f"Opened file: {path}"

        return "File not found"