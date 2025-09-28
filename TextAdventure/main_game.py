import pygame
import sys
import math
import json
from typing import List, Tuple, Optional, Dict

# 初始化pygame
pygame.init()

# 遊戲常數
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# 顏色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (64, 64, 64)
BLUE = (70, 130, 180)
GREEN = (34, 139, 34)
RED = (178, 34, 34)
YELLOW = (255, 215, 0)
PURPLE = (148, 0, 211)

class Character:
    """角色類別，包含外觀和動畫"""
    
    def __init__(self, char_data: Dict):
        """從JSON數據初始化角色"""
        self.id = char_data["id"]
        self.name = char_data["name"]
        self.display_name = char_data["display_name"]
        self.emoji = char_data["emoji"]
        
        # 顏色設置
        color_data = char_data["color"]
        self.color = (color_data["r"], color_data["g"], color_data["b"])
        self.hex_color = color_data.get("hex", "#000000")
        
        self.description = char_data.get("description", "")
        self.personality = char_data.get("personality", [])
        self.voice_style = char_data.get("voice_style", "normal")
        self.animation_style = char_data.get("animation_style", "pulse")
        self.scale = char_data.get("scale", 1.0)
        self.position_preference = char_data.get("position_preference", "center")
        
        # 動畫相關屬性
        self.animation_offset = 0.0
        self.current_scale = self.scale
        
        # 字體設置
        try:
            self.emoji_font = pygame.font.Font("C:/Windows/Fonts/seguiemj.ttf", 48)
            self.name_font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 16)
        except:
            self.emoji_font = pygame.font.Font(None, 48)
            self.name_font = pygame.font.Font(None, 16)
    
    def update_animation(self, dt: float, animation_settings: Dict):
        """更新角色動畫"""
        anim_config = animation_settings.get(self.animation_style, animation_settings.get("pulse", {}))
        self.animation_offset += dt * anim_config.get("speed", 2.0)
        
        # 根據動畫類型計算縮放
        anim_type = anim_config.get("type", "sine_wave")
        intensity = anim_config.get("intensity", 0.05)
        
        if anim_type == "sine_wave":
            self.current_scale = self.scale + math.sin(self.animation_offset) * intensity
        elif anim_type == "bounce_ease":
            bounce_value = abs(math.sin(self.animation_offset * 2)) * intensity
            self.current_scale = self.scale + bounce_value
        elif anim_type == "smooth_wave":
            self.current_scale = self.scale + math.sin(self.animation_offset * 0.5) * intensity
        elif anim_type == "gentle_pulse":
            self.current_scale = self.scale + math.sin(self.animation_offset * 0.8) * intensity
        elif anim_type == "rapid_shake":
            shake_x = math.sin(self.animation_offset * 10) * intensity
            shake_y = math.cos(self.animation_offset * 10) * intensity
            self.current_scale = self.scale + (shake_x + shake_y) * 0.5
        else:
            self.current_scale = self.scale
    
    def render(self, surface: pygame.Surface, x: int, y: int, is_speaking: bool = False):
        """渲染角色"""
        # 如果正在說話，添加高亮效果
        if is_speaking:
            highlight_radius = int(60 * self.current_scale)
            pygame.draw.circle(surface, (255, 255, 255, 100), (x, y), highlight_radius, 3)
        
        # 繪製角色背景圓形
        radius = int(45 * self.current_scale)
        pygame.draw.circle(surface, self.color, (x, y), radius)
        pygame.draw.circle(surface, WHITE, (x, y), radius, 3)
        
        # 如果正在說話，添加脈衝效果
        if is_speaking:
            pulse_alpha = int(abs(math.sin(self.animation_offset * 3)) * 50)
            pulse_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(pulse_surface, (*self.color, pulse_alpha), (radius, radius), radius)
            surface.blit(pulse_surface, (x - radius, y - radius))
        
        # 渲染emoji
        try:
            emoji_surface = self.emoji_font.render(self.emoji, True, BLACK)
            emoji_rect = emoji_surface.get_rect(center=(x, y - 5))
            surface.blit(emoji_surface, emoji_rect)
        except:
            # 備用方案：顯示角色名稱首字
            text_surface = self.name_font.render(self.display_name[0], True, WHITE)
            text_rect = text_surface.get_rect(center=(x, y))
            surface.blit(text_surface, text_rect)
        
        # 在角色下方顯示名稱
        name_surface = self.name_font.render(self.display_name, True, DARK_GRAY)
        name_rect = name_surface.get_rect(center=(x, y + 65))
        surface.blit(name_surface, name_rect)

