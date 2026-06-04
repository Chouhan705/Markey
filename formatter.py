import pyperclip

def format_to_markdown(text, context_type, custom_topic=""):
    templates = {
        "1": f"### VS Code Error\n**Context:** Debugging code error\n```python\n{text}\n```\n**Request:** Please explain this error and suggest a fix.",
        "2": f"### GitHub Discussion\n**Context:** Repository/PR feedback\n> {text}\n\n**Request:** Summarize the main points of this discussion.",
        "3": f"### Website UI/UX\n**Context:** Frontend Preview\n- **Extracted Content:** {text}\n\n**Request:** Review the copy and layout logic of this UI.",
    }

    if context_type == "custom":
        final_md = f"### Topic: {custom_topic}\n---\n{text}\n---\n**Request:** Analyze the content above."
    else:
        final_md = templates.get(context_type, text)

    # Put the final Markdown back into the clipboard
    pyperclip.copy(final_md)
    return final_md