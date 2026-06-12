import os
import webbrowser
import subprocess
import shutil
import time
from datetime import datetime
from pathlib import Path
import json

try:
    import psutil
except ImportError:
    psutil = None

try:
    import numpy as np
except ImportError:
    np = None

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import mss
except ImportError:
    mss = None

try:
    import screen_brightness_control as sbc
except ImportError:
    sbc = None

SPECIAL_FOLDERS = {
    "desktop": os.path.join(os.environ.get("USERPROFILE", str(Path.home())), "Desktop"),
    "downloads": os.path.join(os.environ.get("USERPROFILE", str(Path.home())), "Downloads"),
    "documents": os.path.join(os.environ.get("USERPROFILE", str(Path.home())), "Documents"),
    "pictures": os.path.join(os.environ.get("USERPROFILE", str(Path.home())), "Pictures"),
    "music": os.path.join(os.environ.get("USERPROFILE", str(Path.home())), "Music"),
    "videos": os.path.join(os.environ.get("USERPROFILE", str(Path.home())), "Videos"),
}

class OrbitTools:
    SPECIAL_FOLDERS = SPECIAL_FOLDERS

    @staticmethod
    def open_application(app_name):
        app_name = app_name.lower().strip()
        if app_name in SPECIAL_FOLDERS:
            os.startfile(SPECIAL_FOLDERS[app_name])
            return f"{app_name} folder opened"
        try:
            with open("app/data/app_aliases.json", "r", encoding="utf-8") as f:
                aliases = json.load(f)
        except Exception:
            aliases = {}
        app_name = aliases.get(app_name, app_name)

        if app_name.startswith("http"):
            webbrowser.open(app_name)
            return f"Opened {app_name}"

        path = shutil.which(app_name)
        if path:
            subprocess.Popen(path)
            return f"{app_name} opened"

        try:
            with open("app/data/apps.json", "r", encoding="utf-8") as f:
                apps = json.load(f)
        except Exception:
            apps = {}

        if app_name in apps:
            subprocess.Popen(apps[app_name])
            return f"{app_name} opened"

        return f"{app_name} not found"

    @staticmethod
    def open_url(url):
        webbrowser.open(url)
        return f"Opened {url}"

    @staticmethod
    def google_search(query):
        url = "https://www.google.com/search?q=" + query.replace(" ", "+")
        webbrowser.open(url)
        return f"Searching Google: {query}"

    @staticmethod
    def youtube_search(query):
        url = "https://www.youtube.com/results?search_query=" + query.replace(" ", "+")
        webbrowser.open(url)
        return f"Searching YouTube: {query}"

    @staticmethod
    def open_file_explorer():
        subprocess.Popen("explorer")
        return "File Explorer opened"

    @staticmethod
    def close_application(app_name):
        if psutil is None:
            return "psutil is not installed; cannot close applications."
        app_name = app_name.lower()
        closed = False
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                process_name = proc.info["name"].lower()
                if app_name in process_name or app_name.replace(".exe", "") in process_name:
                    proc.kill()
                    closed = True
            except Exception:
                pass
        return f"{app_name} closed" if closed else f"{app_name} not running"

    @staticmethod
    def open_downloads():
        os.startfile(SPECIAL_FOLDERS["downloads"])
        return "Downloads opened"

    @staticmethod
    def open_desktop():
        os.startfile(SPECIAL_FOLDERS["desktop"])
        return "Desktop opened"

    # ==================================
    # NEW EXTENDED HARDWARE FEATURES
    # ==================================

    @staticmethod
    def set_volume(level: int):
        try:
            import ctypes
            import time
            
            level = max(0, min(100, level))
            
            # Windows Virtual Key Codes for Volume
            VK_VOLUME_MUTE = 0xAD
            VK_VOLUME_DOWN = 0xAE
            VK_VOLUME_UP = 0xAF
            
            # Master volume controller instance via Shell Object
            # Yeh bina pycaw ke direct hardware volume levels toggle karega
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            
            # Step 1: Pehle system ko full mute (0) pe le jao taaki ek base point mile
            # 50 baar volume down dabane se volume pakka 0 ho jayega
            for _ in range(50):
                shell.SendKeys(chr(VK_VOLUME_DOWN))
                
            # Step 2: Ab jitna level chahiye us hisab se UP keys press karo
            # Windows me 1 key press = 2% volume bar growth
            up_clicks = int(level / 2)
            for _ in range(up_clicks):
                shell.SendKeys(chr(VK_VOLUME_UP))
                
            return f"Volume set to {level}%"
            
        except Exception as e:
            return f"Failed to set volume via Shell: {str(e)}"

    @staticmethod
    def set_brightness(level: int):
        if sbc is None:
            return "screen_brightness_control is not installed."
        try:
            level = max(0, min(100, level))
            sbc.set_brightness(level)
            return f"Brightness set to {level}%"
        except Exception as e:
            return f"Failed to set brightness: {str(e)}"

    # ==================================
    # MEDIA CAPTURES & RECORDINGS
    # ==================================

    @staticmethod
    def take_screenshot():
        if mss is None:
            return "mss is not installed."
        os.makedirs("app/data/screenshots", exist_ok=True)
        filename = f"app/data/screenshots/screenshot_{datetime.now():%Y%m%d_%H%M%S}.png"
        try:
            with mss.mss() as sct:
                sct.shot(output=filename)
            return f"Screenshot saved -> {filename}"
        except Exception as e:
            return f"Screenshot failed -> {str(e)}"

    @staticmethod
    def capture_webcam_image():
        if cv2 is None:
            return "opencv-python is not installed."
        os.makedirs("app/data/captures", exist_ok=True)
        filename = f"app/data/captures/webcam_{datetime.now():%Y%m%d_%H%M%S}.jpg"
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Fast boot capture
        if not cap.isOpened():
            return "Error: Webcam could not be accessed."
        time.sleep(1.5) # Camera warm-up delay time
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(filename, frame)
            cap.release()
            return f"Webcam Image saved -> {filename}"
        cap.release()
        return "Failed to grab frame from webcam"

    @staticmethod
    def record_webcam_video(duration=10):
        if cv2 is None:
            return "opencv-python is not installed."
        os.makedirs("app/data/recordings", exist_ok=True)
        filename = f"app/data/recordings/webcam_rec_{datetime.now():%Y%m%d_%H%M%S}.mp4"
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened(): return "Error: Webcam not accessible."
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
        
        start_time = time.time()
        while int(time.time() - start_time) < duration:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                break
        cap.release()
        out.release()
        return f"Webcam Video recorded ({duration}s) -> {filename}"

    @staticmethod
    def record_screen(duration=10):
        if mss is None or np is None or cv2 is None:
            return "screen recording dependencies are not installed."
        os.makedirs("app/data/recordings", exist_ok=True)
        filename = f"app/data/recordings/screen_rec_{datetime.now():%Y%m%d_%H%M%S}.mp4"
        
        with mss.mss() as sct:
            monitor = sct.monitors[1] # Primary screen
            width = monitor["width"]
            height = monitor["height"]
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(filename, fourcc, 12.0, (width, height))
            
            start_time = time.time()
            while int(time.time() - start_time) < duration:
                img = np.array(sct.grab(monitor))
                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) # Matrix compression
                out.write(frame)
                time.sleep(0.05) # Cap loop rate
                
            out.release()
        return f"Screen Recording saved ({duration}s) -> {filename}"
