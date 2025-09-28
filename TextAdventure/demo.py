"""
超神肥文字冒險遊戲 - 快速演示
這個腳本會啟動遊戲並自動演示幾秒鐘，然後退出
"""

import pygame
import sys
import time
from main_game import TextAdventureGamePOC

class DemoGame(TextAdventureGamePOC):
    """演示版遊戲，自動播放"""
    
    def __init__(self):
        super().__init__()
        self.demo_start_time = time.time()
        self.demo_duration = 10  # 演示10秒
        self.auto_advance_time = 2.0  # 每2秒自動前進
        self.last_advance_time = time.time()
        
    def handle_events(self):
        """覆寫事件處理，添加自動播放邏輯"""
        current_time = time.time()
        
        # 自動前進對話
        if current_time - self.last_advance_time > self.auto_advance_time:
            if not self.dialogue_system.skip_typing():
                self.next_dialogue()
            self.last_advance_time = current_time
        
        # 檢查是否應該結束演示
        if current_time - self.demo_start_time > self.demo_duration:
            print("\n演示完成！")
            self.running = False
            return
        
        # 處理退出事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # 手動前進
                    if not self.dialogue_system.skip_typing():
                        self.next_dialogue()
    
    def show_ending(self):
        """簡化的結局顯示"""
        print("演示遊戲已完成所有對話！")
        time.sleep(1)
        self.running = False

def main():
    print("=== 超神肥文字冒險遊戲 - 快速演示 ===")
    print("這個演示會自動播放遊戲內容，持續約10秒")
    print("您可以按ESC鍵提前退出")
    print("按空白鍵可以手動控制對話")
    print("演示開始...\n")
    
    try:
        demo = DemoGame()
        demo.run()
        print("\n演示成功完成！")
        print("要體驗完整遊戲，請運行：python main_game.py")
        
    except Exception as e:
        print(f"演示運行出錯：{e}")
        print("請檢查pygame是否正確安裝")
    
    print("\n演示結束")

if __name__ == "__main__":
    main()