import winrt.windows.ui.notifications as notifications
import winrt.windows.data.xml.dom as dom

def show_toast(title, message):
    """ Displays a native Windows Toast notification banner """
    try:
        # Get standard Toast template type
        template = notifications.ToastNotificationManager.get_template_content(
            notifications.ToastTemplateType.TOAST_TEXT02
        )
        
        # Populate XML text node fields
        text_nodes = template.get_elements_by_tag_name("text")
        text_nodes.item(0).append_child(template.create_text_node(title))
        text_nodes.item(1).append_child(template.create_text_node(message))
        
        # Raise execution notification to desktop
        notifier = notifications.ToastNotificationManager.create_toast_notifier("Markey")
        toast = notifications.ToastNotification(template)
        notifier.show(toast)
    except Exception as e:
        print(f"[TOAST ERROR] Failed to display notification system: {e}")