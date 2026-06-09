import os

class FileTools:

    @staticmethod
    def get_search_directories():
        user_profile = os.environ["USERPROFILE"]
        
        # Base locations jahan user ka data hone ke chances 99% hote hain
        paths = [
            os.getcwd(),  # Current project folder
            user_profile, # User root (yahan se Desktop, Downloads automatic scan ho sakte hain)
            "C:\\",       # C Drive Root
        ]
        
        # Agar system me D Drive exist karti hai to use bhi add karo
        if os.path.exists("D:\\"):
            paths.append("D:\\")
            
        return [p for p in paths if os.path.exists(p)]

    @staticmethod
    def open_folder_by_name(folder_name: str):
        folder_name = folder_name.lower().strip()
        search_dirs = FileTools.get_search_directories()
        
        # System/Windows folders ko skip karne ke liye filters (Taaki search fast ho)
        skip_folders = ["$recycle.bin", "windows", "program files", "program files (x86)", "appdata", "microsoft"]

        for base_dir in search_dirs:
            try:
                # Level 1: Pehle direct root directories me check karo
                for item in os.listdir(base_dir):
                    if item.lower() in skip_folders:
                        continue
                        
                    item_path = os.path.join(base_dir, item)
                    
                    if os.path.isdir(item_path):
                        # Agar folder ka naam exactly match ya partial match ho jaye
                        if folder_name in item.lower():
                            os.startfile(item_path)
                            return f"Opened folder: {item_path}"
                            
                        # Level 2: Ek step aur andar check karo (e.g., D:\gaurang\projects)
                        try:
                            # Is check ko sirf 1st subfolder tak limit rakha hai speed ke liye
                            if base_dir in ["C:\\", "D:\\"] and item.lower() == "users":
                                continue # Users ke andar direct deep scan skip karo, user_profile handle kar lega
                                
                            for sub_item in os.listdir(item_path):
                                sub_item_path = os.path.join(item_path, sub_item)
                                if os.path.isdir(sub_item_path) and folder_name == sub_item.lower():
                                    os.startfile(sub_item_path)
                                    return f"Opened folder: {sub_item_path}"
                        except Exception:
                            continue
            except Exception:
                continue
                
        return f"Folder containing '{folder_name}' not found in C: or D: drives."

    @staticmethod
    def open_file_by_name(file_name: str):
        file_name = file_name.lower().strip()
        search_dirs = FileTools.get_search_directories()
        skip_folders = ["windows", "program files", "program files (x86)", "appdata", ".git", ".venv"]

        for base_dir in search_dirs:
            try:
                # Direct os.walk fallback but with targeted max-depth checking to maintain extreme speed
                for root, dirs, files in os.walk(base_dir):
                    # Filter paths early
                    dirs[:] = [d for d in dirs if d.lower() not in skip_folders]
                    
                    # Prevent going into infinitely deep system paths
                    if root.count(os.sep) - base_dir.count(os.sep) > 3:
                        del dirs[:] # Stop deeper evaluation
                        continue
                        
                    for file in files:
                        if file_name in file.lower():
                            full_path = os.path.join(root, file)
                            os.startfile(full_path)
                            return f"Opened file: {full_path}"
            except Exception:
                continue
        return f"File matching '{file_name}' not found."