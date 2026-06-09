import subprocess


class ForgeTools:

    @staticmethod
    def create_laravel_project(project_name):

        cmd = (
            f"composer create-project laravel/laravel "
            f"{project_name}"
        )

        subprocess.Popen(
            cmd,
            shell=True
        )

        return (
            f"Laravel project creation started: "
            f"{project_name}"
        )