class DialogueSystem:
    """對話系統"""
    
    def __init__(self):
        # 字體設置
        try:
            self.dialogue_font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 18)
            self.character_name_font = pygame.font.Font("C:/Windows/Fonts/msjhbd.ttc", 20)
            self.narration_font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 14)
        except:
            self.dialogue_font = pygame.font.Font(None, 18)
            self.character_name_font = pygame.font.Font(None, 20)
            self.narration_font = pygame.font.Font(None, 14)
        
        self.typing_speed = 50  # 字符每秒
        self.current_text = ""
        self.target_text = ""
        self.typing_progress = 0.0
        self.is_typing = False
        
    def start_typing(self, text: str):
        """開始打字機效果"""
        self.target_text = text
        self.current_text = ""
        self.typing_progress = 0.0
        self.is_typing = True
        
    def update(self, dt: float):
        """更新打字機效果"""
        if self.is_typing:
            self.typing_progress += self.typing_speed * dt
            char_count = int(self.typing_progress)
            if char_count >= len(self.target_text):
                self.current_text = self.target_text
                self.is_typing = False
            else:
                self.current_text = self.target_text[:char_count]
    
    def skip_typing(self):
        """跳過打字機效果"""
        if self.is_typing:
            self.current_text = self.target_text
            self.is_typing = False
            return True
        return False
    
    def is_complete(self) -> bool:
        """檢查是否完成打字"""
        return not self.is_typing

