import re

from app.tools.orbit_tools import OrbitTools


ALIASES = {

    "microsoft edge": "msedge",
    "edge": "msedge",

    "file manager": "explorer",
    "file explorer": "explorer",

    "visual studio code": "code",
    "vs code": "code",

    "heidi": "heidisql",

    "youtube": "https://youtube.com",
    "github": "https://github.com",
    "google": "https://google.com",
}


class Executor:

    def execute(self, queue):

        results = []

        for item in queue:

            agent = item["agent"]
            task = item["task"]

            try:

                result = self.run_task(
                    agent,
                    task
                )

                results.append(
                    {
                        "step": item["step"],
                        "agent": agent,
                        "status": "SUCCESS",
                        "result": result
                    }
                )

            except Exception as e:

                results.append(
                    {
                        "step": item["step"],
                        "agent": agent,
                        "status": "FAILED",
                        "result": str(e)
                    }
                )

        return results

    def run_task(self, agent, task):

        task_lower = task.lower().strip()

        # ==================================
        # ORBIT AGENT
        # ==================================

        if agent == "ORBIT":

            # -------------------------
            # OPEN FILE EXPLORER
            # -------------------------

            if (
                "file explorer" in task_lower
                or "file manager" in task_lower
            ):
                return OrbitTools.open_file_explorer()

            # -------------------------
            # SEARCH YOUTUBE
            # -------------------------

            if task_lower.startswith("search youtube"):

                query = (
                    task_lower
                    .replace("search youtube", "")
                    .strip()
                )

                return OrbitTools.youtube_search(
                    query
                )

            # -------------------------
            # GOOGLE SEARCH
            # -------------------------

            if task_lower.startswith("search"):

                query = (
                    task_lower
                    .replace("search", "")
                    .strip()
                )

                return OrbitTools.google_search(
                    query
                )

            # -------------------------
            # OPEN COMMAND
            # -------------------------

            if task_lower.startswith("open"):

                app_name = (
                    task_lower
                    .replace("open", "")
                    .strip()
                )

                # Apply alias mapping
                app_name = ALIASES.get(
                    app_name,
                    app_name
                )

                # Website aliases
                if str(app_name).startswith("http"):

                    return OrbitTools.open_url(
                        app_name
                    )

                return OrbitTools.open_application(
                    app_name
                )

        # ==================================
        # APOLLO
        # ==================================

        elif agent == "APOLLO":

            return (
                f"APOLLO received task -> {task}"
            )

        # ==================================
        # FORGE
        # ==================================

        elif agent == "FORGE":

            return (
                f"FORGE received task -> {task}"
            )

        # ==================================
        # PHANTOM
        # ==================================

        elif agent == "PHANTOM":

            return (
                f"PHANTOM received task -> {task}"
            )

        # ==================================
        # ARCHIVE
        # ==================================

        elif agent == "ARCHIVE":

            return (
                f"ARCHIVE received task -> {task}"
            )

        # ==================================
        # TITAN
        # ==================================

        elif agent == "TITAN":

            return (
                f"TITAN received task -> {task}"
            )

        # ==================================
        # ATHENA
        # ==================================

        elif agent == "ATHENA":

            return (
                f"ATHENA received task -> {task}"
            )

        # ==================================
        # MERCURY
        # ==================================

        elif agent == "MERCURY":

            return (
                f"MERCURY received task -> {task}"
            )

        # ==================================
        # NOVA
        # ==================================

        elif agent == "NOVA":

            return (
                f"NOVA received task -> {task}"
            )

        # ==================================
        # SENTINEL
        # ==================================

        elif agent == "SENTINEL":

            return (
                f"SENTINEL received task -> {task}"
            )

        return (
            f"{agent} received task -> {task}"
        )