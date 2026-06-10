import pyperclip
from config_manager import load_config

def format_to_markdown(text, context_type, custom_topic=""):
    # Pull dynamic settings configured by the user from AppData JSON store
    config = load_config()
    templates = config.get("templates", {})

    if context_type == "custom":
        final_md = f"### Topic: {custom_topic}\n---\n{text}"
    else:
        # Pull the specific layout selection and swap placeholder token
        raw_template = templates.get(context_type, "{text}")
        if "{text}" in raw_template:
            final_md = raw_template.replace("{text}", text)
        else:
            final_md = f"{raw_template}\n\n{text}"

    pyperclip.copy(final_md)
    return final_md