class TextAdventureGamePOC:
    """文字冒險遊戲POC主類別"""
    
    def __init__(self):
        # 初始化pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("超神肥 - 文字冒險遊戲 POC")
        self.clock = pygame.time.Clock()
        
        # 載入角色配置
        self.character_config = self.load_character_config("character.json")
        self.characters = self.create_characters_from_config()
        
        # 對話系統
        self.dialogue_system = DialogueSystem()
        
        # 載入劇本
        self.dialogue_lines = self.load_script_json("script.json")
        self.current_line = 0
        self.running = True
        
        # UI區域定義
        self.character_area = pygame.Rect(50, 50, SCREEN_WIDTH - 100, 250)
        self.dialogue_area = pygame.Rect(50, 350, SCREEN_WIDTH - 100, 180)
        self.control_area = pygame.Rect(50, 550, SCREEN_WIDTH - 100, 150)
        
        # 背景顏色
        self.bg_color = (240, 248, 255)  # Alice Blue
        
        # 開始第一句對話
        if self.dialogue_lines:
            self.start_current_dialogue()
    
    def load_character_config(self, filename: str) -> Dict:
        """載入角色配置文件"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"找不到角色配置文件：{filename}，使用預設配置")
            return self.get_default_character_config()
        except json.JSONDecodeError as e:
            print(f"角色配置文件格式錯誤：{e}，使用預設配置")
            return self.get_default_character_config()
    
    def get_default_character_config(self) -> Dict:
        """獲取預設角色配置"""
        return {
            "characters": {
                "narrator": {
                    "id": "narrator", "name": "旁白", "display_name": "旁白", 
                    "emoji": "🎵", "color": {"r": 70, "g": 130, "b": 180}, 
                    "animation_style": "pulse", "scale": 1.0
                },
                "farmer_a": {
                    "id": "farmer_a", "name": "農夫甲", "display_name": "農夫甲", 
                    "emoji": "👨‍🌾", "color": {"r": 34, "g": 139, "b": 34}, 
                    "animation_style": "bounce", "scale": 1.0
                },
                "farmer_b": {
                    "id": "farmer_b", "name": "農婦乙", "display_name": "農婦乙", 
                    "emoji": "👩‍🌾", "color": {"r": 178, "g": 34, "b": 34}, 
                    "animation_style": "sway", "scale": 1.0
                },
                "expert": {
                    "id": "expert", "name": "專家", "display_name": "專家", 
                    "emoji": "👴", "color": {"r": 148, "g": 0, "b": 211}, 
                    "animation_style": "steady", "scale": 1.1
                },
                "chorus": {
                    "id": "chorus", "name": "合唱", "display_name": "合唱", 
                    "emoji": "🎵", "color": {"r": 255, "g": 215, "b": 0}, 
                    "animation_style": "vibrate", "scale": 1.2
                }
            },
            "animation_settings": {
                "pulse": {"speed": 2.0, "intensity": 0.05, "type": "sine_wave"},
                "bounce": {"speed": 1.5, "intensity": 0.08, "type": "bounce_ease"},
                "sway": {"speed": 1.0, "intensity": 0.03, "type": "smooth_wave"},
                "steady": {"speed": 0.5, "intensity": 0.02, "type": "gentle_pulse"},
                "vibrate": {"speed": 3.0, "intensity": 0.1, "type": "rapid_shake"}
            }
        }
    
    def create_characters_from_config(self) -> Dict[str, Character]:
        """從配置創建角色對象"""
        characters = {}
        char_data = self.character_config.get("characters", {})
        
        for char_id, data in char_data.items():
            character = Character(data)
            characters[data["name"]] = character  # 使用中文名稱作為key
            characters[char_id] = character       # 同時使用ID作為key
            
        return characters
    
    def load_script_json(self, filename: str) -> List[Dict]:
        """載入JSON格式的劇本文件"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                script_data = json.load(f)
            
            dialogue_lines = []
            for dialogue in script_data.get("dialogues", []):
                dialogue_lines.append({
                    "character": dialogue["character_name"],
                    "character_id": dialogue.get("character_id", ""),
                    "text": dialogue["text"],
                    "type": dialogue.get("type", "dialogue"),
                    "mood": dialogue.get("mood", "normal"),
                    "emphasis": dialogue.get("emphasis", "normal")
                })
            
            return dialogue_lines
            
        except FileNotFoundError:
            print(f"找不到劇本文件：{filename}，回退到TXT格式")
            return self.load_script_txt("script.txt")
        except json.JSONDecodeError as e:
            print(f"劇本文件格式錯誤：{e}，回退到TXT格式")
            return self.load_script_txt("script.txt")
    
    def load_script_txt(self, filename: str) -> List[Dict]:
        """載入TXT格式的劇本文件（備用方案）"""
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
                
                # 解析角色標識
                if line.startswith('🎵 旁白'):
                    current_character = "旁白"
                    continue
                elif line.startswith('👨‍🌾 農夫甲'):
                    current_character = "農夫甲"
                    continue
                elif line.startswith('👩‍🌾 農婦乙'):
                    current_character = "農婦乙"
                    continue
                elif line.startswith('👴 專家口吻'):
                    current_character = "專家"
                    continue
                elif line.startswith('📢 旁白洗腦式狂喊'):
                    current_character = "旁白"
                    continue
                elif line.startswith('🎵 合唱'):
                    current_character = "合唱"
                    continue
                elif line.startswith('「') and line.endswith('」'):
                    # 對話內容
                    text = line[1:-1]  # 移除引號
                    dialogue_lines.append({
                        "character": current_character,
                        "text": text,
                        "type": "dialogue"
                    })
        
        except FileNotFoundError:
            print(f"找不到劇本文件：{filename}")
            # 創建預設對話
            dialogue_lines = [
                {"character": "旁白", "text": "歡迎來到超神肥的神奇世界！", "type": "dialogue"},
                {"character": "農夫甲", "text": "以前施肥三天累到爆，現在只要撒一把，莊稼自己會Rap！", "type": "dialogue"},
                {"character": "農婦乙", "text": "鄰居看到我家玉米長得比她高三倍，還以為我偷偷養了巨人！", "type": "dialogue"},
                {"character": "專家", "text": "超神肥內含九十九種神秘元素，能讓土壤自帶Wi-Fi，連稻田都能上網！", "type": "dialogue"},
                {"character": "旁白", "text": "超神肥！少撒一點，多收一車！", "type": "dialogue"},
                {"character": "合唱", "text": "超神肥！超神肥！越用越神奇！", "type": "dialogue"}
            ]
        
        return dialogue_lines
    
    def start_current_dialogue(self):
        """開始當前對話的打字機效果"""
        if self.current_line < len(self.dialogue_lines):
            current_dialogue = self.dialogue_lines[self.current_line]
            self.dialogue_system.start_typing(current_dialogue["text"])
    
    def handle_events(self):
        """處理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左鍵點擊
                    if not self.dialogue_system.skip_typing():
                        self.next_dialogue()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.dialogue_system.skip_typing():
                        self.next_dialogue()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    # 重新開始
                    self.current_line = 0
                    self.start_current_dialogue()
    
    def next_dialogue(self):
        """進入下一句對話"""
        if self.current_line < len(self.dialogue_lines) - 1:
            self.current_line += 1
            self.start_current_dialogue()
        else:
            self.show_ending()
    
    def show_ending(self):
        """顯示結局"""
        self.screen.fill(self.bg_color)
        
        # 顯示所有角色
        char_positions = [
            (200, 200), (400, 200), (600, 200), (800, 200), (400, 350)
        ]
        
        for i, (char_name, character) in enumerate(self.characters.items()):
            if i < len(char_positions) and isinstance(character, Character):
                x, y = char_positions[i]
                character.render(self.screen, x, y, False)
        
        # 結局文字
        ending_texts = [
            "感謝您體驗超神肥的神奇世界！",
            "",
            "按 R 重新開始",
            "按 ESC 退出遊戲",
            "點擊滑鼠或按空白鍵重新開始"
        ]
        
        y_start = 450
        for i, text in enumerate(ending_texts):
            if text:
                color = DARK_GRAY if text.startswith("按") or text.startswith("點擊") else BLACK
                text_surface = self.dialogue_system.dialogue_font.render(text, True, color)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_start + i * 25))
                self.screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
        
        # 等待輸入
        waiting = True
        while waiting and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN or \
                     (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    self.current_line = 0
                    self.start_current_dialogue()
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.current_line = 0
                        self.start_current_dialogue()
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        waiting = False
    
    def draw_character_area(self, dt: float):
        """繪製角色顯示區域"""
        # 背景
        pygame.draw.rect(self.screen, LIGHT_GRAY, self.character_area)
        pygame.draw.rect(self.screen, DARK_GRAY, self.character_area, 2)
        
        if self.current_line < len(self.dialogue_lines):
            current_dialogue = self.dialogue_lines[self.current_line]
            speaking_character = current_dialogue["character"]
            
            # 獲取動畫設置
            animation_settings = self.character_config.get("animation_settings", {})
            
            # 更新所有角色動畫
            for character in self.characters.values():
                if isinstance(character, Character):
                    character.update_animation(dt, animation_settings)
            
            # 顯示當前說話的角色在中央
            if speaking_character in self.characters:
                character = self.characters[speaking_character]
                center_x = self.character_area.centerx
                center_y = self.character_area.centery - 20
                character.render(self.screen, center_x, center_y, True)
                
                # 在左右兩側顯示其他角色（較小）
                other_chars = [name for name in self.characters.keys() 
                              if name != speaking_character and isinstance(self.characters[name], Character)]
                positions = [(150, center_y), (SCREEN_WIDTH - 150, center_y)]
                
                for i, char_name in enumerate(other_chars[:2]):
                    if i < len(positions):
                        x, y = positions[i]
                        char = self.characters[char_name]
                        original_scale = char.current_scale
                        char.current_scale *= 0.7  # 縮小非主要角色
                        char.render(self.screen, x, y, False)
                        char.current_scale = original_scale  # 恢復縮放
    
    def draw_dialogue_area(self):
        """繪製對話區域"""
        # 背景
        pygame.draw.rect(self.screen, WHITE, self.dialogue_area)
        pygame.draw.rect(self.screen, DARK_GRAY, self.dialogue_area, 2)
        
        if self.current_line < len(self.dialogue_lines):
            current_dialogue = self.dialogue_lines[self.current_line]
            speaking_character = current_dialogue["character"]
            
            # 角色名稱
            if speaking_character in self.characters:
                character = self.characters[speaking_character]
                name_surface = self.dialogue_system.character_name_font.render(
                    character.display_name, True, character.color
                )
                self.screen.blit(name_surface, (self.dialogue_area.x + 15, self.dialogue_area.y + 15))
            
            # 對話內容 - 支持自動換行
            text_area = pygame.Rect(
                self.dialogue_area.x + 15,
                self.dialogue_area.y + 45,
                self.dialogue_area.width - 30,
                self.dialogue_area.height - 60
            )
            
            self.render_wrapped_text(
                self.dialogue_system.current_text,
                text_area,
                self.dialogue_system.dialogue_font,
                BLACK
            )
    
    def render_wrapped_text(self, text: str, rect: pygame.Rect, font: pygame.font.Font, color: Tuple[int, int, int]):
        """渲染自動換行的文字"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] > rect.width:
                if current_line:
                    lines.append(current_line.strip())
                    current_line = word + " "
                else:
                    lines.append(word)
                    current_line = ""
            else:
                current_line = test_line
        
        if current_line:
            lines.append(current_line.strip())
        
        # 渲染每一行
        line_height = font.get_height() + 2
        for i, line in enumerate(lines):
            if i * line_height < rect.height - line_height:
                text_surface = font.render(line, True, color)
                self.screen.blit(text_surface, (rect.x, rect.y + i * line_height))
    
    def draw_control_area(self):
        """繪製控制區域"""
        # 背景
        pygame.draw.rect(self.screen, LIGHT_GRAY, self.control_area)
        pygame.draw.rect(self.screen, DARK_GRAY, self.control_area, 1)
        
        # 控制提示
        controls = [
            "🖱️ 點擊滑鼠 - 繼續對話",
            "⏸️ 空白鍵 - 繼續對話",
            "🔄 R鍵 - 重新開始",
            "❌ ESC鍵 - 退出遊戲"
        ]
        
        y_start = self.control_area.y + 15
        for i, control in enumerate(controls):
            text_surface = self.dialogue_system.narration_font.render(control, True, DARK_GRAY)
            self.screen.blit(text_surface, (self.control_area.x + 15, y_start + i * 20))
        
        # 進度指示
        progress_text = f"對話進度: {self.current_line + 1} / {len(self.dialogue_lines)}"
        progress_surface = self.dialogue_system.narration_font.render(progress_text, True, BLUE)
        progress_rect = progress_surface.get_rect()
        progress_rect.topright = (self.control_area.right - 15, y_start)
        self.screen.blit(progress_surface, progress_rect)
        
        # 打字狀態指示
        if self.dialogue_system.is_typing:
            typing_text = "⏳ 正在顯示文字..."
            typing_surface = self.dialogue_system.narration_font.render(typing_text, True, GREEN)
            typing_rect = typing_surface.get_rect()
            typing_rect.bottomright = (self.control_area.right - 15, self.control_area.bottom - 15)
            self.screen.blit(typing_surface, typing_rect)
        else:
            continue_text = "✅ 點擊繼續"
            continue_surface = self.dialogue_system.narration_font.render(continue_text, True, BLUE)
            continue_rect = continue_surface.get_rect()
            continue_rect.bottomright = (self.control_area.right - 15, self.control_area.bottom - 15)
            self.screen.blit(continue_surface, continue_rect)
    
    def run(self):
        """主遊戲循環"""
        last_time = pygame.time.get_ticks()
        
        while self.running:
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 1000.0
            last_time = current_time
            
            # 處理事件
            self.handle_events()
            
            # 更新
            self.dialogue_system.update(dt)
            
            # 渲染
            self.screen.fill(self.bg_color)
            self.draw_character_area(dt)
            self.draw_dialogue_area()
            self.draw_control_area()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("正在啟動超神肥文字冒險遊戲POC...")
    print("優先載入JSON格式劇本和角色配置")
    
    try:
        game = TextAdventureGamePOC()
        game.run()
    except Exception as e:
        print(f"遊戲啟動失敗: {e}")
        input("按Enter鍵退出...")