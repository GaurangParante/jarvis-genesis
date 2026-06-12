import json
import re
import shutil
import urllib.parse
import webbrowser

from app.core.safety_manager import SafetyManager
from app.providers.provider_manager import ProviderManager
from app.providers.base import ChatRequest

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
}


def extract_command(task: str):
    task = task.lower().strip()
    if task.startswith("open "):
        return task.replace("open ", "").strip()
    if task.startswith("launch "):
        return task.replace("launch ", "").strip()
    if task.startswith("start "):
        return task.replace("start ", "").strip()
    return task


class Executor:
    def __init__(self):
        self.providers = ProviderManager()
        self.safety = SafetyManager()

    def execute(self, queue):
        results = []

        for item in queue:
            agent = item["agent"]
            task = item["task"]

            decision = self.safety.evaluate(
                agent,
                task,
                requires_confirmation=item.get("requires_confirmation", False),
            )

            if decision.requires_confirmation:
                prompt = (
                    f"[SAFETY] Step {item['step']} for {agent} needs confirmation: "
                    f"{decision.reason}\n"
                    "Type YES to continue: "
                )
                user_choice = input(prompt).strip().lower()
                if user_choice not in {"yes", "y"}:
                    results.append(
                        {
                            "step": item["step"],
                            "agent": agent,
                            "status": "SKIPPED",
                            "result": f"Skipped by user approval gate. {decision.reason}",
                        }
                    )
                    continue

            try:
                result = self.run_task(agent, task)
                results.append(
                    {
                        "step": item["step"],
                        "agent": agent,
                        "status": "SUCCESS",
                        "result": result,
                    }
                )
            except Exception as exc:
                results.append(
                    {
                        "step": item["step"],
                        "agent": agent,
                        "status": "FAILED",
                        "result": str(exc),
                    }
                )

        return results

    def _load_orbit_tools(self):
        from app.tools.orbit_tools import OrbitTools

        return OrbitTools

    def _load_file_tools(self):
        from app.tools.file_tools import FileTools

        return FileTools

    def _load_forge_tools(self):
        from app.agents.forge.tools import ForgeTools

        return ForgeTools

    def _load_research_tools(self):
        from app.tools.research_tools import ResearchTools

        return ResearchTools

    def _generate_text_response(self, agent, task, style):
        language_hint = self._language_hint(task)
        prompt = (
            f"You are {agent}, a specialized assistant.\n"
            f"Task: {task}\n\n"
            f"Language style: {language_hint}\n"
            f"Write the final user-facing answer in {style} style.\n"
            "Do not mention agent routing, internal steps, or hidden planning.\n"
            "Return the actual answer only."
        )

        try:
            _, content = self.providers.chat(
                ChatRequest(
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.4,
                ),
                task_text=task,
                purpose="generation",
            )
            return content
        except Exception:
            return f"{agent} could not generate a rich response, but handled the task: {task}"

    def _generate_chat_response(self, task):
        language_hint = self._language_hint(task)
        prompt = (
            "You are a friendly assistant. Answer naturally and directly.\n"
            "If the user asked for a joke, tell one short joke only.\n"
            "If the user is chatting, respond in a warm and concise way.\n"
            f"Language style: {language_hint}\n"
            f"User message: {task}\n"
            "Do not mention agents, workflow, or internal steps."
        )

        try:
            _, content = self.providers.chat(
                ChatRequest(
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.6,
                ),
                task_text=task,
                purpose="chat",
            )
            return content
        except Exception:
            lower = task.lower()
            if "joke" in lower or "funny" in lower or "laugh" in lower:
                return "Computer therapy session mein gaya aur bola, 'Mujhe bohot zyada bytes of emotional baggage hai.'"
            return "Main ready hoon. Jo chahiye bolo, main help karunga."

    def _language_hint(self, task: str) -> str:
        text = task.lower()
        devanagari = any("\u0900" <= ch <= "\u097f" for ch in task)
        hinglish_markers = (
            "kya",
            "koi",
            "sunao",
            "please",
            "bhai",
            "bata",
            "kr",
            "kar",
            "hath",
            "hathi",
            "ek aur",
        )

        if devanagari:
            return "Respond in Hindi using Devanagari script."
        if any(marker in text for marker in hinglish_markers):
            return "Respond in Hinglish with simple, natural Hindi-English mix."
        return "Respond in the same language as the user."

    def resolve_from_apps_json(self, app_name):
        try:
            with open("app/data/apps.json", "r", encoding="utf-8") as f:
                apps = json.load(f)
            if app_name in apps:
                return apps[app_name]
            for key in apps:
                if app_name in key or key in app_name:
                    return apps[key]
        except Exception:
            pass
        return None

    def run_task(self, agent, task):
        task_lower = task.lower().strip()
        orbit_tools = self._load_orbit_tools()
        file_tools = self._load_file_tools()

        if task_lower.startswith("search ") or "search on youtube" in task_lower or task_lower.startswith("youtube "):
            if "youtube" in task_lower:
                query = task_lower
                for pattern in [
                    "search youtube",
                    "search on youtube",
                    "youtube search",
                    "find on youtube",
                    "youtube",
                ]:
                    query = query.replace(pattern, "")
                query = query.replace("find", "").strip()
                webbrowser.open(
                    f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
                )
                return f"Searching YouTube: {query}"

            query = (
                task_lower.replace("search google", "")
                .replace("search for", "")
                .replace("search", "")
                .strip()
            )
            webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
            return f"Searching Google: {query}"

        if agent == "ORBIT":
            if "volume" in task_lower:
                match = re.search(r"(\d+)", task_lower)
                level = int(match.group(1)) if match else None
                if "mute" in task_lower:
                    return orbit_tools.set_volume(0)
                if "max" in task_lower or "full" in task_lower:
                    return orbit_tools.set_volume(100)
                if level is not None:
                    return orbit_tools.set_volume(level)

            if "brightness" in task_lower:
                match = re.search(r"(\d+)", task_lower)
                level = int(match.group(1)) if match else None
                if "max" in task_lower or "full" in task_lower:
                    return orbit_tools.set_brightness(100)
                if level is not None:
                    return orbit_tools.set_brightness(level)

            if "screenshot" in task_lower or "screen shot" in task_lower:
                return orbit_tools.take_screenshot()

            if "record screen" in task_lower or "screen recording" in task_lower:
                match = re.search(r"(\d+)\s*sec", task_lower)
                return orbit_tools.record_screen(duration=int(match.group(1)) if match else 10)

            if (
                "capture webcam" in task_lower
                or "webcam image" in task_lower
                or "take picture" in task_lower
            ):
                return orbit_tools.capture_webcam_image()

            if "open folder " in task_lower:
                return file_tools.open_folder_by_name(task_lower.replace("open folder ", "").strip())

            if task_lower.startswith("open file "):
                return file_tools.open_file_by_name(task_lower.replace("open file ", "").strip())

            if "file explorer" in task_lower or "file manager" in task_lower:
                return orbit_tools.open_file_explorer()

            if task_lower.startswith("close "):
                return orbit_tools.close_application(
                    ALIASES.get(
                        task_lower.replace("close ", "").strip(),
                        task_lower.replace("close ", "").strip(),
                    )
                )

            if task_lower.startswith("open ") or task_lower.startswith("launch ") or task_lower.startswith("start "):
                app_name = ALIASES.get(extract_command(task_lower), extract_command(task_lower))
                if app_name in ["downloads", "desktop", "documents", "pictures", "music", "videos"]:
                    return orbit_tools.open_application(app_name)
                if app_name in ["msedge", "edge"]:
                    import os

                    os.system("start microsoft-edge:")
                    return "Microsoft Edge opened"
                if app_name == "wampmanager":
                    import os

                    p = (
                        "D:\\wamp64\\wampmanager.exe"
                        if os.path.exists("D:\\wamp64\\wampmanager.exe")
                        else "C:\\wamp64\\wampmanager.exe"
                    )
                    if os.path.exists(p):
                        os.startfile(p)
                        return f"WampServer opened from {p[0]}: Drive"
                if str(app_name).startswith("http"):
                    return orbit_tools.open_url(app_name)
                if shutil.which(app_name):
                    return orbit_tools.open_application(app_name)
                resolved = self.resolve_from_apps_json(app_name)
                if resolved:
                    return orbit_tools.open_application(resolved)
                return f"{app_name} not found"

        if agent == "PHANTOM":
            research_tools = self._load_research_tools()
            helper = research_tools()
            return helper.research(task, provider_manager=self.providers)

        if agent == "CHAT":
            return self._generate_chat_response(task)

        if agent == "APOLLO":
            return self._generate_text_response(
                "APOLLO",
                task,
                "a polished YouTube research, script, title, description, and SEO recommendation"
            )

        if agent == "NOVA":
            return self._generate_text_response(
                "NOVA",
                task,
                "a ready-to-post social media draft with captions and hashtags"
            )

        if agent == "MERCURY":
            return self._generate_text_response(
                "MERCURY",
                task,
                "a professional email draft or reply"
            )

        if agent == "ARCHIVE":
            return self._generate_text_response(
                "ARCHIVE",
                task,
                "a clear knowledge note or document summary"
            )

        if agent == "TITAN":
            return self._generate_text_response(
                "TITAN",
                task,
                "a finance summary with actionable insights"
            )

        if agent == "ATHENA":
            return self._generate_text_response(
                "ATHENA",
                task,
                "a fitness or health plan with practical guidance"
            )

        if agent == "SENTINEL":
            return self._generate_text_response(
                "SENTINEL",
                task,
                "a security review or safety recommendation"
            )

        if agent == "FORGE":
            print("\n[FORGE ENGINE] Initializing Codex Agent System...")
            forge_tools = self._load_forge_tools()
            workspace = forge_tools.get_active_workspace()
            clean_tree = forge_tools.read_project_structure()

            print(f"[FORGE Context] Workspace: {workspace['workspace_path']}")
            print(
                f"[FORGE Context] Mapped {len(clean_tree)} active sub-directories "
                f"(Filtered out .venv)"
            )

            retry_count = 0
            max_retries = 3
            last_error_log = "None (First Attempt)"

            while retry_count < max_retries:
                print(f"[FORGE Loop] Generation Attempt {retry_count + 1} of {max_retries}...")

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
                try:
                    _, coder_plan = self.providers.chat_json(
                        prompt,
                        task_text=task,
                        purpose="coding",
                    )
                    target_file = coder_plan["target_file"]
                    code_content = coder_plan["code_content"]
                    test_command = coder_plan["test_command"]
                except Exception as exc:
                    return f"FORGE Parsing Error: {str(exc)}"

                print(f"[FORGE Action] Modifying file: {target_file}")
                write_status = forge_tools.write_file_content(target_file, code_content)

                if write_status != "SUCCESS":
                    return f"FORGE Write Failure: {write_status}"

                print(f"[FORGE Wiring Test] Running validation command: `{test_command}`")
                test_result = forge_tools.execute_test_command(test_command)

                if test_result["exit_code"] == 0:
                    print("[FORGE Engine] Test passed cleanly! Self-healing loop successful.")
                    return (
                        f"Successfully completed coding task! Modified: {target_file}. "
                        f"Verification command `{test_command}` ran smoothly with code 0."
                    )

                print("[FORGE Bug Detected] Code compiled with errors. Launching Self-healing...")
                last_error_log = (
                    f"Exit Code: {test_result['exit_code']}\n"
                    f"STDOUT: {test_result['stdout']}\n"
                    f"STDERR: {test_result['stderr']}"
                )
                retry_count += 1

            return (
                f"FORGE limits hit: Autopilot processed task but failed validation after {max_retries} cycles. "
                f"Last Error Log:\n{last_error_log}"
            )

        return f"{agent} received task -> {task}"
