import pyperclip

def format_to_markdown(text, context_type, custom_topic=""):
    templates = {
        "1": f"### VS Code Error\n```python\n{text}\n```\nPlease analyze this error.",
        "2": f"### GitHub Discussion\n> {text}\n\nPlease summarize the key points.",
        "3": f"### Website UI Content\n{text}\n\nReview the copy for this layout.",
    }

    if context_type == "custom":
        final_md = f"### Topic: {custom_topic}\n---\n{text}"
    else:
        final_md = templates.get(context_type, text)

    pyperclip.copy(final_md)
    return final_md