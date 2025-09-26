#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Balance Game - 減肥平衡遊戲
一個終端遊戲，讓玩家扮演一個人，透過每天的行動來平衡各項指數，最終達到減肥目標。
"""

import random
import json
import os
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class Character:
    """遊戲角色類別"""
    
    def __init__(self, name: str, config: Dict = None):
        self.name = name
        self.day = 1
        
        # 從配置讀取初始數值，如果沒有配置則使用預設值
        if config and 'initial_stats' in config:
            initial = config['initial_stats']
            self.stats = {
                'weight': float(initial.get('weight', 80.0)),
                'health': int(initial.get('health', 50)),
                'happiness': int(initial.get('happiness', 50)),
                'wealth': int(initial.get('wealth', 50)),
                'knowledge': int(initial.get('knowledge', 50)),
                'social': int(initial.get('social', 50))
            }
            self.target_weight = float(config.get('target_weight', 65.0))
            self.initial_weight = float(initial.get('weight', 80.0))
            self.max_days = int(config.get('max_days', 100))
            
            # 失敗條件閾值
            thresholds = config.get('failure_thresholds', {})
            self.health_threshold = int(thresholds.get('health', 10))
            self.happiness_threshold = int(thresholds.get('happiness', 10))
            
            # 統計數值限制
            limits = config.get('stat_limits', {})
            self.weight_min = float(limits.get('weight_min', 40.0))
            self.weight_max = float(limits.get('weight_max', 150.0))
            self.stat_min = int(limits.get('stat_min', 0))
            self.stat_max = int(limits.get('stat_max', 100))
        else:
            # 預設值（向後相容）
            self.stats = {
                'weight': 80.0,      # 體重 (kg)
                'health': 50,        # 健康 (0-100)
                'happiness': 50,     # 快樂 (0-100)
                'wealth': 50,        # 財富 (0-100)
                'knowledge': 50,     # 知識 (0-100)
                'social': 50         # 社交 (0-100)
            }
            self.target_weight = 65.0
            self.initial_weight = 80.0
            self.max_days = 100
            self.health_threshold = 10
            self.happiness_threshold = 10
            self.weight_min = 40.0
            self.weight_max = 150.0
            self.stat_min = 0
            self.stat_max = 100
        
        self.events_log = []
        
    def update_stats(self, changes: Dict[str, float]):
        """更新角色狀態"""
        for stat, change in changes.items():
            if stat == 'weight':
                self.stats[stat] += change
                # 體重限制使用配置值
                self.stats[stat] = max(self.weight_min, min(self.weight_max, self.stats[stat]))
            else:
                self.stats[stat] += change
                # 其他指數使用配置範圍
                self.stats[stat] = max(self.stat_min, min(self.stat_max, self.stats[stat]))
    
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
        
        # 失敗條件使用配置的閾值
        if self.stats['health'] <= self.health_threshold:
            return "lose_health"
        if self.stats['happiness'] <= self.happiness_threshold:
            return "lose_depression"
        if self.day > self.max_days:  # 使用配置的最大天數
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
        self.config = self.load_config()
        self.actions = self._init_actions()
        self.save_file = "balance_game_save.json"
        
    def load_config(self) -> Dict:
        """載入YAML配置文件"""
        config_path = Path(__file__).parent / "config" / "actions.yaml"
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            print(f"✅ 已載入配置文件: {config_path}")
            return config
        except FileNotFoundError:
            print(f"⚠️ 配置文件不存在: {config_path}")
            print("使用預設配置...")
            return self.get_default_config()
        except yaml.YAMLError as e:
            print(f"❌ 載入配置文件失敗: {e}")
            print("使用預設配置...")
            return self.get_default_config()
        except Exception as e:
            print(f"❌ 載入配置時發生錯誤: {e}")
            print("使用預設配置...")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """獲取預設配置（向後相容）"""
        return {
            'actions': [
                {
                    'name': '運動',
                    'description': '去健身房運動1小時',
                    'effects': {'weight': -0.5, 'health': 8, 'happiness': -3},
                    'energy_cost': 15
                },
                {
                    'name': '慢跑',
                    'description': '在公園慢跑30分鐘',
                    'effects': {'weight': -0.3, 'health': 5, 'happiness': 2, 'social': 1},
                    'energy_cost': 10
                },
                {
                    'name': '讀書',
                    'description': '閱讀一本好書',
                    'effects': {'knowledge': 6, 'happiness': 3, 'social': -2},
                    'energy_cost': 5
                },
                {
                    'name': '工作',
                    'description': '努力工作賺錢',
                    'effects': {'wealth': 8, 'health': -4, 'happiness': -2, 'weight': 0.2},
                    'energy_cost': 12
                },
                {
                    'name': '聚會',
                    'description': '和朋友聚會聊天',
                    'effects': {'social': 8, 'happiness': 5, 'wealth': -3, 'weight': 0.3},
                    'energy_cost': 8
                },
                {
                    'name': '休息',
                    'description': '在家放鬆休息',
                    'effects': {'happiness': 6, 'health': 3, 'knowledge': -1},
                    'energy_cost': 0
                },
                {
                    'name': '烹飪',
                    'description': '自己做健康料理',
                    'effects': {'health': 4, 'happiness': 3, 'wealth': -2, 'weight': -0.2},
                    'energy_cost': 6
                },
                {
                    'name': '冥想',
                    'description': '進行正念冥想',
                    'effects': {'happiness': 7, 'health': 2, 'knowledge': 2},
                    'energy_cost': 3
                },
                {
                    'name': '購物',
                    'description': '去商場購物',
                    'effects': {'happiness': 4, 'wealth': -5, 'social': 2, 'weight': 0.1},
                    'energy_cost': 7
                },
                {
                    'name': '學習',
                    'description': '參加線上課程',
                    'effects': {'knowledge': 8, 'wealth': -1, 'happiness': 1},
                    'energy_cost': 8
                }
            ],
            'game_settings': {
                'initial_stats': {
                    'weight': 80.0, 'health': 50, 'happiness': 50,
                    'wealth': 50, 'knowledge': 50, 'social': 50
                },
                'target_weight': 65.0,
                'max_days': 100,
                'failure_thresholds': {'health': 10, 'happiness': 10},
                'stat_limits': {
                    'weight_min': 40.0, 'weight_max': 150.0,
                    'stat_min': 0, 'stat_max': 100
                }
            },
            'random_events': {
                'probability': 0.3,
                'events': [
                    {
                        'name': '下雨天憂鬱',
                        'description': '下雨了，心情有點憂鬱',
                        'effects': {'happiness': -2},
                        'weight': 10
                    },
                    {
                        'name': '朋友鼓勵',
                        'description': '收到朋友的鼓勵訊息！',
                        'effects': {'happiness': 3, 'social': 2},
                        'weight': 15
                    },
                    {
                        'name': '意外收穫',
                        'description': '路上撿到零錢',
                        'effects': {'wealth': 2, 'happiness': 1},
                        'weight': 5
                    },
                    {
                        'name': '勵志內容',
                        'description': '看到勵志影片',
                        'effects': {'happiness': 2, 'knowledge': 1},
                        'weight': 12
                    },
                    {
                        'name': '輕微感冒',
                        'description': '感冒了一點',
                        'effects': {'health': -3},
                        'weight': 8
                    },
                    {
                        'name': '優質睡眠',
                        'description': '睡得很好',
                        'effects': {'health': 3, 'happiness': 2},
                        'weight': 15
                    }
                ]
            },
            'conditional_events': [
                {
                    'condition': {
                        'stat': 'health',
                        'operator': '<',
                        'value': 20
                    },
                    'event': {
                        'name': '疲倦狀態',
                        'description': '因為健康狀況不佳，今天感到很疲倦...',
                        'effects': {'happiness': -5}
                    },
                    'probability': 0.8
                },
                {
                    'condition': {
                        'stat': 'happiness',
                        'operator': '<',
                        'value': 20
                    },
                    'event': {
                        'name': '情緒低落',
                        'description': '心情很低落，做什麼都提不起勁...',
                        'effects': {'health': -3}
                    },
                    'probability': 0.7
                },
                {
                    'condition': {
                        'stat': 'wealth',
                        'operator': '<',
                        'value': 20
                    },
                    'event': {
                        'name': '經濟壓力',
                        'description': '錢包空空如也，有點擔心生活費...',
                        'effects': {'happiness': -3}
                    },
                    'probability': 0.6
                },
                {
                    'condition': {
                        'stat': 'social',
                        'operator': '>',
                        'value': 80
                    },
                    'event': {
                        'name': '朋友關懷',
                        'description': '朋友們都很關心你的近況，感覺很溫暖！',
                        'effects': {'happiness': 3}
                    },
                    'probability': 0.5
                },
                {
                    'condition': {
                        'stat': 'knowledge',
                        'operator': '>',
                        'value': 80
                    },
                    'event': {
                        'name': '知識應用',
                        'description': '學到了很多新知識，工作表現更好了！',
                        'effects': {'wealth': 5}
                    },
                    'probability': 0.4
                }
            ]
        }
        
    def _init_actions(self) -> List[Action]:
        """從配置文件初始化所有可用行動"""
        actions = []
        action_configs = self.config.get('actions', [])
        
        for action_config in action_configs:
            name = action_config.get('name', '未知行動')
            description = action_config.get('description', '無描述')
            effects = action_config.get('effects', {})
            energy_cost = action_config.get('energy_cost', 10)
            
            # 確保effects中的數值為正確類型
            clean_effects = {}
            for stat, value in effects.items():
                clean_effects[stat] = float(value)
            
            actions.append(Action(name, description, clean_effects, energy_cost))
        
        if not actions:
            print("⚠️ 未找到行動配置，使用預設行動")
            # 使用預設行動
            default_config = self.get_default_config()
            for action_config in default_config['actions']:
                actions.append(Action(
                    action_config['name'],
                    action_config['description'],
                    action_config['effects'],
                    action_config['energy_cost']
                ))
        
        return actions
    
    def check_condition(self, condition: Dict, character_stats: Dict) -> bool:
        """檢查條件是否符合"""
        stat = condition.get('stat')
        operator = condition.get('operator')
        value = condition.get('value')
        
        if not all([stat, operator, value is not None]):
            return False
        
        current_value = character_stats.get(stat, 0)
        
        if operator == '<':
            return current_value < value
        elif operator == '>':
            return current_value > value
        elif operator == '<=':
            return current_value <= value
        elif operator == '>=':
            return current_value >= value
        elif operator == '==':
            return current_value == value
        elif operator == '!=':
            return current_value != value
        else:
            return False
    
    def select_random_event(self, events: List[Dict]) -> Optional[Dict]:
        """基於權重選擇隨機事件"""
        if not events:
            return None
        
        # 計算總權重
        total_weight = sum(event.get('weight', 1) for event in events)
        if total_weight == 0:
            return random.choice(events)
        
        # 基於權重隨機選擇
        rand_num = random.uniform(0, total_weight)
        current_weight = 0
        
        for event in events:
            current_weight += event.get('weight', 1)
            if rand_num <= current_weight:
                return event
        
        return events[-1]  # 後備選擇
    
    def start_new_game(self):
        """開始新遊戲"""
        print("=" * 50)
        print("🏃‍♂️ 歡迎來到減肥平衡遊戲！ 🏃‍♀️")
        print("=" * 50)
        
        name = input("請輸入您的角色名字: ").strip()
        if not name:
            name = "減肥勇者"
        
        # 使用配置創建角色
        game_settings = self.config.get('game_settings', {})
        self.character = Character(name, game_settings)
        print(f"\n歡迎 {name}！")
        print(f"目標：從 {self.character.initial_weight}kg 減重到 {self.character.target_weight}kg")
        print(f"每天選擇一個行動，平衡各項指數，在{self.character.max_days}天內達成減肥目標！")
        
        self.game_loop()
    
    def load_game(self) -> bool:
        """載入遊戲"""
        if not os.path.exists(self.save_file):
            return False
        
        try:
            with open(self.save_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 使用配置創建角色
            game_settings = self.config.get('game_settings', {})
            self.character = Character(data['name'], game_settings)
            self.character.day = data['day']
            self.character.stats = data['stats']
            self.character.target_weight = data.get('target_weight', self.character.target_weight)
            self.character.initial_weight = data.get('initial_weight', self.character.initial_weight)
            self.character.events_log = data.get('events_log', [])
            
            # 載入存檔中的其他配置（如果有的話）
            if 'max_days' in data:
                self.character.max_days = data['max_days']
            if 'health_threshold' in data:
                self.character.health_threshold = data['health_threshold']
            if 'happiness_threshold' in data:
                self.character.happiness_threshold = data['happiness_threshold']
            
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
            'events_log': self.character.events_log,
            # 保存配置相關數據
            'max_days': self.character.max_days,
            'health_threshold': self.character.health_threshold,
            'happiness_threshold': self.character.happiness_threshold,
            # 保存存檔時的配置版本（用於未來兼容性）
            'config_version': '1.0'
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
        
        # 處理條件事件
        conditional_events = self.config.get('conditional_events', [])
        for cond_event_config in conditional_events:
            condition = cond_event_config.get('condition', {})
            event_info = cond_event_config.get('event', {})
            probability = cond_event_config.get('probability', 1.0)
            
            # 檢查條件是否滿足
            if self.check_condition(condition, self.character.stats):
                # 基於機率決定是否觸發
                if random.random() < probability:
                    description = event_info.get('description', '未知事件')
                    effects = event_info.get('effects', {})
                    
                    events.append(description)
                    self.character.update_stats(effects)
        
        # 處理隨機事件
        random_events_config = self.config.get('random_events', {})
        probability = random_events_config.get('probability', 0.3)
        
        if random.random() < probability:
            events_list = random_events_config.get('events', [])
            if events_list:
                selected_event = self.select_random_event(events_list)
                if selected_event:
                    description = selected_event.get('description', '未知隨機事件')
                    effects = selected_event.get('effects', {})
                    
                    events.append(description)
                    self.character.update_stats(effects)
        
        # 顯示事件
        if events:
            print("\n🎲 今日事件:")
            for event in events:
                print(f"   • {event}")
                if hasattr(self.character, 'events_log'):
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
        game_settings = self.config.get('game_settings', {})
        initial_weight = game_settings.get('initial_stats', {}).get('weight', 80.0)
        target_weight = game_settings.get('target_weight', 65.0)
        max_days = game_settings.get('max_days', 100)
        health_threshold = game_settings.get('failure_thresholds', {}).get('health', 10)
        happiness_threshold = game_settings.get('failure_thresholds', {}).get('happiness', 10)
        
        print(f"🎯 目標：在{max_days}天內從{initial_weight}kg減重到{target_weight}kg")
        print("\n📊 指數說明：")
        print("   • 體重：越低越好，但不能太極端")
        print(f"   • 健康：保持身體健康，低於{health_threshold}會失敗")
        print(f"   • 快樂：保持心情愉快，低於{happiness_threshold}會失敗")
        print("   • 財富：金錢狀況，影響生活品質")
        print("   • 知識：學習成長，有助於工作")
        print("   • 社交：人際關係，影響心情")
        print("\n🎮 遊戲玩法：")
        print("   • 每天選擇一個行動")
        print("   • 每個行動會影響不同指數")
        print("   • 平衡各項指數是成功的關鍵")
        print("   • 隨機事件會增加遊戲趣味")
        print("\n⚙️ 遊戲配置：")
        print("   • 行動和效果可在 config/actions.yaml 中自定義")
        print("   • 遊戲數值可根據個人喜好調整")
        print("   • 修改配置後重啟遊戲即可生效")
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