import pygame
import sys
import re
from typing import List, Tuple, Optional
import json

# 初始化pygame
pygame.init()

# 設置遊戲常數
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# 顏色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 100, 200)
GREEN = (0, 150, 0)
RED = (200, 50, 50)
YELLOW = (255, 255, 0)

class Character:
    """角色類別"""
    def __init__(self, name: str, emoji: str, color: Tuple[int, int, int]):
        self.name = name
        self.emoji = emoji
        self.color = color
        self.font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 24)  # 使用微軟正黑體
        
    def render_character(self, surface: pygame.Surface, x: int, y: int):
        """渲染角色外觀"""
        # 繪製角色背景圓形
        pygame.draw.circle(surface, self.color, (x + 40, y + 40), 35)
        pygame.draw.circle(surface, WHITE, (x + 40, y + 40), 35, 3)
        
        # 渲染emoji
        try:
            emoji_surface = self.font.render(self.emoji, True, WHITE)
            emoji_rect = emoji_surface.get_rect(center=(x + 40, y + 40))
            surface.blit(emoji_surface, emoji_rect)
        except:
            # 如果emoji渲染失敗，顯示名字首字
            text_surface = self.font.render(self.name[0], True, WHITE)
            text_rect = text_surface.get_rect(center=(x + 40, y + 40))
            surface.blit(text_surface, text_rect)

class DialogueLine:
    """對話行類別"""
    def __init__(self, character: Optional[Character], text: str, line_type: str = "dialogue"):
        self.character = character
        self.text = text
        self.line_type = line_type  # "dialogue", "narration", "chorus"

