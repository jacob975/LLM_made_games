#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Balance Game GUI - 減肥平衡遊戲 (圖形界面版本)
使用tkinter創建的圖形界面版本減肥模擬遊戲
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import random
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import threading
import time

# 導入原始遊戲邏輯
from balance_game import Character, Action, BalanceGame

class BalanceGameGUI:
    """GUI版本的減肥平衡遊戲"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("減肥平衡遊戲 🏃‍♂️")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # 設定窗口圖標（如果有的話）
        try:
            self.root.iconbitmap("game_icon.ico")
        except:
            pass
        
        # 遊戲邏輯實例
        self.game_logic = BalanceGame()
        self.character = None
        
        # GUI元件
        self.notebook = None
        self.stats_frame = None
        self.actions_frame = None
        self.log_frame = None
        
        # 統計顯示元件
        self.stats_labels = {}
        self.progress_bars = {}
        self.day_label = None
        self.status_label = None
        
        # 行動按鈕
        self.action_buttons = []
        
        # 日誌文字框
        self.log_text = None
        
        # 主角造型相關
        self.character_canvas = None
        self.character_face = None
        self.character_body = None
        self.character_accessories = []
        self.current_mood = "normal"
        self.current_activity = "idle"
        self.last_action = None
        
        # 消息列折疊狀態
        self.log_collapsed = False
        self.log_container = None
        self.log_toggle_button = None
        self.log_original_height = 150
        
        # 初始化GUI
        self.setup_gui()
        self.show_main_menu()
    
    def setup_gui(self):
        """設置GUI界面"""
        # 主標題
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🏃‍♂️ 減肥平衡遊戲 🏃‍♀️",
            font=('微軟正黑體', 24, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # 創建筆記本容器（分頁）
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 遊戲主界面頁面
        self.game_frame = tk.Frame(self.notebook)
        self.notebook.add(self.game_frame, text="🎮 遊戲")
        
        # 設置遊戲主界面
        self.setup_game_interface()
        
        # 說明頁面
        self.help_frame = tk.Frame(self.notebook)
        self.notebook.add(self.help_frame, text="📖 說明")
        self.setup_help_interface()
        
        # 統計頁面
        self.stats_detail_frame = tk.Frame(self.notebook)
        self.notebook.add(self.stats_detail_frame, text="📊 詳細統計")
        self.setup_stats_detail_interface()
    
    def setup_game_interface(self):
        """設置遊戲主界面"""
        # 左側：角色狀態和造型
        left_frame = tk.Frame(self.game_frame, bg='#ecf0f1', relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # 角色造型區域
        character_title = tk.Label(
            left_frame,
            text="👤 主角造型",
            font=('微軟正黑體', 16, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        character_title.pack(pady=10)
        
        # 主角造型畫布
        self.character_canvas = tk.Canvas(
            left_frame,
            width=200,
            height=200,
            bg='#ffffff',
            relief='sunken',
            bd=2
        )
        self.character_canvas.pack(pady=10)
        
        # 角色狀態標題
        stats_title = tk.Label(
            left_frame,
            text="📊 角色狀態",
            font=('微軟正黑體', 16, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        stats_title.pack(pady=(20, 10))
        
        # 天數和狀態
        self.day_label = tk.Label(
            left_frame,
            text="第 1 天",
            font=('微軟正黑體', 14, 'bold'),
            bg='#ecf0f1',
            fg='#e74c3c'
        )
        self.day_label.pack(pady=5)
        
        self.status_label = tk.Label(
            left_frame,
            text="準備開始遊戲...",
            font=('微軟正黑體', 10),
            bg='#ecf0f1',
            fg='#7f8c8d',
            wraplength=250
        )
        self.status_label.pack(pady=5)
        
        # 統計數據框架
        stats_container = tk.Frame(left_frame, bg='#ecf0f1')
        stats_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 創建各項統計的顯示
        stat_configs = [
            ('weight', '🏋️ 體重', 'kg'),
            ('health', '❤️ 健康', '/100'),
            ('happiness', '😊 快樂', '/100'),
            ('wealth', '💰 財富', '/100'),
            ('knowledge', '📚 知識', '/100'),
            ('social', '👥 社交', '/100')
        ]
        
        for stat_key, stat_name, unit in stat_configs:
            stat_frame = tk.Frame(stats_container, bg='#ecf0f1')
            stat_frame.pack(fill='x', pady=8)
            
            # 統計名稱
            name_label = tk.Label(
                stat_frame,
                text=stat_name,
                font=('微軟正黑體', 12, 'bold'),
                bg='#ecf0f1',
                fg='#2c3e50'
            )
            name_label.pack(anchor='w')
            
            # 數值顯示
            value_frame = tk.Frame(stat_frame, bg='#ecf0f1')
            value_frame.pack(fill='x', pady=2)
            
            self.stats_labels[stat_key] = tk.Label(
                value_frame,
                text=f"0{unit}",
                font=('微軟正黑體', 11),
                bg='#ecf0f1',
                fg='#34495e'
            )
            self.stats_labels[stat_key].pack(side='left')
            
            # 進度條（除了體重）
            if stat_key != 'weight':
                progress = ttk.Progressbar(
                    value_frame,
                    mode='determinate',
                    length=150,
                    style='Custom.Horizontal.TProgressbar'
                )
                progress.pack(side='right')
                self.progress_bars[stat_key] = progress
        
        # 右側：行動選擇和日誌
        right_frame = tk.Frame(self.game_frame, bg='#ecf0f1')
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # 行動選擇區域
        actions_title = tk.Label(
            right_frame,
            text="🎯 今天要做什麼？",
            font=('微軟正黑體', 16, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        actions_title.pack(pady=10)
        
        # 行動按鈕容器
        actions_container = tk.Frame(right_frame, bg='#ecf0f1')
        actions_container.pack(fill='x', padx=10)
        
        # 創建行動按鈕（2列布局）
        self.create_action_buttons(actions_container)
        
        # 控制按鈕
        control_frame = tk.Frame(right_frame, bg='#ecf0f1')
        control_frame.pack(fill='x', padx=10, pady=10)
        
        self.save_button = tk.Button(
            control_frame,
            text="💾 儲存遊戲",
            font=('微軟正黑體', 11),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            command=self.save_game
        )
        self.save_button.pack(side='left', padx=5)
        
        self.load_button = tk.Button(
            control_frame,
            text="📁 載入遊戲",
            font=('微軟正黑體', 11),
            bg='#2ecc71',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            command=self.load_game
        )
        self.load_button.pack(side='left', padx=5)
        
        self.new_game_button = tk.Button(
            control_frame,
            text="🆕 新遊戲",
            font=('微軟正黑體', 11),
            bg='#e67e22',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            command=self.start_new_game
        )
        self.new_game_button.pack(side='left', padx=5)
        
        # 日誌區域標題框架
        log_title_frame = tk.Frame(right_frame, bg='#ecf0f1')
        log_title_frame.pack(fill='x', pady=(20, 0))
        
        # 日誌標題
        log_title = tk.Label(
            log_title_frame,
            text="📝 遊戲日誌",
            font=('微軟正黑體', 14, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        log_title.pack(side='left')
        
        # 折疊/展開按鈕
        self.log_toggle_button = tk.Button(
            log_title_frame,
            text="▼",
            font=('微軟正黑體', 12, 'bold'),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            width=3,
            height=1,
            command=self.toggle_log
        )
        self.log_toggle_button.pack(side='right')
        
        # 日誌文字框和滾動條容器
        self.log_container = tk.Frame(right_frame, bg='#ecf0f1')
        self.log_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.log_text = tk.Text(
            self.log_container,
            height=8,
            font=('微軟正黑體', 10),
            bg='white',
            fg='#2c3e50',
            relief='sunken',
            bd=1,
            wrap='word'
        )
        
        log_scrollbar = ttk.Scrollbar(self.log_container)
        log_scrollbar.pack(side='right', fill='y')
        
        self.log_text.pack(side='left', fill='both', expand=True)
        self.log_text.config(yscrollcommand=log_scrollbar.set)
        log_scrollbar.config(command=self.log_text.yview)
    
    def create_action_buttons(self, parent):
        """創建行動按鈕"""
        actions = self.game_logic.actions
        
        # 清除現有按鈕
        for widget in parent.winfo_children():
            widget.destroy()
        self.action_buttons.clear()
        
        # 創建2列網格布局
        for i, action in enumerate(actions):
            row = i // 2
            col = i % 2
            
            # 按鈕框架
            button_frame = tk.Frame(parent, bg='#ecf0f1')
            button_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            # 配置列權重
            parent.columnconfigure(col, weight=1)
            
            # 行動按鈕
            button = tk.Button(
                button_frame,
                text=f"{action.name}",
                font=('微軟正黑體', 11, 'bold'),
                bg='#34495e',
                fg='white',
                relief='flat',
                padx=10,
                pady=8,
                width=15,
                command=lambda a=action: self.perform_action(a)
            )
            button.pack(fill='x')
            
            # 效果描述
            effects_text = self.format_action_effects(action)
            desc_label = tk.Label(
                button_frame,
                text=effects_text,
                font=('微軟正黑體', 9),
                bg='#ecf0f1',
                fg='#7f8c8d',
                wraplength=200
            )
            desc_label.pack(pady=2)
            
            self.action_buttons.append(button)
    
    def format_action_effects(self, action: Action) -> str:
        """格式化行動效果描述"""
        effects = []
        stat_names = {
            'weight': '體重',
            'health': '健康',
            'happiness': '快樂',
            'wealth': '財富',
            'knowledge': '知識',
            'social': '社交'
        }
        
        for stat, change in action.effects.items():
            if change != 0:
                stat_name = stat_names.get(stat, stat)
                if change > 0:
                    effects.append(f"+{change}{stat_name}")
                else:
                    effects.append(f"{change}{stat_name}")
        
        return f"{action.description}\n效果: {', '.join(effects)}"
    
    def toggle_log(self):
        """切換日誌區域的折疊狀態"""
        if self.log_collapsed:
            # 展開日誌
            self.log_container.pack(fill='both', expand=True, padx=10, pady=5)
            self.log_toggle_button.config(text="▼")
            self.log_collapsed = False
        else:
            # 折疊日誌
            self.log_container.pack_forget()
            self.log_toggle_button.config(text="▲")
            self.log_collapsed = True
    
    def draw_character(self):
        """繪製主角造型"""
        if not self.character_canvas or not self.character:
            return
            
        # 清空畫布
        self.character_canvas.delete("all")
        
        # 畫布尺寸
        width = 200
        height = 200
        center_x = width // 2
        center_y = height // 2
        
        # 根據狀態決定造型
        self.determine_character_appearance()
        
        # 繪製身體（橢圓形）
        body_color = self.get_body_color()
        body_size = self.get_body_size()
        
        self.character_canvas.create_oval(
            center_x - body_size, center_y + 20 - body_size//2,
            center_x + body_size, center_y + 20 + body_size//2,
            fill=body_color, outline='#2c3e50', width=2
        )
        
        # 繪製頭部
        head_color = '#ffdbac'  # 膚色
        self.character_canvas.create_oval(
            center_x - 25, center_y - 60,
            center_x + 25, center_y - 10,
            fill=head_color, outline='#2c3e50', width=2
        )
        
        # 繪製臉部表情
        self.draw_face(center_x, center_y - 35)
        
        # 繪製配件（根據最近行動）
        self.draw_accessories(center_x, center_y)
        
        # 繪製狀態指示器
        self.draw_status_indicators(center_x, center_y)
    
    def determine_character_appearance(self):
        """根據角色狀態決定外觀"""
        if not self.character:
            return
            
        # 根據快樂度決定心情
        happiness = self.character.stats.get('happiness', 50)
        if happiness >= 70:
            self.current_mood = "happy"
        elif happiness >= 40:
            self.current_mood = "normal"
        elif happiness >= 20:
            self.current_mood = "sad"
        else:
            self.current_mood = "very_sad"
        
        # 根據最後行動決定活動狀態
        if self.last_action:
            action_name = self.last_action.name
            if "運動" in action_name or "慢跑" in action_name:
                self.current_activity = "exercise"
            elif "工作" in action_name:
                self.current_activity = "work"
            elif "讀書" in action_name or "學習" in action_name:
                self.current_activity = "study"
            elif "聚會" in action_name:
                self.current_activity = "social"
            elif "休息" in action_name or "冥想" in action_name:
                self.current_activity = "relax"
            elif "烹飪" in action_name:
                self.current_activity = "cooking"
            elif "購物" in action_name:
                self.current_activity = "shopping"
            else:
                self.current_activity = "idle"
    
    def get_body_color(self):
        """根據健康狀況決定身體顏色"""
        if not self.character:
            return '#87ceeb'  # 天藍色
            
        health = self.character.stats.get('health', 50)
        if health >= 80:
            return '#98fb98'  # 淺綠色，健康
        elif health >= 60:
            return '#87ceeb'  # 天藍色，一般
        elif health >= 40:
            return '#f0e68c'  # 卡其色，疲累
        elif health >= 20:
            return '#dda0dd'  # 紫色，不健康
        else:
            return '#f08080'  # 淺紅色，很不健康
    
    def get_body_size(self):
        """根據體重決定身體大小"""
        if not self.character:
            return 35
            
        weight = self.character.stats.get('weight', 75)
        # 體重在65-85之間，身體大小在25-45之間
        size = int(25 + (weight - 65) * 0.5)
        return max(25, min(45, size))
    
    def draw_face(self, x, y):
        """繪製面部表情"""
        # 眼睛
        self.character_canvas.create_oval(x-10, y-8, x-6, y-4, fill='black')
        self.character_canvas.create_oval(x+6, y-8, x+10, y-4, fill='black')
        
        # 根據心情繪製嘴巴
        if self.current_mood == "happy":
            # 開心的笑臉
            self.character_canvas.create_arc(
                x-8, y+2, x+8, y+12,
                start=0, extent=180, style='arc', outline='#2c3e50', width=2
            )
        elif self.current_mood == "normal":
            # 普通表情
            self.character_canvas.create_line(x-6, y+6, x+6, y+6, fill='#2c3e50', width=2)
        elif self.current_mood == "sad":
            # 難過表情
            self.character_canvas.create_arc(
                x-8, y+2, x+8, y+12,
                start=180, extent=180, style='arc', outline='#2c3e50', width=2
            )
        else:  # very_sad
            # 很難過表情
            self.character_canvas.create_arc(
                x-10, y, x+10, y+15,
                start=180, extent=180, style='arc', outline='#e74c3c', width=3
            )
            # 眼淚
            self.character_canvas.create_oval(x-12, y+2, x-10, y+8, fill='#3498db')
            self.character_canvas.create_oval(x+10, y+2, x+12, y+8, fill='#3498db')
    
    def draw_accessories(self, center_x, center_y):
        """根據最近行動繪製配件"""
        if self.current_activity == "exercise":
            # 運動頭帶
            self.character_canvas.create_rectangle(
                center_x-30, center_y-50, center_x+30, center_y-45,
                fill='#e74c3c', outline='#c0392b', width=1
            )
            # 汗珠
            self.character_canvas.create_oval(center_x+15, center_y-40, center_x+20, center_y-35, fill='#3498db')
            
        elif self.current_activity == "work":
            # 領帶
            self.character_canvas.create_polygon(
                center_x-3, center_y-5, center_x+3, center_y-5,
                center_x+5, center_y+30, center_x-5, center_y+30,
                fill='#2c3e50', outline='#34495e'
            )
            
        elif self.current_activity == "study":
            # 眼鏡
            self.character_canvas.create_oval(center_x-15, center_y-45, center_x-5, center_y-35, outline='#2c3e50', width=2)
            self.character_canvas.create_oval(center_x+5, center_y-45, center_x+15, center_y-35, outline='#2c3e50', width=2)
            self.character_canvas.create_line(center_x-5, center_y-40, center_x+5, center_y-40, fill='#2c3e50', width=2)
            
        elif self.current_activity == "social":
            # 派對帽
            self.character_canvas.create_polygon(
                center_x-15, center_y-50, center_x+15, center_y-50,
                center_x, center_y-70,
                fill='#f39c12', outline='#e67e22', width=2
            )
            self.character_canvas.create_oval(center_x-2, center_y-72, center_x+2, center_y-68, fill='#e74c3c')
            
        elif self.current_activity == "cooking":
            # 廚師帽
            self.character_canvas.create_rectangle(
                center_x-20, center_y-65, center_x+20, center_y-50,
                fill='white', outline='#bdc3c7', width=2
            )
            self.character_canvas.create_rectangle(
                center_x-25, center_y-55, center_x+25, center_y-50,
                fill='white', outline='#bdc3c7', width=1
            )
            
        elif self.current_activity == "relax":
            # 睡眠標誌 (Z字)
            self.character_canvas.create_text(
                center_x+25, center_y-50, text="Z", font=('微軟正黑體', 16, 'bold'),
                fill='#95a5a6'
            )
            self.character_canvas.create_text(
                center_x+30, center_y-40, text="Z", font=('微軟正黑體', 12, 'bold'),
                fill='#bdc3c7'
            )
    
    def draw_status_indicators(self, center_x, center_y):
        """繪製狀態指示器"""
        if not self.character:
            return
            
        # 低健康警告
        if self.character.stats.get('health', 50) < 30:
            self.character_canvas.create_text(
                center_x-40, center_y-70, text="🤒", font=('微軟正黑體', 20)
            )
            
        # 低快樂警告
        if self.character.stats.get('happiness', 50) < 30:
            self.character_canvas.create_text(
                center_x+40, center_y-70, text="😢", font=('微軟正黑體', 20)
            )
            
        # 高成就指示
        if self.character.stats.get('knowledge', 50) > 80:
            self.character_canvas.create_text(
                center_x-40, center_y+50, text="🎓", font=('微軟正黑體', 16)
            )
            
        if self.character.stats.get('wealth', 50) > 80:
            self.character_canvas.create_text(
                center_x+40, center_y+50, text="💰", font=('微軟正黑體', 16)
            )
    
    def setup_help_interface(self):
        """設置幫助界面"""
        help_text = tk.Text(
            self.help_frame,
            font=('微軟正黑體', 11),
            bg='#fefefe',
            fg='#2c3e50',
            relief='flat',
            wrap='word',
            padx=20,
            pady=20
        )
        help_text.pack(fill='both', expand=True)
        
        help_scrollbar = ttk.Scrollbar(self.help_frame)
        help_scrollbar.pack(side='right', fill='y')
        help_text.config(yscrollcommand=help_scrollbar.set)
        help_scrollbar.config(command=help_text.yview)
        
        help_content = """
