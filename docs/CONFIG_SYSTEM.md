# ⚙️ 配置系統完全指南

YAML驅動的完全可自定義遊戲體驗系統

## 📋 目錄
- [🎯 系統概述](#-系統概述)
- [📁 配置文件結構](#-配置文件結構)
- [🎮 行動配置](#-行動配置)
- [🎲 隨機事件系統](#-隨機事件系統)
- [⚙️ 遊戲設定](#-遊戲設定)
- [🔧 配置管理工具](#-配置管理工具)
- [🛠️ 自定義創建](#-自定義創建)
- [💡 最佳實踐](#-最佳實踐)

## 🎯 系統概述

### ✨ 核心理念
> **"讓每一個玩家都能創造屬於自己的遊戲體驗"**

配置系統讓您能夠：
- **🎮 自定義所有行動** - 修改行動效果和描述
- **🎲 設計隨機事件** - 創建獨特的事件系統
- **⚙️ 調整遊戲難度** - 修改目標和限制條件
- **🔄 快速切換模式** - 預設多種遊戲配置

### 🏗️ 技術架構
```
YAML配置系統架構:
├── 配置文件 (.yaml)
│   ├── 行動定義 (actions)
│   ├── 遊戲設定 (game_settings) 
│   ├── 隨機事件 (random_events)
│   └── 條件事件 (conditional_events)
├── 配置管理器 (config_manager.py)
│   ├── 配置載入與驗證
│   ├── 配置切換與備份
│   └── 配置創建與編輯
└── 遊戲引擎整合
    ├── 動態載入配置
    ├── 即時應用變更
    └── 錯誤處理與回退
```

## 📁 配置文件結構

### 🗂️ 文件組織
```
config/
├── actions.yaml          # 主配置文件（困難模式）
├── actions_hard.yaml     # 困難模式配置
├── actions_standard.yaml # 標準模式配置  
├── CONFIG_GUIDE.md      # 配置說明文件
└── [自定義配置].yaml    # 用戶自定義配置
```

### 📋 配置模式對比
| 特性 | 標準模式 | 困難模式 | 自定義模式 |
|------|----------|----------|------------|
| **難度** | 適中 | 困難 | 完全自定義 |
| **隨機事件** | 12個 | 12個 | 可自定義 |
| **條件事件** | 8個 | 8個 | 可自定義 |
| **初始體重** | 80kg | 80kg | 可調整 |
| **目標體重** | 65kg | 65kg | 可調整 |
| **遊戲天數** | 100天 | 100天 | 可調整 |
| **失敗閾值** | 20 | 10 | 可調整 |

### 🔄 配置切換
```bash
# 使用配置管理工具
config_manager.bat

# 或直接運行
python config_manager.py

# 操作選項:
1. 查看當前配置
2. 切換到標準模式  
3. 切換到困難模式
4. 列出所有配置
5. 創建新配置
```

## 🎮 行動配置

### 📝 基本結構
```yaml
actions:
  - name: "行動名稱"           # 顯示名稱
    description: "行動描述"     # 詳細說明
    effects:                   # 效果定義
      weight: 0.0             # 體重變化 (kg)
      health: 0               # 健康變化 (0-100)
      happiness: 0            # 快樂變化 (0-100)
      wealth: 0               # 財富變化 (0-100) 
      knowledge: 0            # 知識變化 (0-100)
      social: 0               # 社交變化 (0-100)
    energy_cost: 0            # 體力消耗 (保留字段)
```

### 🎯 行動設計原則

#### 平衡性原則
```yaml
# ✅ 良好的平衡設計
- name: "慢跑"
  description: "在公園慢跑30分鐘"
  effects:
    weight: -0.3     # 適度減重
    health: 5        # 提升健康
    happiness: 2     # 輕微快樂
    social: 2        # 社交接觸
    
# ❌ 過度強力的設計  
- name: "超級運動"
  description: "瘋狂運動"
  effects:
    weight: -2.0     # 減重過快
    health: 20       # 提升過多
    happiness: -10   # 懲罰過重
```

#### 主題一致性
```yaml
# 🏃‍♂️ 運動主題
- name: "運動"
  effects:
    weight: -0.5     # 主要效果：減重
    health: 8        # 正面效果：健康
    happiness: -3    # 代價：疲勞
    
# 📚 學習主題  
- name: "學習"
  effects:
    knowledge: 15    # 主要效果：知識
    happiness: 2     # 正面效果：成就感
    social: 0        # 中性：無社交影響
```

### 📊 效果數值指南

#### 體重變化 (weight)
```yaml
極強減重: -0.8 ~ -1.0    # 危險，可能過快
強力減重: -0.5 ~ -0.7    # 有效，但需平衡
適度減重: -0.2 ~ -0.4    # 安全，可持續  
輕微減重: -0.1 ~ -0.1    # 溫和，長期效果
維持體重: 0              # 無變化
輕微增重: 0.1 ~ 0.2      # 小幅增長
明顯增重: 0.3 ~ 0.5      # 需要注意
```

#### 其他指數 (0-100)
```yaml
極大變化: ±15 ~ ±20      # 戲劇性效果
大幅變化: ±8 ~ ±12       # 顯著影響
適度變化: ±3 ~ ±6        # 平衡效果
輕微變化: ±1 ~ ±2        # 細微調整
無變化:   0              # 不影響該指數
```

### 🎨 創意行動示例

#### 季節性行動
```yaml
- name: "春季踏青"
  description: "到郊外欣賞櫻花，呼吸新鮮空氣"
  effects:
    happiness: 8
    health: 3
    social: 4
    knowledge: 1     # 接觸自然知識
    
- name: "夏日游泳"  
  description: "在游泳池暢游，消暑健身"
  effects:
    weight: -0.4
    health: 6
    happiness: 5
    social: 3
    
- name: "秋季登山"
  description: "登高望遠，鍛煉意志力"
  effects:
    weight: -0.6
    health: 8  
    happiness: 4
    knowledge: 2     # 意志力學習
    
- name: "冬日滑雪"
  description: "雪地運動，挑戰自我極限"
  effects:
    weight: -0.5
    health: 7
    happiness: 6
    wealth: -5       # 滑雪費用
```

#### 職業特色行動  
```yaml
- name: "程式設計"
  description: "專注開發項目，提升技能"
  effects:
    knowledge: 12
    wealth: 8        # 技能提升帶來收入
    health: -2       # 久坐傷害
    social: -1       # 減少社交
    
- name: "創意設計"
  description: "發揮創造力，完成設計作品"  
  effects:
    knowledge: 8
    happiness: 6     # 創作快樂
    wealth: 5        # 作品收入
    social: 2        # 與客戶交流
```

## 🎲 隨機事件系統

### 🎯 事件系統架構
```yaml
random_events:
  probability: 0.3           # 每日觸發機率
  events:                    # 權重隨機事件列表
    - name: "事件名稱"
      description: "事件描述"
      effects: {...}
      weight: 15             # 事件權重
      
conditional_events:          # 條件觸發事件
  - condition:               # 觸發條件
      stat: "health"
      operator: "<"
      value: 30
    event:                   # 事件內容
      name: "事件名稱" 
      description: "事件描述"
      effects: {...}
    probability: 0.8         # 條件滿足時的觸發機率
```

### 🎲 隨機事件設計

#### 權重分配策略
```yaml
高頻事件 (權重 15-20):
- 正面日常事件
- 鼓勵性事件
- 平衡遊戲體驗

中頻事件 (權重 8-12):
- 中性事件
- 輕微挑戰
- 狀態微調

低頻事件 (權重 3-7):
- 負面挑戰  
- 特殊獎勵
- 劇情性事件

稀有事件 (權重 1-2):
- 大獎或災難
- 劇情轉折
- 記憶深刻
```

#### 事件平衡原則
```yaml
# ✅ 平衡的正面事件
- name: "朋友鼓勵"
  description: "收到朋友的溫暖鼓勵訊息"
  effects:
    happiness: 3      # 適度提升
    social: 2         # 相關增益
  weight: 15          # 高頻出現

# ✅ 平衡的負面事件  
- name: "輕微感冒"
  description: "有點感冒症狀，身體不適"
  effects:
    health: -3        # 適度影響
    happiness: -1     # 連帶影響
  weight: 5           # 低頻出現
  
# ❌ 過度極端事件
- name: "中樂透"  
  description: "意外中了大獎！"
  effects:
    wealth: 50        # 影響過大
    happiness: 30     # 破壞平衡
  weight: 1           # 即使稀有也太強
```

### 🎯 條件事件設計

#### 支援的運算子
```yaml
條件運算子:
"<"  : 小於
">"  : 大於  
"<=" : 小於等於
">=" : 大於等於
"==" : 等於
"!=" : 不等於
```

#### 條件事件範例
```yaml
# 健康預警系統
- condition:
    stat: "health" 
    operator: "<"
    value: 25
  event:
    name: "身體警訊"
    description: "身體發出警告，感到非常疲憊"
    effects:
      happiness: -5
      health: -2      # 惡化趨勢
  probability: 0.9    # 高機率觸發
  
# 成就獎勵系統
- condition:
    stat: "knowledge"
    operator: ">="  
    value: 80
  event:
    name: "學識淵博"
    description: "因為豐富的知識獲得工作機會"
    effects:
      wealth: 8
      happiness: 3
      social: 2
  probability: 0.6    # 適中機率

# 社交效應系統
- condition:
    stat: "social"
    operator: ">="
    value: 85
  event: 
    name: "人氣王"
    description: "朋友圈的人氣很高，大家都想約你"
    effects:
      happiness: 5
      social: 2
      wealth: -3      # 社交開銷
  probability: 0.7
```

### 🎨 創意事件設計

#### 連鎖事件系統
```yaml
# 感冒康復連鎖
- name: "感冒初期"
  effects: { health: -5, happiness: -2 }
  # 後續可能觸發康復事件

- condition: { stat: "health", operator: ">", value: 60 }
  event:
    name: "感冒康復"  
    description: "感冒好了，身體恢復活力"
    effects: { happiness: 4, health: 2 }
```

#### 季節主題事件
```yaml
# 春季事件
- name: "春暖花開"
  description: "春天到了，心情特別舒暢"
  effects: { happiness: 4, health: 2 }
  weight: 10
  
# 夏季事件  
- name: "夏日炎炎"
  description: "天氣太熱，有點無精打采"
  effects: { happiness: -2, health: -1 }
  weight: 8
```

## ⚙️ 遊戲設定

### 🎮 基本設定結構
```yaml
game_settings:
  initial_stats:          # 初始數值
    weight: 80.0
    health: 50
    happiness: 50  
    wealth: 50
    knowledge: 50
    social: 50
    
  target_weight: 65.0     # 目標體重
  max_days: 100          # 最大天數
  
  failure_thresholds:     # 失敗條件
    health: 20
    happiness: 20
    
  stat_limits:            # 數值限制
    weight_min: 40.0
    weight_max: 150.0
    stat_min: 0
    stat_max: 100
    
  difficulty_modifiers:   # 難度調整
    event_impact: 1.0     # 事件影響倍數
    action_efficiency: 1.0 # 行動效率倍數
```

### 🎯 難度設計指南

#### 簡單模式設定
```yaml
game_settings:
  initial_stats:
    weight: 75.0          # 更接近目標
    health: 60            # 更高初始值
    happiness: 60
    wealth: 60
  
  target_weight: 65.0     # 減重10kg
  max_days: 120          # 更多時間
  
  failure_thresholds:
    health: 25            # 更寬鬆
    happiness: 25
    
  difficulty_modifiers:
    event_impact: 0.8     # 事件影響較小
    action_efficiency: 1.2 # 行動效果更好
```

#### 困難模式設定  
```yaml
game_settings:
  initial_stats:
    weight: 85.0          # 更重的起點
    health: 40            # 較低初始值
    happiness: 40
    wealth: 40
  
  target_weight: 65.0     # 減重20kg
  max_days: 80           # 更少時間
  
  failure_thresholds:  
    health: 10            # 更嚴格
    happiness: 10
    
  difficulty_modifiers:
    event_impact: 1.3     # 事件影響更大
    action_efficiency: 0.8 # 行動效果較差
```

#### 專家模式設定
```yaml
game_settings:
  initial_stats:
    weight: 90.0          # 極重起點
    health: 30            # 很低初始值
    happiness: 30
    wealth: 20            # 經濟困難
    
  target_weight: 65.0     # 減重25kg
  max_days: 60           # 極少時間
  
  failure_thresholds:
    health: 5             # 極嚴格
    happiness: 5
    wealth: 0             # 新增財富失敗條件
    
  additional_rules:       # 額外規則
    daily_decay:          # 每日衰減
      health: -1
      happiness: -1
    achievement_required: # 成就要求
      min_knowledge: 60
      min_social: 40
```

## 🔧 配置管理工具

### 🛠️ config_manager.py 功能

#### 主要功能列表
```python
功能選單:
1. 查看當前配置    # 顯示正在使用的配置
2. 列出所有配置    # 顯示可用的配置文件
3. 切換配置       # 更改活動配置
4. 創建新配置     # 複製並修改配置
5. 備份配置       # 保存當前配置副本
6. 恢復配置       # 從備份恢復
7. 驗證配置       # 檢查配置文件正確性
8. 配置對比       # 比較不同配置差異
```

#### 使用方法
```bash
# 啟動配置管理器
python config_manager.py

# 或使用批次檔 (Windows)
config_manager.bat

# 選擇操作:
請選擇操作：
1. 查看當前配置
2. 切換到標準模式
3. 切換到困難模式  
4. 列出所有配置
5. 創建新配置
6. 退出
```

### 📋 配置驗證系統

#### 自動驗證規則
```python
驗證檢查項目:
✓ YAML語法正確性
✓ 必要字段存在性  
✓ 數據類型正確性
✓ 數值範圍合理性
✓ 邏輯一致性檢查
✓ 平衡性警告提示

錯誤處理:
❌ 語法錯誤 → 顯示具體行號
❌ 缺少字段 → 列出遺失項目  
❌ 類型錯誤 → 說明期望類型
❌ 範圍錯誤 → 提供建議值
⚠️ 平衡警告 → 提醒潛在問題
```

#### 驗證結果示例
```
配置驗證結果:
✅ YAML格式: 正確
✅ 基本結構: 完整
✅ 行動配置: 10個行動，格式正確
⚠️ 平衡性警告: 
   - "超級運動" 減重效果可能過強 (-1.2kg)
   - "工作" 健康懲罰可能過重 (-8)
✅ 遊戲設定: 數值範圍合理
✅ 隨機事件: 12個事件，權重總計110
```

## 🛠️ 自定義創建

### 🎨 創建個人專屬配置

#### 步驟1: 複製基礎配置
```bash
# 使用配置管理器創建
python config_manager.py
# 選擇 "5. 創建新配置"
# 輸入新配置名稱: my_custom_config
# 選擇基於的模板: standard/hard
```

#### 步驟2: 修改行動配置
```yaml
# 個人化行動範例
actions:
  # 添加個人喜好的運動
  - name: "瑜伽"
    description: "進行1小時的瑜伽練習，身心平靜"
    effects:
      weight: -0.2
      health: 4
      happiness: 6
      knowledge: 2      # 身心靈知識
      social: -1        # 獨處時間
      
  # 添加職業相關活動  
  - name: "寫程式"
    description: "專注編程，提升技能和收入"
    effects:
      knowledge: 10
      wealth: 6
      health: -3        # 久坐傷害
      social: -2        # 減少社交
      happiness: 3      # 成就感
```

#### 步驟3: 設計專屬事件
```yaml
# 程式設計師專屬事件
random_events:
  events:
    - name: "代碼通過審核"
      description: "寫的代碼獲得團隊讚賞！"
      effects:
        happiness: 5
        wealth: 3
        knowledge: 2
      weight: 8
      
    - name: "遇到Bug"
      description: "代碼出現難以解決的Bug..."
      effects:
        happiness: -3
        health: -1      # 壓力影響
      weight: 6
```

#### 步驟4: 調整遊戲設定
```yaml
# 適合自己的難度設定
game_settings:
  initial_stats:
    weight: 78.0        # 根據實際情況
    health: 45          # 程式設計師通常較低
    knowledge: 70       # 專業技能較高
    social: 35          # 社交可能較少
    
  max_days: 90          # 適合的時間長度
  
  failure_thresholds:
    health: 15          # 考慮職業特性
    happiness: 15
```

### 🎯 主題化配置創建

#### 學生主題配置
```yaml
# 專為學生設計的配置
actions:
  - name: "上課"
    description: "認真聽課，學習新知識"
    effects:
      knowledge: 12
      happiness: 1
      social: 3
      wealth: -1        # 學費開銷
      
  - name: "兼職工作"  
    description: "課餘時間打工賺取生活費"
    effects:
      wealth: 8
      knowledge: 2      # 工作經驗
      health: -3        # 疲勞
      social: 4         # 職場社交

game_settings:
  initial_stats:
    wealth: 30          # 學生經濟狀況
    knowledge: 40       # 正在學習中
    social: 60          # 校園生活
```

#### 家庭主婦主題配置
```yaml
actions:
  - name: "照顧家庭"
    description: "處理家務，照顧家人"
    effects:
      happiness: 4      # 家庭溫暖
      health: 2         # 適度活動
      social: 2         # 家庭社交
      knowledge: 1      # 生活智慧
      weight: 0.1       # 輕微增重
      
  - name: "親子活動"
    description: "和孩子一起玩耍運動"
    effects:
      happiness: 8      # 親子快樂
      social: 5         # 家庭關係
      health: 3         # 陪玩運動
      weight: -0.2      # 輕度運動
```

### 🌟 創意配置點子

#### 科幻主題配置
```yaml
# 未來世界的減肥遊戲
actions:
  - name: "全息健身"
    description: "使用全息技術進行虛擬健身"
    effects:
      weight: -0.6
      health: 10
      happiness: 5
      knowledge: 3      # 科技知識
      
  - name: "腦力增強"
    description: "使用神經接口提升腦力"
    effects:
      knowledge: 20
      wealth: 5
      health: -1        # 腦部負荷
      social: -3        # 脫離現實
```

#### 奇幻主題配置
```yaml  
# 魔法世界的冒險
actions:
  - name: "魔法修練"
    description: "學習新的魔法咒語"
    effects:
      knowledge: 15     # 魔法知識
      happiness: 6      # 成就感
      health: 2         # 魔力提升身體
      social: -2        # 獨自修練
      
  - name: "冒險探索"
    description: "前往未知領域探險"
    effects:
      weight: -0.4      # 體力活動
      health: 6         # 鍛煉身體
      happiness: 8      # 冒險刺激
      wealth: 10        # 找到寶藏
      social: 5         # 隊友情誼
```

## 💡 最佳實踐

### 🎯 設計原則

#### 1. 平衡性第一
```yaml
設計檢查清單:
□ 沒有過度強力的行動 (單項效果 > ±15)
□ 負面效果有合理補償
□ 正面效果有適當代價  
□ 整體趨勢支持遊戲目標
□ 隨機事件不會破壞平衡
```

#### 2. 主題一致性
```yaml
主題對齊檢查:
□ 行動名稱與效果邏輯一致
□ 描述文字生動具體
□ 事件符合遊戲世界觀
□ 數值符合現實邏輯
□ 整體風格統一協調
```

#### 3. 玩家體驗優先
```yaml
體驗設計考量:
□ 提供清晰的策略選擇
□ 避免過於複雜的計算
□ 保持適度的挑戰性
□ 給予及時的反饋
□ 支持不同遊戲風格
```

### 🔧 測試與調優

#### 測試流程
```
1. 語法驗證
   └── 使用 config_manager.py 驗證

2. 數值測試  
   └── 快速遊戲測試各種策略

3. 平衡性測試
   └── 多次完整遊戲，記錄結果

4. 用戶測試
   └── 邀請其他人試玩並收集反馈

5. 迭代改進
   └── 根據測試結果調整配置
```

#### 調優技巧
```yaml
常見問題與解決:

問題: 遊戲過於簡單
解決: 
- 降低初始數值
- 提高失敗閾值  
- 增加負面事件權重
- 減少行動效果

問題: 遊戲過於困難
解決:
- 提高初始數值
- 降低失敗閾值
- 增加正面事件權重  
- 增強行動效果

問題: 策略單一
解決:
- 平衡各行動效果
- 增加條件事件
- 添加多樣化行動
- 調整數值上限
```

### 📊 數據分析工具

#### 配置分析腳本
```python
# config_analyzer.py (概念)
def analyze_config(config_file):
    """分析配置文件的平衡性"""
    
    # 行動效果統計
    weight_effects = []
    health_effects = []
    # ... 收集數據
    
    # 計算指標
    balance_score = calculate_balance(effects)
    difficulty_rating = estimate_difficulty(settings)
    
    # 生成報告
    return {
        'balance_score': balance_score,
        'difficulty_rating': difficulty_rating,  
        'recommendations': get_recommendations()
    }
```

#### 遊戲數據追蹤
```yaml
# 在配置中添加數據追蹤
analytics:
  track_player_choices: true    # 追蹤玩家選擇偏好
  track_success_rate: true      # 追蹤成功率
  track_failure_points: true    # 追蹤失敗原因
  generate_heatmap: true        # 生成行動熱力圖
```

### 🤝 社區分享

#### 配置分享格式
```yaml
# 配置文件頭部添加元資料
meta:
  name: "程式設計師減肥挑戰"
  author: "YourName"  
  version: "1.2"
  description: "專為程式設計師設計的減肥遊戲配置"
  difficulty: "中等"
  estimated_time: "90-100天"
  tags: ["程式設計師", "職場", "平衡"]
  
# 配置說明
readme: |
  這個配置專為程式設計師群體設計，考慮到：
  - 久坐的工作特性
  - 較高的知識基礎
  - 相對較少的社交活動
  - 通過技術手段改善健康的傾向
  
  建議策略：
  - 平衡工作與健康
  - 利用知識優勢
  - 注意社交需求
```

#### 社區貢獻指南
```
貢獻流程:
1. Fork 專案
2. 創建特色配置
3. 測試並文檔化
4. 提交 Pull Request
5. 社區審核與合併

配置質量標準:
✓ 平衡性測試通過
✓ 主題明確一致
✓ 文檔說明完整
✓ 至少經過3次完整測試
✓ 提供策略建議
```

---

**配置系統讓您完全掌控遊戲體驗！創造屬於自己的減肥挑戰，享受個性化的遊戲樂趣！** ⚙️✨

**立即開始自定義您的配置！** 🛠️🎮