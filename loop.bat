@echo off
cd C:\Users\RandomGuy90\Desktop\qr-reader\pyimagecamera
:loop
Start python.exe run.py | set /P "="
goto loop