class TextAdventureGame:
    """文字冒險遊戲主類別"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("超神肥 文字冒險遊戲")
        self.clock = pygame.time.Clock()
        
        # 字體設置
        try:
            self.dialogue_font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 20)
            self.character_name_font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 18)
            self.narration_font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 16)
        except:
            self.dialogue_font = pygame.font.Font(None, 20)
            self.character_name_font = pygame.font.Font(None, 18)
            self.narration_font = pygame.font.Font(None, 16)
            
        # 初始化角色
        self.characters = {
            "旁白": Character("旁白", "🎵", BLUE),
            "農夫甲": Character("農夫甲", "👨‍🌾", GREEN),
            "農婦乙": Character("農婦乙", "👩‍🌾", RED),
            "專家": Character("專家", "👴", GRAY),
            "合唱": Character("合唱", "🎵", YELLOW)
        }
        
        # 載入劇本
        self.dialogue_lines = self.load_script("script.txt")
        self.current_line = 0
        self.running = True
        
        # UI元素
        self.dialogue_box_rect = pygame.Rect(50, SCREEN_HEIGHT - 200, SCREEN_WIDTH - 100, 150)
        self.character_display_rect = pygame.Rect(50, 50, SCREEN_WIDTH - 100, 200)
        
    def load_script(self, filename: str) -> List[DialogueLine]:
        """載入並解析劇本文件"""
        dialogue_lines = []
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                
            lines = content.split('\n')
            current_character = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # 解析不同類型的行
                if line.startswith('🎵 旁白'):
                    current_character = self.characters["旁白"]
                    continue
                elif line.startswith('👨‍🌾 農夫甲'):
                    current_character = self.characters["農夫甲"]
                    continue
                elif line.startswith('👩‍🌾 農婦乙'):
                    current_character = self.characters["農婦乙"]
                    continue
                elif line.startswith('👴 專家口吻'):
                    current_character = self.characters["專家"]
                    continue
                elif line.startswith('📢 旁白洗腦式狂喊'):
                    current_character = self.characters["旁白"]
                    continue
                elif line.startswith('🎵 合唱'):
                    current_character = self.characters["合唱"]
                    continue
                elif line.startswith('「') and line.endswith('」'):
                    # 對話內容
                    text = line[1:-1]  # 移除引號
                    dialogue_lines.append(DialogueLine(current_character, text, "dialogue"))
                    
        except FileNotFoundError:
            print(f"找不到劇本文件：{filename}")
            # 創建一個預設對話
            dialogue_lines.append(DialogueLine(self.characters["旁白"], "歡迎來到超神肥的世界！", "dialogue"))
            dialogue_lines.append(DialogueLine(self.characters["農夫甲"], "準備好體驗神奇的農業革命了嗎？", "dialogue"))
            
        return dialogue_lines
    
    def draw_dialogue_box(self):
        """繪製對話框"""
        # 繪製對話框背景
        pygame.draw.rect(self.screen, WHITE, self.dialogue_box_rect)
        pygame.draw.rect(self.screen, BLACK, self.dialogue_box_rect, 3)
        
        if self.current_line < len(self.dialogue_lines):
            current_dialogue = self.dialogue_lines[self.current_line]
            
            # 顯示角色名稱
            if current_dialogue.character:
                name_surface = self.character_name_font.render(
                    current_dialogue.character.name, True, current_dialogue.character.color
                )
                self.screen.blit(name_surface, (self.dialogue_box_rect.x + 10, self.dialogue_box_rect.y + 10))
                
                # 顯示對話內容
                text_y = self.dialogue_box_rect.y + 40
                words = current_dialogue.text.split()
                lines = []
                current_line_text = ""
                
                for word in words:
                    test_line = current_line_text + word + " "
                    if self.dialogue_font.size(test_line)[0] > self.dialogue_box_rect.width - 40:
                        if current_line_text:
                            lines.append(current_line_text.strip())
                            current_line_text = word + " "
                        else:
                            lines.append(word)
                            current_line_text = ""
                    else:
                        current_line_text = test_line
                        
                if current_line_text:
                    lines.append(current_line_text.strip())
                
                for i, text_line in enumerate(lines[:4]):  # 最多顯示4行
                    text_surface = self.dialogue_font.render(text_line, True, BLACK)
                    self.screen.blit(text_surface, (self.dialogue_box_rect.x + 10, text_y + i * 25))
                    
        # 顯示繼續提示
        hint_text = "點擊滑鼠繼續..."
        hint_surface = self.narration_font.render(hint_text, True, GRAY)
        hint_rect = hint_surface.get_rect()
        hint_rect.bottomright = (self.dialogue_box_rect.right - 10, self.dialogue_box_rect.bottom - 10)
        self.screen.blit(hint_surface, hint_rect)
    
    def draw_character_display(self):
        """繪製角色顯示區域"""
        # 繪製背景
        pygame.draw.rect(self.screen, LIGHT_GRAY, self.character_display_rect)
        pygame.draw.rect(self.screen, BLACK, self.character_display_rect, 2)
        
        if self.current_line < len(self.dialogue_lines):
            current_dialogue = self.dialogue_lines[self.current_line]
            if current_dialogue.character:
                # 在中央顯示當前說話的角色
                char_x = self.character_display_rect.centerx - 40
                char_y = self.character_display_rect.centery - 40
                current_dialogue.character.render_character(self.screen, char_x, char_y)
    
    def handle_events(self):
        """處理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左鍵點擊
                    self.next_dialogue()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_dialogue()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def next_dialogue(self):
        """進入下一句對話"""
        if self.current_line < len(self.dialogue_lines) - 1:
            self.current_line += 1
        else:
            # 遊戲結束
            self.show_ending()
    
    def show_ending(self):
        """顯示結局畫面"""
        self.screen.fill(BLACK)
        
        ending_texts = [
            "感謝您體驗超神肥的神奇世界！",
            "",
            "按ESC鍵退出遊戲",
            "或點擊滑鼠重新開始"
        ]
        
        y_offset = SCREEN_HEIGHT // 2 - 50
        for text in ending_texts:
            if text:
                text_surface = self.dialogue_font.render(text, True, WHITE)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                self.screen.blit(text_surface, text_rect)
            y_offset += 40
        
        pygame.display.flip()
        
        # 等待用戶輸入
        waiting = True
        while waiting and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.current_line = 0  # 重新開始
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        waiting = False
    
    def run(self):
        """主遊戲循環"""
        while self.running:
            self.handle_events()
            
            # 繪製畫面
            self.screen.fill(BLACK)
            self.draw_character_display()
            self.draw_dialogue_box()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = TextAdventureGame()
    game.run()