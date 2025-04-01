import re
from datetime import datetime

# File paths - update as needed
yaml_path = r"YOUR_PATH_HERE\text-generation-webui\characters\Nous-Hermes-LLaMa-2-7B-GPTQ.yaml"
latest_reflect_path = r"YOUR_PATH_HERE\memory_core\latest_reflect.txt"

def inject_last_reflection():
    try:
        with open(latest_reflect_path, "r", encoding="utf-8") as f:
            reflection = f.read().strip()

        if not reflection:
            print("⚠️ No reflection found in latest_reflect.txt.")
            return

        with open(yaml_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        in_last_reflection = False
        injected = False

        for line in lines:
            if "Last Reflection:" in line:
                new_lines.append(line)
                in_last_reflection = True
                continue 

            if in_last_reflection:
                if line.startswith("  ") or not line.strip():
                    continue  # skip old placeholder or previous value
                else:
                    # new top-level key begins, stop replacing
                    in_last_reflection = False
                    new_lines.append(f"  {reflection}\n")
                    injected = True

            if not in_last_reflection:
                new_lines.append(line)

        if not injected and in_last_reflection:
            new_lines.append(f"  {reflection}\n")

        with open(yaml_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        print("✅ Last Reflection updated successfully!")
    except Exception as e:
        print(f"⚠️ Error during reflection injection: {e}")

if __name__ == "__main__":
    inject_last_reflection()