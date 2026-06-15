import pyperclip
import re
from config_manager import load_config

def detect_code_language(text):
    """
    Scans code text signatures to determine the programming language.
    Returns the markdown fence identifier string.
    """
    # Clean up white spaces for uniform line evaluations
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    combined = " ".join(lines)

    # 1. Python Signatures
    if any(line.startswith(("def ", "import ", "from ", "class ")) for line in lines) or "if __name__ ==" in combined or "print(" in combined:
        if ":" in combined and ("elif " in combined or "pass" in combined or "lambda " in combined):
            return "python"

    # 2. JavaScript / TypeScript Signatures
    if any(line.startswith(("const ", "let ", "import ", "export ", "function ")) for line in lines) or "console.log" in combined or "=>" in combined:
        return "javascript"

    # 3. C++ / C / Java Signatures
    if "#include" in combined or "using namespace std" in combined or "std::" in combined:
        return "cpp"
    if "public class " in combined and "public static void main" in combined:
        return "java"

    # 4. HTML / XML
    if "</" in combined or "<html" in combined or "<div>" in combined:
        return "html"

    # 5. CSS
    if "{" in combined and "}" in combined and any(x in combined for x in [";", "margin:", "padding:", "color:"]):
        if not any(x in combined for x in ["function", "const", "def"]):
            return "css"

    # Default fallback to plain text if syntax is ambiguous
    return "text"

def format_to_markdown(text, context_type, custom_topic=""):
    config = load_config()
    templates = config.get("templates", {})

    if context_type == "custom":
        final_md = f"### Topic: {custom_topic}\n---\n{text}"
    else:
        raw_template = templates.get(context_type, "{text}")
        
        # Look specifically at the VS Code Error / Code block selection
        if context_type == "1":
            detected_lang = detect_code_language(text)
            # Dynamically substitute placeholder block wrappers if they exist
            if "```python" in raw_template:
                raw_template = raw_template.replace("```python", f"```{detected_lang}")
            elif "```" in raw_template:
                # If user removed 'python' but left the tick boxes, match it
                raw_template = re.sub(r'```\w*', f"```{detected_lang}", raw_template)

        if "{text}" in raw_template:
            final_md = raw_template.replace("{text}", text)
        else:
            final_md = f"{raw_template}\n\n{text}"

    pyperclip.copy(final_md)
    return final_md