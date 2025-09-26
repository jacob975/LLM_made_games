#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Balance Game - 減肥平衡遊戲
一個終端遊戲，讓玩家扮演一個人，透過每天的行動來平衡各項指數，最終達到減肥目標。
"""

import random
import json
import os
from typing import Dict, List, Tuple, Optional

class Character:
    """遊戲角色類別"""
    
    def __init__(self, name: str):
        self.name = name
        self.day = 1
        self.stats = {
            'weight': 80.0,      # 體重 (kg)
            'health': 50,        # 健康 (0-100)
            'happiness': 50,     # 快樂 (0-100)
            'wealth': 50,        # 財富 (0-100)
            'knowledge': 50,     # 知識 (0-100)
            'social': 50         # 社交 (0-100)
        }
        self.target_weight = 65.0  # 目標體重
        self.initial_weight = 80.0
        self.events_log = []
        
    def update_stats(self, changes: Dict[str, float]):
        """更新角色狀態"""
        for stat, change in changes.items():
            if stat == 'weight':
                self.stats[stat] += change
                # 體重不能低於40kg或高於150kg
                self.stats[stat] = max(40.0, min(150.0, self.stats[stat]))
            else:
                self.stats[stat] += change
                # 其他指數範圍0-100
                self.stats[stat] = max(0, min(100, self.stats[stat]))
    
    def get_status(self) -> str:
        """根據各項指數獲取角色狀態描述"""
        weight_progress = ((self.initial_weight - self.stats['weight']) / 
                          (self.initial_weight - self.target_weight)) * 100
        
        status_parts = []
        
        # 體重狀態
        if weight_progress >= 100:
            status_parts.append("🎉 恭喜！已達到目標體重！")
        elif weight_progress >= 75:
            status_parts.append("💪 離目標很近了！")
        elif weight_progress >= 50:
            status_parts.append("👍 減肥進度良好")
        elif weight_progress >= 25:
            status_parts.append("📈 有些進步")
        else:
            status_parts.append("😅 還需要努力")
        
        # 健康狀態
        if self.stats['health'] >= 80:
            status_parts.append("身體很健康")
        elif self.stats['health'] >= 60:
            status_parts.append("身體狀況良好")
        elif self.stats['health'] >= 40:
            status_parts.append("身體狀況普通")
        elif self.stats['health'] >= 20:
            status_parts.append("身體狀況不佳")
        else:
            status_parts.append("身體很虛弱")
        
        return "，".join(status_parts)
    
    def check_win_condition(self) -> Optional[str]:
        """檢查勝利或失敗條件"""
        if self.stats['weight'] <= self.target_weight:
            return "win"
        
        # 失敗條件
        if self.stats['health'] <= 10:
            return "lose_health"
        if self.stats['happiness'] <= 10:
            return "lose_depression"
        if self.day > 100:  # 100天內沒達成目標
            return "lose_time"
        
        return None

class Action:
    """行動類別"""
    
    def __init__(self, name: str, description: str, effects: Dict[str, float], 
                 energy_cost: int = 10):
        self.name = name
        self.description = description
        self.effects = effects
        self.energy_cost = energy_cost

class BalanceGame:
    """遊戲主類別"""
    
    def __init__(self):
        self.character = None
        self.actions = self._init_actions()
        self.save_file = "balance_game_save.json"
        
    def _init_actions(self) -> List[Action]:
        """初始化所有可用行動"""
        return [
            Action(
                "運動", 
                "去健身房運動1小時",
                {'weight': -0.5, 'health': 8, 'happiness': -3}
            ),
            Action(
                "慢跑", 
                "在公園慢跑30分鐘",
                {'weight': -0.3, 'health': 5, 'happiness': 2, 'social': 1}
            ),
            Action(
                "讀書", 
                "閱讀一本好書",
                {'knowledge': 6, 'happiness': 3, 'social': -2}
            ),
            Action(
                "工作", 
                "努力工作賺錢",
                {'wealth': 8, 'health': -4, 'happiness': -2, 'weight': 0.2}
            ),
            Action(
                "聚會", 
                "和朋友聚會聊天",
                {'social': 8, 'happiness': 5, 'wealth': -3, 'weight': 0.3}
            ),
            Action(
                "休息", 
                "在家放鬆休息",
                {'happiness': 6, 'health': 3, 'knowledge': -1}
            ),
            Action(
                "烹飪", 
                "自己做健康料理",
                {'health': 4, 'happiness': 3, 'wealth': -2, 'weight': -0.2}
            ),
            Action(
                "冥想", 
                "進行正念冥想",
                {'happiness': 7, 'health': 2, 'knowledge': 2}
            ),
            Action(
                "購物", 
                "去商場購物",
                {'happiness': 4, 'wealth': -5, 'social': 2, 'weight': 0.1}
            ),
            Action(
                "學習", 
                "參加線上課程",
                {'knowledge': 8, 'wealth': -1, 'happiness': 1}
            )
        ]
    
    def start_new_game(self):
        """開始新遊戲"""
        print("=" * 50)
        print("🏃‍♂️ 歡迎來到減肥平衡遊戲！ 🏃‍♀️")
        print("=" * 50)
        
        name = input("請輸入您的角色名字: ").strip()
        if not name:
            name = "減肥勇者"
        
        self.character = Character(name)
        print(f"\n歡迎 {name}！")
        print(f"目標：從 {self.character.initial_weight}kg 減重到 {self.character.target_weight}kg")
        print("每天選擇一個行動，平衡各項指數，在100天內達成減肥目標！")
        
        self.game_loop()
    
    def load_game(self) -> bool:
        """載入遊戲"""
        if not os.path.exists(self.save_file):
            return False
        
        try:
            with open(self.save_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.character = Character(data['name'])
            self.character.day = data['day']
            self.character.stats = data['stats']
            self.character.target_weight = data['target_weight']
            self.character.initial_weight = data['initial_weight']
            self.character.events_log = data.get('events_log', [])
            
            print(f"遊戲已載入！歡迎回來，{self.character.name}！")
            return True
            
        except Exception as e:
            print(f"載入遊戲失敗: {e}")
            return False
    
    def save_game(self):
        """儲存遊戲"""
        if not self.character:
            return
        
        data = {
            'name': self.character.name,
            'day': self.character.day,
            'stats': self.character.stats,
            'target_weight': self.character.target_weight,
            'initial_weight': self.character.initial_weight,
            'events_log': self.character.events_log
        }
        
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("遊戲已儲存！")
        except Exception as e:
            print(f"儲存遊戲失敗: {e}")
    
    def display_character_stats(self):
        """顯示角色狀態"""
        print("\n" + "=" * 50)
        print(f"📅 第 {self.character.day} 天 - {self.character.name} 的狀態")
        print("=" * 50)
        
        # 計算減肥進度
        weight_lost = self.character.initial_weight - self.character.stats['weight']
        target_loss = self.character.initial_weight - self.character.target_weight
        progress = (weight_lost / target_loss) * 100 if target_loss > 0 else 0
        
        print(f"🏋️  體重: {self.character.stats['weight']:.1f}kg "
              f"(目標: {self.character.target_weight}kg, 進度: {progress:.1f}%)")
        
        # 顯示其他指數
        stats_display = [
            ("❤️  健康", self.character.stats['health']),
            ("😊 快樂", self.character.stats['happiness']),
            ("💰 財富", self.character.stats['wealth']),
            ("📚 知識", self.character.stats['knowledge']),
            ("👥 社交", self.character.stats['social'])
        ]
        
        for name, value in stats_display:
            bar = "█" * int(value / 5) + "░" * (20 - int(value / 5))
            print(f"{name}: [{bar}] {value:.0f}/100")
        
        print(f"\n💭 狀態: {self.character.get_status()}")
    
    def display_actions(self):
        """顯示可用行動"""
        print("\n📋 今天要做什麼？")
        print("-" * 50)
        
        for i, action in enumerate(self.actions, 1):
            effects_str = []
            for stat, change in action.effects.items():
                if change != 0:
                    stat_name = {
                        'weight': '體重',
                        'health': '健康',
                        'happiness': '快樂',
                        'wealth': '財富',
                        'knowledge': '知識',
                        'social': '社交'
                    }.get(stat, stat)
                    
                    if change > 0:
                        effects_str.append(f"+{change}{stat_name}")
                    else:
                        effects_str.append(f"{change}{stat_name}")
            
            print(f"{i}. {action.name} - {action.description}")
            print(f"   效果: {', '.join(effects_str)}")
    
    def process_daily_events(self):
        """處理每日隨機事件"""
        events = []
        
        # 根據指數觸發特殊事件
        if self.character.stats['health'] < 20:
            events.append("因為健康狀況不佳，今天感到很疲倦...")
            self.character.update_stats({'happiness': -5})
            
        if self.character.stats['happiness'] < 20:
            events.append("心情很低落，做什麼都提不起勁...")
            self.character.update_stats({'health': -3})
            
        if self.character.stats['wealth'] < 20:
            events.append("錢包空空如也，有點擔心生活費...")
            self.character.update_stats({'happiness': -3})
            
        if self.character.stats['social'] > 80:
            events.append("朋友們都很關心你的近況，感覺很溫暖！")
            self.character.update_stats({'happiness': 3})
            
        if self.character.stats['knowledge'] > 80:
            events.append("學到了很多新知識，工作表現更好了！")
            self.character.update_stats({'wealth': 5})
        
        # 隨機事件
        if random.random() < 0.3:  # 30%機率
            random_events = [
                ("下雨了，心情有點憂鬱", {'happiness': -2}),
                ("收到朋友的鼓勵訊息！", {'happiness': 3, 'social': 2}),
                ("路上撿到零錢", {'wealth': 2, 'happiness': 1}),
                ("看到勵志影片", {'happiness': 2, 'knowledge': 1}),
                ("感冒了一點", {'health': -3}),
                ("睡得很好", {'health': 3, 'happiness': 2})
            ]
            
            event_text, effects = random.choice(random_events)
            events.append(event_text)
            self.character.update_stats(effects)
        
        # 顯示事件
        if events:
            print("\n🎲 今日事件:")
            for event in events:
                print(f"   • {event}")
                self.character.events_log.append(f"第{self.character.day}天: {event}")
    
    def game_loop(self):
        """主遊戲循環"""
        while True:
            self.display_character_stats()
            
            # 檢查勝利/失敗條件
            game_result = self.character.check_win_condition()
            if game_result:
                self.handle_game_end(game_result)
                break
            
            self.display_actions()
            
            # 獲取玩家選擇
            while True:
                try:
                    print(f"\n請選擇行動 (1-{len(self.actions)}) 或輸入 's' 儲存遊戲, 'q' 退出: ")
                    choice = input(">>> ").strip().lower()
                    
                    if choice == 'q':
                        print("遊戲結束，再見！")
                        return
                    elif choice == 's':
                        self.save_game()
                        continue
                    
                    action_index = int(choice) - 1
                    if 0 <= action_index < len(self.actions):
                        chosen_action = self.actions[action_index]
                        break
                    else:
                        print("無效的選擇，請重試。")
                        
                except ValueError:
                    print("請輸入有效的數字。")
            
            # 執行選擇的行動
            print(f"\n{self.character.name} 選擇了: {chosen_action.name}")
            print(f"📝 {chosen_action.description}")
            
            self.character.update_stats(chosen_action.effects)
            
            # 處理每日事件
            self.process_daily_events()
            
            # 進入下一天
            self.character.day += 1
            
            input("\n按 Enter 鍵繼續到下一天...")
    
    def handle_game_end(self, result: str):
        """處理遊戲結束"""
        print("\n" + "=" * 50)
        if result == "win":
            print("🎉🎉🎉 恭喜您成功達成減肥目標！ 🎉🎉🎉")
            print(f"您在第 {self.character.day} 天達成了目標體重 {self.character.target_weight}kg！")
            print("您成功平衡了生活各個方面，真是太棒了！")
        elif result == "lose_health":
            print("😵 遊戲結束：健康狀況太差了...")
            print("記住，健康是最重要的，要好好照顧自己！")
        elif result == "lose_depression":
            print("😢 遊戲結束：心情太低落了...")
            print("快樂也是成功減肥的重要因素，要保持正面心態！")
        elif result == "lose_time":
            print("⏰ 遊戲結束：時間到了...")
            print("雖然沒有在100天內達成目標，但您已經有所進步！")
        
        weight_lost = self.character.initial_weight - self.character.stats['weight']
        print(f"\n📊 最終數據:")
        print(f"   總減重: {weight_lost:.1f}kg")
        print(f"   遊戲天數: {self.character.day} 天")
        
        # 刪除存檔
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
        
        print("=" * 50)
        input("按 Enter 鍵回到主選單...")
    
    def main_menu(self):
        """主選單"""
        while True:
            print("\n" + "=" * 50)
            print("🏃‍♂️ 減肥平衡遊戲 🏃‍♀️")
            print("=" * 50)
            print("1. 開始新遊戲")
            print("2. 載入遊戲")
            print("3. 遊戲說明")
            print("4. 退出遊戲")
            
            choice = input("\n請選擇 (1-4): ").strip()
            
            if choice == "1":
                self.start_new_game()
            elif choice == "2":
                if self.load_game():
                    self.game_loop()
                else:
                    print("沒有找到存檔，請先開始新遊戲。")
                    input("按 Enter 鍵繼續...")
            elif choice == "3":
                self.show_instructions()
            elif choice == "4":
                print("謝謝遊玩！再見！")
                break
            else:
                print("無效的選擇，請重試。")
    
    def show_instructions(self):
        """顯示遊戲說明"""
        print("\n" + "=" * 50)
        print("📖 遊戲說明")
        print("=" * 50)
        print("🎯 目標：在100天內從80kg減重到65kg")
        print("\n📊 指數說明：")
        print("   • 體重：越低越好，但不能太極端")
        print("   • 健康：保持身體健康，低於20會失敗")
        print("   • 快樂：保持心情愉快，低於20會失敗")
        print("   • 財富：金錢狀況，影響生活品質")
        print("   • 知識：學習成長，有助於工作")
        print("   • 社交：人際關係，影響心情")
        print("\n🎮 遊戲玩法：")
        print("   • 每天選擇一個行動")
        print("   • 每個行動會影響不同指數")
        print("   • 平衡各項指數是成功的關鍵")
        print("   • 隨機事件會增加遊戲趣味")
        print("\n💡 小貼士：")
        print("   • 不要只專注於體重，健康和快樂同樣重要")
        print("   • 適度運動和健康飲食是減肥王道")
        print("   • 保持社交和學習，生活要平衡")
        
        input("\n按 Enter 鍵回到主選單...")

def main():
    """主程序入口"""
    try:
        game = BalanceGame()
        game.main_menu()
    except KeyboardInterrupt:
        print("\n\n遊戲被中斷，再見！")
    except Exception as e:
        print(f"\n發生錯誤: {e}")
        print("請重新啟動遊戲。")

if __name__ == "__main__":
    main()