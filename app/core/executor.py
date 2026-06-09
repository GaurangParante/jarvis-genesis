import json
import shutil
import re
from app.tools.orbit_tools import OrbitTools
from app.tools.file_tools import FileTools

# =========================
# ALIASES
# =========================
ALIASES = {
    "microsoft edge": "msedge",
    "edge": "msedge",
    "file manager": "explorer",
    "file explorer": "explorer",
    "visual studio code": "code",
    "vs code": "code",
    "heidi": "heidisql",
    "wamp": "wampmanager",
    "youtube": "https://youtube.com",
    "github": "https://github.com",
    "google": "https://google.com",
    "download": "downloads",
    "downloads": "downloads",
    "desktop": "desktop",
    "documents": "documents",
    "download folder": "downloads",
    "desktop folder": "desktop",
    "documents folder": "documents",
}

# =========================
# COMMAND PARSER
# =========================
def extract_command(task: str):
    task = task.lower().strip()
    if task.startswith("open "): return task.replace("open ", "").strip()
    if task.startswith("launch "): return task.replace("launch ", "").strip()
    if task.startswith("start "): return task.replace("start ", "").strip()
    return task

class Executor:
    def execute(self, queue):
        results = []
        for item in queue:
            agent = item["agent"]
            task = item["task"]
            try:
                result = self.run_task(agent, task)
                results.append({
                    "step": item["step"],
                    "agent": agent,
                    "status": "SUCCESS",
                    "result": result
                })
            except Exception as e:
                results.append({
                    "step": item["step"],
                    "agent": agent,
                    "status": "FAILED",
                    "result": str(e)
                })
        return results

    def resolve_from_apps_json(self, app_name):
        try:
            with open("app/data/apps.json", "r", encoding="utf-8") as f:
                apps = json.load(f)
            if app_name in apps: return apps[app_name]
            for key in apps:
                if app_name in key or key in app_name:
                    return apps[key]
        except:
            pass
        return None

    # =========================
    # MAIN ROUTER
    # =========================
    def run_task(self, agent, task):
        task_lower = task.lower().strip()

        if agent == "ORBIT":
            # -------------------------
            # HARDWARE CONTROL (VOLUME / BRIGHTNESS)
            # -------------------------
            if "volume" in task_lower:
                match = re.search(r'(\d+)', task_lower)
                level = int(match.group(1)) if match else None
                if "mute" in task_lower: return OrbitTools.set_volume(0)
                if "max" in task_lower or "full" in task_lower: return OrbitTools.set_volume(100)
                if level is not None: return OrbitTools.set_volume(level)

            if "brightness" in task_lower:
                match = re.search(r'(\d+)', task_lower)
                level = int(match.group(1)) if match else None
                if "max" in task_lower or "full" in task_lower: return OrbitTools.set_brightness(100)
                if level is not None: return OrbitTools.set_brightness(level)

            # -------------------------
            # MEDIA & CAPTURE
            # -------------------------
            if "screenshot" in task_lower or "screen shot" in task_lower:
                return OrbitTools.take_screenshot()

            if "record screen" in task_lower or "screen recording" in task_lower:
                # Isme simple duration toggle match de rahe hain default 10s ke liye
                match = re.search(r'(\d+)\s*sec', task_lower)
                duration = int(match.group(1)) if match else 10
                return OrbitTools.record_screen(duration=duration)

            if "capture webcam" in task_lower or "webcam image" in task_lower or "take picture" in task_lower:
                return OrbitTools.capture_webcam_image()

            if "record webcam" in task_lower or "video from webcam" in task_lower:
                match = re.search(r'(\d+)\s*sec', task_lower)
                duration = int(match.group(1)) if match else 10
                return OrbitTools.record_webcam_video(duration=duration)

            # -------------------------
            # SYSTEM FILES & FOLDERS
            # -------------------------
            if task_lower.startswith("open folder "):
                folder_name = task_lower.replace("open folder ", "").strip()
                return FileTools.open_folder_by_name(folder_name)

            if task_lower.startswith("open file "):
                file_name = task_lower.replace("open file ", "").strip()
                return FileTools.open_file_by_name(file_name)

            # -------------------------
            # FILE EXPLORER / SEARCHES / BASICS
            # -------------------------
            if "file explorer" in task_lower or "file manager" in task_lower:
                return OrbitTools.open_file_explorer()

            youtube_patterns = ["search youtube", "search on youtube", "youtube search", "find on youtube"]
            for pattern in youtube_patterns:
                if task_lower.startswith(pattern):
                    query = task_lower.replace(pattern, "").strip()
                    return OrbitTools.youtube_search(query)

            if task_lower.startswith("search "):
                query = task_lower.replace("search ", "").strip()
                return OrbitTools.google_search(query)

            if task_lower == "open downloads": return OrbitTools.open_downloads()
            if task_lower == "open desktop": return OrbitTools.open_desktop()

            # -------------------------
            # CLOSE APP
            # -------------------------
            if task_lower.startswith("close "):
                app_name = task_lower.replace("close ", "").strip()
                app_name = ALIASES.get(app_name, app_name)
                return OrbitTools.close_application(app_name)

            # -------------------------
            # OPEN COMMAND (FIXED CORE V2)
            # -------------------------
            if task_lower.startswith("open "):
                app_name = extract_command(task_lower)
                app_name = ALIASES.get(app_name, app_name)

                # PRIORITY 1: Special Folders Check (Bina shutil.which pe gaye)
                # OrbitTools ke paas already SPECIAL_FOLDERS ki list hai
                if app_name in ["downloads", "desktop", "documents", "pictures", "music", "videos"]:
                    return OrbitTools.open_application(app_name)

                # PRIORITY 2: Edge Browser Protocol
                if app_name in ["msedge", "edge"]:
                    import os
                    os.system("start microsoft-edge:")
                    return "Microsoft Edge opened"
                
                if app_name == "wampmanager":
                    import os
                    if os.path.exists("D:\\wamp64\\wampmanager.exe"):
                        os.startfile("D:\\wamp64\\wampmanager.exe")
                        return "WampServer opened from D: Drive"
                    elif os.path.exists("C:\\wamp64\\wampmanager.exe"):
                        os.startfile("C:\\wamp64\\wampmanager.exe")
                        return "WampServer opened from C: Drive"

                # PRIORITY 3: URL/Websites
                if str(app_name).startswith("http"):
                    return OrbitTools.open_url(app_name)

                # PRIORITY 4: Check PATH System Executables
                path = shutil.which(app_name)
                if path: 
                    return OrbitTools.open_application(app_name)

                # PRIORITY 5: apps.json lookup fallback
                resolved = self.resolve_from_apps_json(app_name)
                if resolved: 
                    return OrbitTools.open_application(resolved)

                return f"{app_name} not found"

        # Baaki agents fallback return logic
        return f"{agent} received task -> {task}"