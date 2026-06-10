import json
import shutil
import re
import webbrowser
import urllib.parse
from groq import Groq
from app.core.config import GROQ_API_KEY
from app.tools.orbit_tools import OrbitTools
from app.tools.file_tools import FileTools
from app.agents.forge.tools import ForgeTools

ALIASES = {
    "microsoft edge": "msedge", "edge": "msedge", "file manager": "explorer",
    "file explorer": "explorer", "visual studio code": "code", "vs code": "code",
    "heidi": "heidisql", "wamp": "wampmanager", "youtube": "https://youtube.com",
    "github": "https://github.com", "google": "https://google.com", "download": "downloads",
    "downloads": "downloads", "desktop": "desktop", "documents": "documents",
}

def extract_command(task: str):
    task = task.lower().strip()
    if task.startswith("open "): return task.replace("open ", "").strip()
    if task.startswith("launch "): return task.replace("launch ", "").strip()
    if task.startswith("start "): return task.replace("start ", "").strip()
    return task

class Executor:
    def __init__(self):
        self.groq_client = Groq(api_key=GROQ_API_KEY)

    def execute(self, queue):
        results = []
        for item in queue:
            agent = item["agent"]
            task = item["task"]
            try:
                result = self.run_task(agent, task)
                results.append({
                    "step": item["step"], "agent": agent, "status": "SUCCESS", "result": result
                })
            except Exception as e:
                results.append({
                    "step": item["step"], "agent": agent, "status": "FAILED", "result": str(e)
                })
        return results

    def resolve_from_apps_json(self, app_name):
        try:
            with open("app/data/apps.json", "r", encoding="utf-8") as f:
                apps = json.load(f)
            if app_name in apps: return apps[app_name]
            for key in apps:
                if app_name in key or key in app_name: return apps[key]
        except: pass
        return None

    def run_task(self, agent, task):
        task_lower = task.lower().strip()

        # Global Search Bypass
        if task_lower.startswith("search ") or "search on youtube" in task_lower or task_lower.startswith("youtube "):
            if "youtube" in task_lower:
                query = task_lower
                for pattern in ["search youtube", "search on youtube", "youtube search", "find on youtube", "youtube"]:
                    query = query.replace(pattern, "")
                query = query.replace("find", "").strip()
                webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}")
                return f"Searching YouTube: {query}"
            
            query = task_lower.replace("search google", "").replace("search for", "").replace("search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
            return f"Searching Google: {query}"

        # ----------------- ORBIT AGENT -----------------
        if agent == "ORBIT":
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

            if "screenshot" in task_lower or "screen shot" in task_lower: return OrbitTools.take_screenshot()
            if "record screen" in task_lower or "screen recording" in task_lower:
                match = re.search(r'(\d+)\s*sec', task_lower)
                return OrbitTools.record_screen(duration=int(match.group(1)) if match else 10)

            if "capture webcam" in task_lower or "webcam image" in task_lower or "take picture" in task_lower: return OrbitTools.capture_webcam_image()
            if "open folder " in task_lower: return FileTools.open_folder_by_name(task_lower.replace("open folder ", "").strip())
            if task_lower.startswith("open file "): return FileTools.open_file_by_name(task_lower.replace("open file ", "").strip())
            if "file explorer" in task_lower or "file manager" in task_lower: return OrbitTools.open_file_explorer()
            if task_lower.startswith("close "): return OrbitTools.close_application(ALIASES.get(task_lower.replace("close ", "").strip(), task_lower.replace("close ", "").strip()))

            if task_lower.startswith("open ") or task_lower.startswith("launch ") or task_lower.startswith("start "):
                app_name = ALIASES.get(extract_command(task_lower), extract_command(task_lower))
                if app_name in ["downloads", "desktop", "documents", "pictures", "music", "videos"]: return OrbitTools.open_application(app_name)
                if app_name in ["msedge", "edge"]:
                    import os; os.system("start microsoft-edge:")
                    return "Microsoft Edge opened"
                if app_name == "wampmanager":
                    import os
                    p = "D:\\wamp64\\wampmanager.exe" if os.path.exists("D:\\wamp64\\wampmanager.exe") else "C:\\wamp64\\wampmanager.exe"
                    if os.path.exists(p): os.startfile(p); return f"WampServer opened from {p[0]}: Drive"
                if str(app_name).startswith("http"): return OrbitTools.open_url(app_name)
                if shutil.which(app_name): return OrbitTools.open_application(app_name)
                resolved = self.resolve_from_apps_json(app_name)
                if resolved: return OrbitTools.open_application(resolved)
                return f"{app_name} not found"

        # ----------------- FORGE AUTONOMOUS CODEX ENGINE -----------------
        if agent == "FORGE":
            print("\n🚀 [FORGE ENGINE] Initializing Codex Agent System...")
            workspace = ForgeTools.get_active_workspace()
            clean_tree = ForgeTools.read_project_structure()
            
            print(f"📂 [FORGE Context] Workspace: {workspace['workspace_path']}")
            print(f"🌲 [FORGE Context] Mapped {len(clean_tree)} active sub-directories (Filtered out .venv)")

            # Loop Setup for Self-Healing (Max 3 Retry cycles)
            retry_count = 0
            max_retries = 3
            last_error_log = "None (First Attempt)"
            
            # Hum LLM ko bolenge ki kis file ko edit karna hai uska path aur raw code JSON me de
            while retry_count < max_retries:
                print(f"🤖 [FORGE Loop] Generation Attempt {retry_count + 1} of {max_retries}...")
                
                prompt = f"""
You are the FORGE Codex Engine, an Autonomous Senior Software Engineer.
Your job is to read a user programming task, analyze the clean project structure layout, write the fix, and output standard instructions.

[CONTEXT WORKSPACE]
Path: {workspace['workspace_path']}
Active Tree Map: {json.dumps(clean_tree, indent=2)}

[USER ASSIGNMENT TASK]
{task}

[LAST TERMINAL RUN STATUS/CRASH ERROR]
{last_error_log}

RULES:
1. Identify which file needs modification or generation based on the tree.
2. Provide the absolute full path of the file and the complete rewritten source code.
3. Return response STRICTLY in the following JSON format. No markdown blocks, no extra prose.
4. CRITICAL: If the user says "update same file", "modify", or mentions an existing file name, you MUST scan the 'Active Tree Map' to find its exact current path. DO NOT create a duplicate at the root if it already exists in a sub-folder.
5. CRITICAL: The 'test_command' MUST execute the exact same file path specified in 'target_file'. Do not test a different file path than the one you just modified.
6. CRITICAL: DO NOT use interactive 'input()' functions in the code if it blocks the terminal execution. Instead, use hardcoded default test values or check for 'sys.argv' inputs, so that the 'test_command' can run completely unattended without waiting for human keyboard interaction.
7. CRITICAL STRUCTURE RULE: If the user requests to generate or write a file mapping the project structure, layout, or tree, DO NOT write a script that runs a raw or unfiltered os.walk() at runtime. Instead, take the clean data provided in the '[CONTEXT WORKSPACE] Active Tree Map' directly and dump that pre-filtered structure layout straight into the target file. Trust the context tree completely, as it already excludes .venv and follows .gitignore rules.

Format:
{{
    "target_file": "absolute_or_relative_path_to_file",
    "code_content": "THE ENTIRE CODE CONTENT GOES HERE",
    "test_command": "command to run and test this code (e.g., python main.py)"
}}
"""
                response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1
                )
                
                content = response.choices[0].message.content.strip()
                match = re.search(r"\{.*\}", content, re.DOTALL)
                
                if not match:
                    return f"FORGE Error: AI didn't return a valid JSON structure. Raw response: {content}"
                
                try:
                    coder_plan = json.loads(match.group())
                    target_file = coder_plan["target_file"]
                    code_content = coder_plan["code_content"]
                    test_command = coder_plan["test_command"]
                except Exception as e:
                    return f"FORGE Parsing Error: {str(e)} -> Content: {content}"

                print(f"📝 [FORGE Action] Modifying file: {target_file}")
                write_status = ForgeTools.write_file_content(target_file, code_content)
                
                if write_status != "SUCCESS":
                    return f"FORGE Write Failure: {write_status}"

                # Test & Verify Wiring Process
                print(f"⚙️ [FORGE Wiring Test] Running validation command: `{test_command}`")
                test_result = ForgeTools.execute_test_command(test_command)
                
                if test_result["exit_code"] == 0:
                    print("✅ [FORGE Engine] Test passed cleanly! Self-healing loop successful.")
                    return f"Successfully completed coding task! Modified: {target_file}. Verification command `{test_command}` ran smoothly with code 0."
                else:
                    print("⚠️ [FORGE Bug Detected] Code compiled with errors. Launching Self-healing...")
                    last_error_log = f"Exit Code: {test_result['exit_code']}\nSTDOUT: {test_result['stdout']}\nSTDERR: {test_result['stderr']}"
                    retry_count += 1
            
            return f"FORGE limits hit: Autopilot processed task but failed validation after {max_retries} cycles. Last Error Log:\n{last_error_log}"

        return f"{agent} received task -> {task}"