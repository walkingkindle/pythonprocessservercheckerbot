import datetime
import random
import time
import psutil
import threading
from skpy import SkypeEventLoop, SkypeNewMessageEvent


PROCESSNAME = "processnames"


def tell_me_a_joke():
    with open('jokes.txt', "r") as jokes:
        jokes_content = jokes.readlines()
        jokeslist = [x for x in jokes_content]
        return random.choice(jokeslist)


def is_remote_desktop_active():
    # Check if wscript.exe process is running
    for proc in psutil.process_iter():
        try:
            process = proc.as_dict(attrs=['name'])
            if process['name'] == PROCESSNAME:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def check_for_remote_desktop(chat):
    notified = False  # Flag to track if notification has been sent
    while True:
        is_active = is_remote_desktop_active()
        if not is_active:
            if not notified:
                chat.sendMsg(f"Hey! The server is free to use!")
                notified = True
        else:
            notified = False  # Reset the flag if the remote desktop becomes active again
        time.sleep(5)

def get_process_creation_time(process_name):
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        if proc.info['name'] == process_name:
            return proc.info['create_time']
    return None


def calculate_duration_since_creation(creation_time):
    current_time = datetime.datetime.now().timestamp()
    duration_seconds = current_time - creation_time
    duration_minutes = duration_seconds / 60
    duration_hours = duration_minutes / 60
    return round(duration_hours, 2)


class SkypeServerStatus(SkypeEventLoop):
    def __init__(self, username, password):
        super(SkypeServerStatus, self).__init__(username, password)

    def onEvent(self, event):
        if isinstance(event, SkypeNewMessageEvent) and event.msg.content.lower() == 'ping':
            event.msg.chat.sendMsg("Pong!")

        if isinstance(event, SkypeNewMessageEvent) and event.msg.content.lower() == 'status':
            if is_remote_desktop_active():
                event.msg.chat.sendMsg("Looks like someone is using the remote desktop")
                process_creation_time = get_process_creation_time(PROCESSNAME)
                if process_creation_time is not None:
                    event.msg.chat.sendMsg(
                        f"The current Remote Desktop session has been going on for {calculate_duration_since_creation(process_creation_time)} hours.")
            else:
                event.msg.chat.sendMsg("No one is using remote desktop")
        if isinstance(event, SkypeNewMessageEvent) and event.msg.content.lower() == 'joke':
            joke = tell_me_a_joke()
            event.msg.chat.sendMsg(joke)
        if isinstance(event, SkypeNewMessageEvent) and event.msg.content.lower() == 'notify-me':
            event.msg.chat.sendMsg("Okay, I will notify you when the server is disconnected")
            threading.Thread(target=check_for_remote_desktop, args=(event.msg.chat)).start()
        if isinstance(event, SkypeNewMessageEvent) and event.msg.content.lower() == 'commands':
            event.msg.chat.sendMsg(f"Hey!\nPlease find the list of commands below: \n"
                            "ping= See if I'm alive.\n"
                            "joke = Hear a hilarious joke about servers.\n"
                            "status = I will tell you if the remote is being used by someone currently and for how long.\n"
                            "notify-me = I will notify you when the remote is free for you to use!")




if __name__ == "__main__":
    skype_bot = SkypeServerStatus("yourskypemail", "password")
    skype_bot.loop()
