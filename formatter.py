import pyperclip
import re
from config_manager import load_config

def detect_code_language(text):
    """ Scans text signatures for programming languages """
    # Strip layout headers out to look at clean characters
    clean_lines = [re.sub(r'^#+\s*', '', line).strip() for line in text.split("\n")]
    combined = " ".join(clean_lines)

    # Common programming keywords
    if any(line.startswith(("def ", "import ", "from ", "class ", "print(")) for line in clean_lines) or "==" in combined or "def " in combined:
        return "python"
    if any(line.startswith(("const ", "let ", "function ")) for line in clean_lines) or "console.log" in combined or "=>" in combined:
        return "javascript"
    if "#include" in combined or "std::" in combined:
        return "cpp"
    
    return None

def format_to_markdown(text, context_type, custom_topic=""):
    config = load_config()
    templates = config.get("templates", {})

    topic_lower = custom_topic.lower()
    
    # 1. Run our signature engine over the text body to verify if it's code
    detected_lang = detect_code_language(text)
    
    # 2. Check if the context choice or the text scan indicates programming code
    is_code_context = (
        context_type == "1" or 
        "code" in topic_lower or 
        topic_lower in ["python", "js", "javascript", "cpp", "c++", "java", "html", "css"] or
        detected_lang is not None
    )

    # If the fallback scan caught code but the custom topic didn't specify the language
    if detected_lang is None and is_code_context:
        detected_lang = "text"

    if is_code_context:
        # Clean out all visual layout tracking hashes (#) assigned by the OCR height scanner
        lines_clean = []
        for line in text.split("\n"):
            cleaned = re.sub(r'^#+\s*', '', line)
            lines_clean.append(cleaned)
        text = "\n".join(lines_clean)

    if context_type == "custom":
        if is_code_context:
            final_md = f"### Topic: {custom_topic}\n---\n```{detected_lang or 'text'}\n{text}\n```"
        else:
            final_md = f"### Topic: {custom_topic}\n---\n{text}"
    else:
        raw_template = templates.get(context_type, "{text}")
        
        if context_type == "1":
            if "```python" in raw_template:
                raw_template = raw_template.replace("```python", f"```{detected_lang}")
            elif "```" in raw_template:
                raw_template = re.sub(r'```\w*', f"```{detected_lang}", raw_template)

        if "{text}" in raw_template:
            final_md = raw_template.replace("{text}", text)
        else:
            final_md = f"{raw_template}\n\n{text}"

    pyperclip.copy(final_md)
    return final_md