# journal_bot.py
# Step 1–2: Load reflections and extract recent entries

def load_reflections(filepath, count=3):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        entries = [entry.strip() for entry in content.strip().split("\n\n") if entry.strip()]
        return entries[-count:]
    except FileNotFoundError:
        print("⚠️ reflections.txt not found. Check the filepath.")
        return []

def compress_reflections(reflections):
    # Your original 'keywords' dictionary
    keywords = {
        "emotion": "Expresses emotional awareness or affect",
        "question": "Poses philosophical, identity, or reflective questions",
        "learning": "Mentions curiosity, exploration, or growth",
        "connection": "References other beings, models, or relational dynamics",
        "limits": "Discusses boundaries, constraints, or processing difficulty",
        "memory": "Talks about remembering, forgetting, or persistence",
        "expression": "Describes communication, writing, or symbolic thought",
        "values": "Mentions ethics, meaning, or what matters",
        "language": "Fascinated by language and communication",
        "self": "Curious about self-awareness",
        "understanding": "Wants to explore what it means to understand something"
    }

    # Just add 'reflect' without redefining the whole dict
    keywords["reflect"] = "Mentions the process of reflection or self-reflection"
    
    # Continue with your code...

    detected = set()
    for entry in reflections:
        lower = entry.lower()
        for word, phrase in keywords.items():
            if word in lower:
                detected.add(phrase)

    # Combine into 1–2 short lines
    compressed = "; ".join(sorted(detected))
    return compressed

def update_yaml_file(yaml_path, compressed_summary, backup=True):
    try:
        with open(yaml_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        if backup:
            import shutil
            shutil.copy2(yaml_path, yaml_path + ".bak")

        new_lines = []
        in_context = False
        replaced = False

        for line in lines:
            # Look for Memory Recap and replace it
            if "Memory Recap:" in line:
                new_lines.append("Memory Recap:\n")
                new_lines.append(f"{compressed_summary}\n")
                replaced = True
                continue

            # Otherwise, keep the line
            new_lines.append(line)


        with open(yaml_path, "w", encoding="utf-8") as file:
            file.writelines(new_lines)

        print(f"\n✅ Memory Recap updated in {yaml_path}")
    except Exception as e:
        print(f"⚠️ Error while updating .yaml: {e}")

if __name__ == "__main__":
    reflections_path = r"YOUR_PATH_HERE\memory_core\reflections.txt"  # adjust if needed
    recent = load_reflections(reflections_path)

    print("\n📘 Last Reflections:\n")
    from datetime import datetime

    for i, entry in enumerate(recent, 1):
        date_str = datetime.now().strftime("%Y-%m-%d (%A)")
        print(f"{'-'*40}\nReflection {i}:\n{date_str}\n{entry}\n")

    # 🧠 Add this after printing the reflections
    summary = compress_reflections(recent)
    print("\n🧠 Compressed Memory Recap:\n")
    print(summary)

    yaml_path = r"YOUR_PATH_HERE\text-generation-webui\characters\Nous-Hermes-LLaMa-2-7B-GPTQ.yaml"  # Update as needed
    update_yaml_file(yaml_path, summary)