🎯 遊戲目標
在100天內從80kg減重到65kg，同時保持健康和快樂指數不低於20。

📊 指數說明
• 體重 🏋️ - 主要目標，需要從80kg減到65kg
• 健康 ❤️ - 身體狀況，不能低於20（會失敗）
• 快樂 😊 - 心理狀態，不能低於20（會失敗）
• 財富 💰 - 經濟狀況，影響生活品質
• 知識 📚 - 學習成長，間接影響其他方面
• 社交 👥 - 人際關係，影響心情

🎮 遊戲玩法
1. 每天選擇一個行動
2. 每個行動會影響不同的指數
3. 平衡各項指數是成功的關鍵
4. 注意隨機事件的影響
5. 可以隨時儲存和載入遊戲

🎯 可選行動
1. 運動 - 去健身房運動1小時
   效果: 減重效果佳，提升健康，但會降低快樂

2. 慢跑 - 在公園慢跑30分鐘
   效果: 平衡的運動選擇，還有輕微社交加成

3. 讀書 - 閱讀一本好書
   效果: 增加知識和快樂，但會減少社交

4. 工作 - 努力工作賺錢
   效果: 增加財富但損害健康，還會輕微增重

5. 聚會 - 和朋友聚會聊天
   效果: 大幅提升社交和快樂，但花錢且增重

