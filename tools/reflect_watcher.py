import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from datetime import datetime
import os

# CONFIGURABLE PATHS
log_folder = r"YOUR_PATH_HERE\text-generation-webui\logs\chat\Nous-Hermes-LLaMa-2-7B-GPTQ"
reflection_template_path = r"YOUR_PATH_HERE\memory_core\reflection_template.txt"
reflections_output_path = r"YOUR_PATH_HERE\memory_core\reflections.txt"
latest_reflect_path = r"YOUR_PATH_HERE\memory_core\latest_reflect.txt"
recent_memory_script_path = r"YOUR_PATH_HERE\scripts\recent_memory.py"
latest_injector_script_path = r"YOUR_PATH_HERE\latest_reflect_injector.py"

def find_latest_json_file(folder):
    json_files = [f for f in os.listdir(folder) if f.endswith(".json")]
    if not json_files:
        return None
    full_paths = [os.path.join(folder, f) for f in json_files]
    return max(full_paths, key=os.path.getmtime)

class ReflectFromLatestJsonHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".json"):
            latest_file = find_latest_json_file(log_folder)
            if not latest_file:
                return
        try:
            with open(latest_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "internal" not in data:
                return
            last_pairs = data["internal"][-10:]
            for user_msg, assistant_msg in last_pairs:
                # Look for "reflect" even if not in brackets
                if "reflect" in assistant_msg.lower():  # This will detect "reflect", "reflection", etc.
                    timestamp = datetime.now().strftime("%Y-%m-%d (%A)")

                    # Save to latest_reflect.txt
                    with open(latest_reflect_path, "w", encoding="utf-8") as latest_file_out:
                        latest_file_out.write(assistant_msg.strip())

                    # Save longform to reflections.txt
                    with open(reflection_template_path, "r", encoding="utf-8") as template:
                        reflection = template.read()
                    
                    # Skip saving if template still has blanks
                    if "__________" in reflection:
                        print("🛑 Reflection template not filled in — skipping save to reflections.txt.")
                    else:
                        reflection_with_time = f"[REFLECTION_START]\nReflection Date: {timestamp}\n\n" + reflection
                        with open(reflections_output_path, "a", encoding="utf-8") as out:
                            out.write("\n" + reflection_with_time.strip() + "\n")
                    print("💾 Saved filled-in reflection to reflections.txt.")

                    print("Detected [reflect] in:", os.path.basename(latest_file), "at", timestamp)
                    print("Saving to reflections.txt and latest_reflect.txt...")
                    print("Running recent_memory.py and latest_reflect_injector.py...\n")

                    os.system(f'python "{recent_memory_script_path}"')
                    os.system(f'python "{latest_injector_script_path}"')
                    break
        except Exception as e:
            print("Error reading JSON:", e)


if os.path.exists(log_folder):
    event_handler = ReflectFromLatestJsonHandler()
    observer = Observer()
    observer.schedule(event_handler, path=log_folder, recursive=False)
    observer.start()
    print("Watcher started. Monitoring for [reflect]... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
else:
    print("Log folder not found. Please check the path.")