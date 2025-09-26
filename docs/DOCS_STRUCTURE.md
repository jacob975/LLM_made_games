# 文檔重構計劃

## 📚 文檔分類與重構

### 核心文檔 (保留並優化)
1. `README.md` - 主要介紹文檔
2. `PROJECT_OVERVIEW.md` - 專案總覽

### 使用指南類
3. `GETTING_STARTED.md` - 快速開始指南 (新建)
4. `GUI_GUIDE.md` - GUI使用說明
5. `GAMEPLAY_STRATEGY.md` - 遊戲玩法與策略 (合併 GAMEPLAY.md + game_strategy.md)

### 功能說明類
6. `CHARACTER_AVATAR_SYSTEM.md` - 主角造型系統 (重構)
7. `CONFIG_SYSTEM.md` - 配置系統說明 (移動並重構 config/CONFIG_GUIDE.md)

### 開發文檔類  
8. `DEVELOPMENT_REPORTS.md` - 開發報告合集 (合併所有報告類文檔)
9. `API_REFERENCE.md` - API參考文檔 (新建)

### 需要合併/刪除的文檔
- YAML_IMPLEMENTATION_REPORT.md → 合併到 DEVELOPMENT_REPORTS.md
- RANDOM_EVENTS_REPORT.md → 合併到 DEVELOPMENT_REPORTS.md  
- CHARACTER_SYSTEM_COMPLETION_REPORT.md → 合併到 DEVELOPMENT_REPORTS.md
- GAMEPLAY.md + game_strategy.md → 合併為 GAMEPLAY_STRATEGY.md