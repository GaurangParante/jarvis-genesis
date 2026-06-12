import os
import subprocess
from pathlib import Path

try:
    import psutil
except ImportError:
    psutil = None

class ForgeTools:
    
    @staticmethod
    def get_active_workspace():
        """Detects if VS Code is open and hooks the current working directory."""
        vscode_active = False
        if psutil is not None:
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] and 'code' in proc.info['name'].lower():
                        vscode_active = True
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                
        current_dir = os.getcwd()
        return {
            "workspace_path": current_dir,
            "vs_code_active": vscode_active,
            "project_name": os.path.basename(current_dir)
        }

    @staticmethod
    def read_project_structure(root_dir=None):
        """Generates a clean structure, dynamically parsing and respecting .gitignore rules."""
        if not root_dir:
            root_dir = os.getcwd()
            
        structure = {}
        
        # Base hardcoded kachra list
        ignore_dirs = {'.git', '__pycache__', '.venv', 'venv', 'node_modules'}
        ignore_files = set()

        # Dynamic .gitignore Parsing Logic
        gitignore_path = os.path.join(root_dir, '.gitignore')
        if os.path.exists(gitignore_path):
            try:
                with open(gitignore_path, 'r', encoding='utf-8') as gf:
                    for line in gf:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Strip slashes to match folder/file names loosely
                            clean_pattern = line.replace('/', '').replace('*', '')
                            if clean_pattern:
                                if line.endswith('/') or '.' not in clean_pattern:
                                    ignore_dirs.add(clean_pattern)
                                else:
                                    ignore_files.add(clean_pattern)
            except Exception:
                pass # Fallback to base ignore list if file is unreadable
        
        for root, dirs, files in os.walk(root_dir):
            # Prune unwanted directories instantly
            dirs[:] = [d for d in dirs if d not in ignore_dirs and not any(p in d for p in ignore_dirs if p)]
            
            relative_path = os.path.relpath(root, root_dir)
            if relative_path == ".":
                relative_path = "root"
                
            # Filter files using base list + dynamic gitignore patterns
            clean_files = []
            for f in files:
                if f.endswith(('.pyc', '.pyo', '.pyd', '.class')):
                    continue
                # Skip if file matches any gitignore file pattern
                if f in ignore_files or any(pat in f for pat in ignore_files if pat):
                    continue
                clean_files.append(f)
                
            structure[relative_path] = clean_files
            
        return structure

    @staticmethod
    def read_file_content(file_path):
        """Reads code from a specific project file safely."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @staticmethod
    def write_file_content(file_path, content):
        """Writes or modifies code with an automatic safety backup (.bak)."""
        try:
            target_path = Path(file_path)
            if target_path.exists():
                backup = target_path.with_suffix(target_path.suffix + '.bak')
                with open(target_path, 'r', encoding='utf-8') as src, open(backup, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
                    
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return "SUCCESS"
        except Exception as e:
            return f"FAILED: {str(e)}"

    @staticmethod
    def execute_test_command(command, timeout=20):
        """Runs the test or script in the terminal and grabs the error logs."""
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=timeout
            )
            return {
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"exit_code": -1, "stdout": "", "stderr": "Execution Timeout."}
