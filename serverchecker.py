from skpy import SkypeEventLoop, SkypeNewMessageEvent
import psutil

def is_remote_desktop_active():
    # Check for the tssdis.exe process
    for proc in psutil.process_iter():
        try:
            process = proc.as_dict(attrs=['name'])
            if process['name'] == 'your-process':
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return False

class SkypeServerStatus(SkypeEventLoop):
    def __init__(self, username, password):
        super(SkypeServerStatus, self).__init__(username, password)
    
    def onEvent(self, event):
        if isinstance(event, SkypeNewMessageEvent) and "ping" in event.msg.content:
            event.msg.chat.sendMsg("Pong!")
        
        if isinstance(event, SkypeNewMessageEvent) and event.msg.content == '!server-status':
            if is_remote_desktop_active():
                event.msg.chat.sendMsg("Looks like someone is using the remote desktop")
            else:
                event.msg.chat.sendMsg("No one is using remote desktop")

if __name__ == "__main__":
    skype_bot = SkypeServerStatus("username", "password")
    skype_bot.loop()