6. 休息 - 在家放鬆休息
   效果: 恢復快樂和健康，但知識會下降

7. 烹飪 - 自己做健康料理
   效果: 健康的選擇，有助減重

8. 冥想 - 進行正念冥想
   效果: 心靈平靜，提升多項指數

9. 購物 - 去商場購物
   效果: 花錢買快樂，輕微社交效果

10. 學習 - 參加線上課程
    效果: 大幅提升知識，小幅提升快樂

🎲 隨機事件
遊戲中會根據你的當前狀態觸發各種事件：
• 健康過低時可能會感到疲倦
• 快樂過低時可能會心情低落
• 財富過低時可能會擔心生活費
• 高指數時可能獲得額外獎勵
• 還有各種日常隨機事件

🏆 勝利與失敗
勝利條件：
• 體重達到65kg或以下

失敗條件：
• 健康指數降到20以下
• 快樂指數降到20以下
• 100天內未達成減肥目標

💡 策略建議
• 不要只專注於減重，健康和快樂同樣重要
• 適度運動是減肥的關鍵，但要注意快樂指數
• 保持社交活動可以提升心情
• 學習和工作可以提升生活品質
• 注意隨機事件，有時需要調整策略
• 烹飪和冥想是很好的平衡選擇

🎨 GUI操作說明
• 點擊行動按鈕執行對應行動
• 使用儲存/載入按鈕管理遊戲進度
• 查看遊戲日誌了解詳細變化
• 切換到詳細統計頁面查看完整數據
• 所有操作都有即時反饋
        """
        
        help_text.insert('1.0', help_content)
        help_text.config(state='disabled')
    
    def setup_stats_detail_interface(self):
        """設置詳細統計界面"""
        self.stats_detail_text = tk.Text(
            self.stats_detail_frame,
            font=('Consolas', 11),
            bg='#2c3e50',
            fg='#ecf0f1',
            relief='flat',
            wrap='word',
            padx=20,
            pady=20
        )
        self.stats_detail_text.pack(fill='both', expand=True)
        
        detail_scrollbar = ttk.Scrollbar(self.stats_detail_frame)
        detail_scrollbar.pack(side='right', fill='y')
        self.stats_detail_text.config(yscrollcommand=detail_scrollbar.set)
        detail_scrollbar.config(command=self.stats_detail_text.yview)
    
    def show_main_menu(self):
        """顯示主選單對話框"""
        if not hasattr(self, 'character') or self.character is None:
            choice = messagebox.askyesnocancel(
                "歡迎來到減肥平衡遊戲",
                "🏃‍♂️ 歡迎來到減肥平衡遊戲！🏃‍♀️\n\n" +
                "選擇：\n" +
                "是 - 開始新遊戲\n" +
                "否 - 載入舊遊戲\n" +
                "取消 - 退出遊戲"
            )
            
            if choice is True:
                self.start_new_game()
            elif choice is False:
                self.load_game()
            else:
                self.root.quit()
    
    def start_new_game(self):
        """開始新遊戲"""
        name = simpledialog.askstring(
            "新遊戲",
            "請輸入您的角色名字:",
            initialvalue="減肥勇者"
        )
        
        if name is None:  # 用戶取消
            return
        
        if not name.strip():
            name = "減肥勇者"
        
        # 使用配置創建新角色
        game_settings = self.game_logic.config.get('game_settings', {})
        self.character = Character(name.strip(), game_settings)
        self.game_logic.character = self.character
        
        # 更新界面
        self.update_display()
        
        # 初始化造型
        self.draw_character()
        
        # 歡迎訊息
        welcome_msg = f"歡迎 {name}！\n目標：從 {self.character.initial_weight}kg 減重到 {self.character.target_weight}kg\n每天選擇一個行動，在{self.character.max_days}天內達成減肥目標！"
        self.add_log(welcome_msg)
        
        messagebox.showinfo(
            "新遊戲開始",
            welcome_msg
        )
    
    def load_game(self):
        """載入遊戲"""
        if self.game_logic.load_game():
            self.character = self.game_logic.character
            self.update_display()
            self.draw_character()  # 繪製載入後的造型
            self.add_log(f"遊戲已載入！歡迎回來，{self.character.name}！")
            messagebox.showinfo("載入成功", f"歡迎回來，{self.character.name}！")
        else:
            messagebox.showwarning("載入失敗", "沒有找到存檔檔案，請先開始新遊戲。")
    
    def save_game(self):
        """儲存遊戲"""
        if self.character:
            self.game_logic.save_game()
            self.add_log("遊戲已儲存！")
            messagebox.showinfo("儲存成功", "遊戲已儲存！")
        else:
            messagebox.showwarning("儲存失敗", "沒有進行中的遊戲可以儲存。")
    
    def perform_action(self, action: Action):
        """執行行動"""
        if not self.character:
            messagebox.showwarning("錯誤", "請先開始遊戲！")
            return
        
        # 檢查遊戲結束條件
        game_result = self.character.check_win_condition()
        if game_result:
            self.handle_game_end(game_result)
            return
        
        # 記錄最後行動（用於造型更新）
        self.last_action = action
        
        # 執行行動
        self.add_log(f"\n第{self.character.day}天 - {self.character.name} 選擇了: {action.name}")
        self.add_log(f"📝 {action.description}")
        
        # 記錄行動前的狀態
        old_stats = self.character.stats.copy()
        
        # 更新角色狀態
        self.character.update_stats(action.effects)
        
        # 顯示變化
        self.show_stat_changes(old_stats, self.character.stats, action.effects)
        
        # 處理每日事件
        self.process_daily_events()
        
        # 進入下一天
        self.character.day += 1
        
        # 更新顯示（包括造型）
        self.update_display()
        
        # 檢查遊戲結束條件
        game_result = self.character.check_win_condition()
        if game_result:
            self.handle_game_end(game_result)
    
    def show_stat_changes(self, old_stats: Dict[str, float], new_stats: Dict[str, float], effects: Dict[str, float]):
        """顯示數值變化"""
        changes = []
        stat_names = {
            'weight': '體重',
            'health': '健康',
            'happiness': '快樂',
            'wealth': '財富',
            'knowledge': '知識',
            'social': '社交'
        }
        
        for stat, change in effects.items():
            if change != 0:
                stat_name = stat_names.get(stat, stat)
                old_val = old_stats.get(stat, 0)
                new_val = new_stats.get(stat, 0)
                
                if stat == 'weight':
                    changes.append(f"{stat_name}: {old_val:.1f} → {new_val:.1f}kg ({change:+.1f})")
                else:
                    changes.append(f"{stat_name}: {old_val:.0f} → {new_val:.0f} ({change:+.0f})")
        
        if changes:
            self.add_log("📊 指數變化: " + ", ".join(changes))
    
    def process_daily_events(self):
        """處理每日事件（使用YAML配置的事件系統）"""
        if not self.game_logic:
            return
            
        # 使用遊戲邏輯的事件處理方法
        events_occurred = []
        
        # 處理條件事件
        conditional_events = self.game_logic.config.get('conditional_events', [])
        for event_config in conditional_events:
            condition = event_config.get('condition', {})
            probability = event_config.get('probability', 0.5)
            
            # 檢查條件
            if (self.game_logic.check_condition(condition, self.character.stats) and 
                random.random() < probability):
                
                event = event_config.get('event', {})
                event_name = event.get('name', '未知事件')
                event_desc = event.get('description', '發生了什麼事...')
                effects = event.get('effects', {})
                
                events_occurred.append(event_desc)
                self.character.update_stats(effects)
        
        # 處理隨機事件
        random_events = self.game_logic.config.get('random_events', {})
        event_probability = random_events.get('probability', 0.3)
        
        if random.random() < event_probability:
            events_list = random_events.get('events', [])
            if events_list:
                selected_event = self.game_logic.select_random_event(events_list)
                if selected_event:
                    event_name = selected_event.get('name', '未知事件')
                    event_desc = selected_event.get('description', '發生了什麼事...')
                    effects = selected_event.get('effects', {})
                    
                    events_occurred.append(event_desc)
                    self.character.update_stats(effects)
        
        # 顯示事件
        if events_occurred:
            self.add_log("🎲 今日事件:")
            for event in events_occurred:
                self.add_log(f"   • {event}")
                if hasattr(self.character, 'events_log'):
                    self.character.events_log.append(f"第{self.character.day}天: {event}")
            
            # 事件可能影響造型，稍後會在update_display中重新繪製
    
    def handle_game_end(self, result: str):
        """處理遊戲結束"""
        title = ""
        message = ""
        
        if result == "win":
            title = "🎉 恭喜獲勝！"
            message = f"🎉🎉🎉 恭喜您成功達成減肥目標！ 🎉🎉🎉\n\n您在第 {self.character.day} 天達成了目標體重 {self.character.target_weight}kg！\n您成功平衡了生活各個方面，真是太棒了！"
        elif result == "lose_health":
            title = "😵 遊戲結束"
            message = "😵 遊戲結束：健康狀況太差了...\n\n記住，健康是最重要的，要好好照顧自己！"
        elif result == "lose_depression":
            title = "😢 遊戲結束"
            message = "😢 遊戲結束：心情太低落了...\n\n快樂也是成功減肥的重要因素，要保持正面心態！"
        elif result == "lose_time":
            title = "⏰ 遊戲結束"
            message = "⏰ 遊戲結束：時間到了...\n\n雖然沒有在100天內達成目標，但您已經有所進步！"
        
        weight_lost = self.character.initial_weight - self.character.stats['weight']
        message += f"\n\n📊 最終數據:\n   總減重: {weight_lost:.1f}kg\n   遊戲天數: {self.character.day} 天"
        
        # 記錄到日誌
        self.add_log(f"\n{title}")
        self.add_log(message)
        
        # 顯示對話框
        messagebox.showinfo(title, message)
        
        # 刪除存檔
        if os.path.exists(self.game_logic.save_file):
            os.remove(self.game_logic.save_file)
        
        # 重置遊戲
        self.character = None
        self.game_logic.character = None
        self.update_display()
        
        # 詢問是否開始新遊戲
        if messagebox.askyesno("遊戲結束", "要開始新遊戲嗎？"):
            self.start_new_game()
    
    def update_display(self):
        """更新顯示"""
        if not self.character:
            # 重置顯示
            self.day_label.config(text="準備開始...")
            self.status_label.config(text="請開始新遊戲或載入存檔")
            
            for stat_key in self.stats_labels:
                if stat_key == 'weight':
                    self.stats_labels[stat_key].config(text="0.0kg")
                else:
                    self.stats_labels[stat_key].config(text="0/100")
                    self.progress_bars[stat_key]['value'] = 0
            return
        
        # 更新天數
        self.day_label.config(text=f"第 {self.character.day} 天")
        
        # 更新狀態描述
        status = self.character.get_status()
        self.status_label.config(text=status)
        
        # 更新統計數據
        weight_progress = ((self.character.initial_weight - self.character.stats['weight']) / 
                          (self.character.initial_weight - self.character.target_weight)) * 100
        
        self.stats_labels['weight'].config(
            text=f"{self.character.stats['weight']:.1f}kg (進度: {weight_progress:.1f}%)"
        )
        
        for stat_key in ['health', 'happiness', 'wealth', 'knowledge', 'social']:
            value = self.character.stats[stat_key]
            self.stats_labels[stat_key].config(text=f"{value:.0f}/100")
            self.progress_bars[stat_key]['value'] = value
            
            # 根據數值改變進度條顏色
            if value <= 20:
                self.progress_bars[stat_key].configure(style='Red.Horizontal.TProgressbar')
            elif value <= 50:
                self.progress_bars[stat_key].configure(style='Yellow.Horizontal.TProgressbar')
            else:
                self.progress_bars[stat_key].configure(style='Green.Horizontal.TProgressbar')
        
        # 更新詳細統計
        self.update_detailed_stats()
        
        # 更新主角造型
        self.draw_character()
    
    def update_detailed_stats(self):
        """更新詳細統計頁面"""
        if not self.character:
            self.stats_detail_text.delete('1.0', 'end')
            self.stats_detail_text.insert('1.0', "請先開始遊戲...")
            return
        
        # 計算各種統計數據
        weight_lost = self.character.initial_weight - self.character.stats['weight']
        target_loss = self.character.initial_weight - self.character.target_weight
        progress = (weight_lost / target_loss) * 100 if target_loss > 0 else 0
        days_remaining = 100 - self.character.day + 1
        
        stats_text = f"""
