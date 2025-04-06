@echo off
echo ===================================================
echo Fixed ML Chatbot Launcher
echo ===================================================
echo.

REM Use the Python installation that has Flask installed
"C:\Users\Asus\AppData\Local\Programs\Python\Python312\python.exe" fix_chatbot.py

echo.
echo If the server didn't start, press any key to exit.
pause > nul 