# 配置文件說明 - actions.yaml

## 📝 概述
`actions.yaml` 文件包含了減肥平衡遊戲的所有配置，包括行動定義和遊戲設定。你可以修改這個文件來自定義遊戲體驗。

## 🎮 行動配置 (actions)

每個行動包含以下屬性：

### 基本屬性
- **name** (字串): 行動名稱，顯示在遊戲界面中
- **description** (字串): 行動描述，解釋這個行動的內容
- **energy_cost** (數字): 體力消耗，目前未使用但保留為未來功能

### 效果配置 (effects)
effects 部分定義行動對各項指數的影響：

- **weight** (浮點數): 對體重的影響 (kg)
  - 負數 = 減重
  - 正數 = 增重
  - 範例: -0.5 表示減重0.5kg

- **health** (整數): 對健康的影響 (0-100)
  - 正數 = 增加健康
  - 負數 = 減少健康
  - 範例: 8 表示增加8點健康

- **happiness** (整數): 對快樂的影響 (0-100)
  - 正數 = 增加快樂
  - 負數 = 減少快樂

- **wealth** (整數): 對財富的影響 (0-100)
  - 正數 = 增加財富
  - 負數 = 減少財富

- **knowledge** (整數): 對知識的影響 (0-100)
  - 正數 = 增加知識
  - 負數 = 減少知識

- **social** (整數): 對社交的影響 (0-100)
  - 正數 = 增加社交
  - 負數 = 減少社交

### 行動範例
```yaml
- name: "運動"
  description: "去健身房運動1小時"
  effects:
    weight: -0.5      # 減重0.5kg
    health: 8         # 增加8點健康
    happiness: -3     # 減少3點快樂
  energy_cost: 15     # 體力消耗15點
```

## ⚙️ 遊戲設定 (game_settings)

### 初始數值 (initial_stats)
定義角色開始時的各項指數：
```yaml
initial_stats:
  weight: 80.0        # 初始體重 (kg)
  health: 50          # 初始健康 (0-100)
  happiness: 50       # 初始快樂 (0-100)
  wealth: 50          # 初始財富 (0-100)
  knowledge: 50       # 初始知識 (0-100)
  social: 50          # 初始社交 (0-100)
```

### 遊戲目標
- **target_weight** (浮點數): 目標體重 (kg)
- **max_days** (整數): 最大遊戲天數

### 失敗條件 (failure_thresholds)
定義什麼情況下遊戲失敗：
```yaml
failure_thresholds:
  health: 10          # 健康低於此值會失敗
  happiness: 10       # 快樂低於此值會失敗
```

### 數值限制 (stat_limits)
定義各項指數的最大最小值：
```yaml
stat_limits:
  weight_min: 40.0    # 最低體重
  weight_max: 150.0   # 最高體重
  stat_min: 0         # 其他指數最小值
  stat_max: 100       # 其他指數最大值
```

## 🎲 隨機事件系統 (random_events)

### 隨機事件配置
```yaml
random_events:
  probability: 0.3    # 每日隨機事件觸發機率 (0.0-1.0)
  events:             # 隨機事件列表
    - name: "事件名稱"
      description: "事件描述文字"
      effects:          # 對指數的影響
        happiness: 3
        social: 2
      weight: 15        # 事件權重，數字越大越容易發生
```

### 事件權重系統
- 權重越高的事件越容易被選中
- 權重為相對值，總和會自動計算
- 建議範圍：1-20

### 隨機事件示例
```yaml
events:
  - name: "朋友鼓勵"
    description: "收到朋友的鼓勵訊息！"
    effects:
      happiness: 3
      social: 2
    weight: 15          # 高權重，經常發生
    
  - name: "意外收穫"
    description: "路上撿到零錢"
    effects:
      wealth: 2
      happiness: 1
    weight: 5           # 低權重，偶爾發生
```

## 🎯 條件事件系統 (conditional_events)

### 條件事件結構
```yaml
conditional_events:
  - condition:          # 觸發條件
      stat: "health"    # 檢查的指數
      operator: "<"     # 比較運算子
      value: 20         # 閾值
    event:              # 觸發的事件
      name: "疲倦狀態"
      description: "因為健康狀況不佳，今天感到很疲倦..."
      effects:
        happiness: -5
    probability: 0.8    # 滿足條件時的觸發機率
```

