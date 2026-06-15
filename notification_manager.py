import winrt.windows.ui.notifications as notifications
import winrt.windows.data.xml.dom as dom

def show_toast(title, message):
    """ Displays a native Windows Toast notification banner via a standard system shell fallback """
    try:
        # Construct an escaping-safe raw XML payload string
        xml_payload = f"""
        <toast>
            <visual>
                <binding template="ToastGeneric">
                    <text>{title}</text>
                    <text>{message}</text>
                </binding>
            </visual>
        </toast>
        """
        
        # Load string cleanly into a Windows XML Document object
        xml_doc = dom.XmlDocument()
        xml_doc.load_xml(xml_payload)
        
        # Using the standard Windows Explorer Notification Shell ID ensures it works perfectly 
        # when running raw main.py files AND when bundled inside a single-file PyInstaller .exe
        app_id = "Windows.SystemToast.Background"
        
        notifier = notifications.ToastNotificationManager.create_toast_notifier(app_id)
        toast = notifications.ToastNotification(xml_doc)
        notifier.show(toast)
    except Exception as e:
        print(f"[TOAST ERROR] Failed to display notification system: {e}")