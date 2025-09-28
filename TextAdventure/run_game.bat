@echo off
echo 正在啟動超神肥文字冒險遊戲...

REM 檢查conda環境是否存在
conda info --envs | findstr "text_adv" >nul
if %errorlevel% neq 0 (
    echo 錯誤: text_adv環境不存在，請先運行 setup_env.bat
    pause
    exit /b 1
)

REM 啟動遊戲（JSON版本）
echo 使用JSON格式劇本啟動遊戲...
conda run -n text_adv python main_game.py

if %errorlevel% neq 0 (
    echo.
    echo 遊戲運行出現錯誤，嘗試基礎版本...
    conda run -n text_adv python game.py
)

pause