### 支援的運算子
- `<` : 小於
- `>` : 大於  
- `<=` : 小於等於
- `>=` : 大於等於
- `==` : 等於
- `!=` : 不等於

### 條件事件示例
```yaml
# 低健康警告
- condition:
    stat: "health"
    operator: "<"
    value: 20
  event:
    name: "疲倦狀態"
    description: "因為健康狀況不佳，今天感到很疲倦..."
    effects:
      happiness: -5
  probability: 0.8

# 高社交獎勵
- condition:
    stat: "social"
    operator: ">"
    value: 80
  event:
    name: "朋友關懷"
    description: "朋友們都很關心你的近況，感覺很溫暖！"
    effects:
      happiness: 3
  probability: 0.5
```

## 🎯 自定義建議

### 1. 調整難度
- **增加難度**: 降低positive effects，增加negative effects
- **降低難度**: 增加positive effects，降低negative effects
- **延長遊戲**: 增加 max_days
- **縮短遊戲**: 減少 max_days

### 2. 添加新行動
```yaml
- name: "游泳"
  description: "在泳池游泳45分鐘"
  effects:
    weight: -0.4
    health: 6
    happiness: 4
    social: 2
  energy_cost: 12
```

### 3. 自定義隨機事件
```yaml
# 添加季節性事件
- name: "春天來臨"
  description: "春暖花開，心情特別好"
  effects:
    happiness: 5
    health: 2
  weight: 8

# 添加挑戰事件
- name: "食物中毒"
  description: "吃壞肚子，身體不適"
  effects:
    health: -5
    happiness: -3
  weight: 3
```

### 4. 創建條件事件鏈
```yaml
# 體重進展獎勵
- condition:
    stat: "weight"
    operator: "<="
    value: 70
  event:
    name: "減重里程碑"
    description: "達到重要的減重里程碑！"
    effects:
      happiness: 6
      social: 3
  probability: 1.0
```

### 5. 平衡調整
- 確保有足夠的減重行動
- 平衡正面和負面效果
- 考慮行動之間的相互配合
- 調整隨機事件的頻率和影響

### 6. 主題變化
你可以修改行動來適應不同主題：
- **學習主題**: 專注於知識和技能
- **社交主題**: 專注於人際關係
- **健康主題**: 專注於身心健康

## 🎮 事件系統技巧

### 權重設計原則
- **正面事件**: 權重15-20（經常發生，提升體驗）
- **中性事件**: 權重8-12（適度發生）
- **負面事件**: 權重3-8（偶爾發生，增加挑戰）

### 條件事件設計
- **低指數警告**: 高機率觸發，提醒玩家注意
- **高指數獎勵**: 中等機率，鼓勵玩家維持
- **特殊里程碑**: 一次性觸發，慶祝成就

### 事件平衡建議
- 每個指數都應該有相關的隨機事件
- 正負面事件的總體影響應該平衡
- 條件事件應該有意義且符合邏輯

## ⚠️ 注意事項

### 文件格式
- 使用正確的YAML縮排（2個空格）
- 字串使用雙引號包圍
- 數字不需要引號
- 注意冒號後面要有空格

### 數值平衡
- 體重變化建議在 -1.0 到 +1.0 之間
- 其他指數變化建議在 -10 到 +10 之間
- 避免過於極端的數值

### 測試配置
修改配置後建議：
1. 重啟遊戲測試
2. 玩幾天觀察平衡性
3. 根據體驗調整數值

## 🔧 故障排除

### 常見錯誤
1. **YAML語法錯誤**: 檢查縮排和語法
2. **數值類型錯誤**: 確保數字不用引號包圍
3. **缺少必要屬性**: 確保每個行動都有 name, description, effects

### 恢復預設
如果配置出現問題，刪除 `config/actions.yaml` 文件，遊戲會自動使用預設配置。

## 💡 進階技巧

### 1. 條件效果
雖然目前不支援，但未來可能添加基於當前狀態的條件效果。

### 2. 隨機效果
考慮添加效果範圍，讓同一行動有不同的結果。

### 3. 季節變化
可以創建不同的配置文件來模擬季節性變化。