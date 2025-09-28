@echo off
echo Starting Config Manager...
echo.
C:/Users/User/Documents/Github/balance_game/.conda/python.exe config_manager.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error occurred. Press any key to exit...
    pause > nul
)