═══════════════════════════════════════════════════════
    📊 {self.character.name} 的詳細統計資料
═══════════════════════════════════════════════════════

⏰ 時間資訊
   當前天數: 第 {self.character.day} 天
   剩餘天數: {days_remaining} 天
   遊戲進度: {((self.character.day - 1) / 100) * 100:.1f}%

🏋️ 減肥進度
   起始體重: {self.character.initial_weight:.1f}kg
   當前體重: {self.character.stats['weight']:.1f}kg
   目標體重: {self.character.target_weight}kg
   已減重量: {weight_lost:.1f}kg
   目標重量: {target_loss:.1f}kg
   完成進度: {progress:.1f}%
   平均日減: {weight_lost / max(1, self.character.day - 1):.2f}kg/天

📊 各項指數詳情
   ❤️  健康: {self.character.stats['health']:.0f}/100 {'⚠️ 危險!' if self.character.stats['health'] <= 20 else '✅ 安全' if self.character.stats['health'] >= 60 else '⚡ 注意'}
   😊 快樂: {self.character.stats['happiness']:.0f}/100 {'⚠️ 危險!' if self.character.stats['happiness'] <= 20 else '✅ 良好' if self.character.stats['happiness'] >= 60 else '⚡ 普通'}
   💰 財富: {self.character.stats['wealth']:.0f}/100 {'💸 貧困' if self.character.stats['wealth'] <= 20 else '💰 富裕' if self.character.stats['wealth'] >= 80 else '💵 普通'}
   📚 知識: {self.character.stats['knowledge']:.0f}/100 {'📖 博學' if self.character.stats['knowledge'] >= 80 else '📚 學習中' if self.character.stats['knowledge'] >= 40 else '🤔 需加油'}
   👥 社交: {self.character.stats['social']:.0f}/100 {'🎉 人氣王' if self.character.stats['social'] >= 80 else '👥 正常' if self.character.stats['social'] >= 40 else '😔 孤獨'}

