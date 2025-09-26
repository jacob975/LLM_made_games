#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試主角造型和可折疊消息列功能的簡單演示
"""

import tkinter as tk
from balance_game_gui import BalanceGameGUI

def main():
    """主函數 - 啟動遊戲並顯示新功能說明"""
    print("🎮 啟動減肥平衡遊戲GUI (新增主角造型功能)")
    print("=" * 50)
    print("✨ 新功能介紹:")
    print("1. 📱 主角造型系統:")
    print("   • 會根據當前健康狀況改變身體顏色")
    print("   • 會根據體重變化調整身體大小") 
    print("   • 會根據快樂程度顯示不同表情")
    print("   • 會根據最後選擇的行動顯示對應配件")
    print("   • 會根據低指數狀態顯示警告標誌")
    print("")
    print("2. 📋 可折疊消息列:")
    print("   • 點擊日誌標題旁的 ▼/▲ 按鈕可折疊/展開")
    print("   • 節省界面空間，讓造型顯示更清楚")
    print("")
    print("3. 🎯 造型變化說明:")
    print("   • 運動 → 紅色頭帶 + 汗珠")
    print("   • 工作 → 領帶")
    print("   • 讀書/學習 → 眼鏡")
    print("   • 聚會 → 派對帽")
    print("   • 烹飪 → 廚師帽")
    print("   • 休息/冥想 → 睡眠符號 (Z)")
    print("")
    print("4. 🎨 狀態指示:")
    print("   • 健康<30 → 🤒 (生病表情)")
    print("   • 快樂<30 → 😢 (難過表情)")
    print("   • 知識>80 → 🎓 (學位帽)")
    print("   • 財富>80 → 💰 (金錢符號)")
    print("")
    print("🚀 正在啟動遊戲...")
    print("=" * 50)
    
    # 啟動GUI
    try:
        game = BalanceGameGUI()
        game.root.mainloop()
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()