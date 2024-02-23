# pythonprocessservercheckerbot
This will send a skype message to a contact when a process is active


Change username  and password, as well as your-process with your process name that you want to check ( whether it exists or not)


Update 1.1


Server Checker now uses Windows event scheduling to activate or kill a script whenever a remote connection has been established/stopped.
It can also tell jokes.
Use kill.ps1 and wscript.exe and implement them in your windows scheduler of the server you want to track connections of.
wcript.exe is just a dummy script that I made that runs in the background.
kill.ps1 just kills the process.