🎯 目標分析
   距離目標: {max(0, self.character.stats['weight'] - self.character.target_weight):.1f}kg
   建議策略: {'🎉 已達成目標！' if self.character.stats['weight'] <= self.character.target_weight else '🏃‍♂️ 需要更多運動' if weight_lost < target_loss * 0.5 else '💪 繼續保持！'}

🎲 風險評估
   健康風險: {'🚨 極高' if self.character.stats['health'] <= 20 else '⚠️ 高' if self.character.stats['health'] <= 40 else '✅ 低'}
   心理風險: {'🚨 極高' if self.character.stats['happiness'] <= 20 else '⚠️ 高' if self.character.stats['happiness'] <= 40 else '✅ 低'}
   時間風險: {'🚨 極高' if days_remaining <= 10 and progress < 80 else '⚠️ 高' if days_remaining <= 30 and progress < 50 else '✅ 低'}

💡 智慧建議
"""
        
        # 添加建議
        suggestions = []
        if self.character.stats['health'] <= 30:
            suggestions.append("   🏥 健康狀況不佳，建議多休息、運動或冥想")
        if self.character.stats['happiness'] <= 30:
            suggestions.append("   😊 心情低落，建議聚會、休息或購物")
        if self.character.stats['weight'] > self.character.target_weight + 5:
            suggestions.append("   🏃‍♂️ 體重超標較多，建議加強運動和烹飪")
        if days_remaining <= 20 and progress < 70:
            suggestions.append("   ⏰ 時間緊迫，需要專注於減重行動")
        if self.character.stats['wealth'] <= 20:
            suggestions.append("   💼 財富不足，建議多工作賺錢")
        
        if not suggestions:
            suggestions.append("   🌟 目前狀況良好，繼續保持平衡！")
        
        stats_text += "\n".join(suggestions)
        
        # 添加事件日誌
        if hasattr(self.character, 'events_log') and self.character.events_log:
            stats_text += f"\n\n📝 重要事件記錄 (最近10項):\n"
            recent_events = self.character.events_log[-10:] if len(self.character.events_log) > 10 else self.character.events_log
            for event in recent_events:
                stats_text += f"   • {event}\n"
        
        stats_text += "\n═══════════════════════════════════════════════════════"
        
        # 更新文字
        self.stats_detail_text.delete('1.0', 'end')
        self.stats_detail_text.insert('1.0', stats_text)
    
    def add_log(self, message: str):
        """添加日誌訊息"""
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')  # 自動滾動到最新訊息
    
    def setup_progressbar_styles(self):
        """設置進度條樣式"""
        style = ttk.Style()
        
        # 綠色進度條（良好狀態）
        style.configure("Green.Horizontal.TProgressbar", 
                       troughcolor='#ecf0f1',
                       bordercolor='#27ae60',
                       background='#27ae60',
                       lightcolor='#27ae60',
                       darkcolor='#27ae60')
        
        # 黃色進度條（警告狀態）
        style.configure("Yellow.Horizontal.TProgressbar",
                       troughcolor='#ecf0f1', 
                       bordercolor='#f39c12',
                       background='#f39c12',
                       lightcolor='#f39c12',
                       darkcolor='#f39c12')
        
        # 紅色進度條（危險狀態）
        style.configure("Red.Horizontal.TProgressbar",
                       troughcolor='#ecf0f1',
                       bordercolor='#e74c3c', 
                       background='#e74c3c',
                       lightcolor='#e74c3c',
                       darkcolor='#e74c3c')
        
        # 預設進度條
        style.configure("Custom.Horizontal.TProgressbar",
                       troughcolor='#ecf0f1',
                       bordercolor='#3498db',
                       background='#3498db',
                       lightcolor='#3498db',
                       darkcolor='#3498db')
    
    def run(self):
        """運行GUI"""
        # 設置進度條樣式
        self.setup_progressbar_styles()
        
        # 設置關閉事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 啟動主迴圈
        self.root.mainloop()
    
    def on_closing(self):
        """處理窗口關閉事件"""
        if self.character:
            if messagebox.askyesno("退出遊戲", "要在退出前儲存遊戲嗎？"):
                self.save_game()
        self.root.quit()


def main():
    """主程序入口"""
    try:
        app = BalanceGameGUI()
        app.run()
    except KeyboardInterrupt:
        print("\n遊戲被中斷，再見！")
    except Exception as e:
        messagebox.showerror("錯誤", f"發生錯誤: {e}")
        print(f"發生錯誤: {e}")


if __name__ == "__main__":
    main()