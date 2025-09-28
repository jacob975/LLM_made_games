@echo off
echo Starting Balance Game GUI...
echo.
C:/Users/User/Documents/Github/balance_game/.conda/python.exe balance_game_gui.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error occurred. Press any key to exit...
    pause > nul
)