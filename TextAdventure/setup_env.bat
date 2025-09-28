@echo off
echo =================================
echo 超神肥文字冒險遊戲 - 環境設置
echo =================================
echo.

REM 檢查conda是否存在
conda --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 錯誤: 未找到conda，請先安裝Anaconda或Miniconda
    pause
    exit /b 1
)

echo 正在創建conda環境 text_adv...
conda create -n text_adv python=3.11 -y
if %errorlevel% neq 0 (
    echo 錯誤: 創建conda環境失敗
    pause
    exit /b 1
)

echo.
echo 正在啟動text_adv環境並安裝依賴...
call conda activate text_adv
conda run -n text_adv pip install pygame pillow numpy

echo.
echo 檢查安裝結果...
conda run -n text_adv python -c "import pygame; print('pygame版本:', pygame.version.ver)"
conda run -n text_adv python -c "import PIL; print('Pillow安裝成功')"
conda run -n text_adv python -c "import numpy; print('numpy安裝成功')"

echo.
echo =================================
echo 環境設置完成！
echo =================================
echo.
echo 使用方法:
echo 1. conda activate text_adv
echo 2. python main_game.py
echo.
echo 或者直接運行 run_game.bat
echo.
pause