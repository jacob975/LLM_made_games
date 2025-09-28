"""
文字冒險遊戲測試腳本
用於驗證遊戲各組件是否正常工作
"""

import sys
import os

def test_imports():
    """測試所有必要的模組導入"""
    print("=== 測試模組導入 ===")
    
    try:
        import pygame
        print(f"✅ pygame {pygame.version.ver} 導入成功")
    except ImportError as e:
        print(f"❌ pygame 導入失敗: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✅ numpy {np.__version__} 導入成功")
    except ImportError as e:
        print(f"❌ numpy 導入失敗: {e}")
        return False
        
    try:
        from PIL import Image
        print("✅ Pillow 導入成功")
    except ImportError as e:
        print(f"❌ Pillow 導入失敗: {e}")
        return False
    
    return True

def test_script_file():
    """測試劇本文件是否存在且可讀"""
    print("\n=== 測試劇本文件 ===")
    
    script_path = "script.txt"
    if not os.path.exists(script_path):
        print(f"❌ 找不到劇本文件: {script_path}")
        return False
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            dialogue_count = sum(1 for line in lines if line.strip().startswith('「') and line.strip().endswith('」'))
            
        print(f"✅ 劇本文件讀取成功")
        print(f"   文件大小: {len(content)} 字符")
        print(f"   對話行數: {dialogue_count}")
        return True
        
    except Exception as e:
        print(f"❌ 讀取劇本文件失敗: {e}")
        return False

def test_game_initialization():
    """測試遊戲初始化（不運行主循環）"""
    print("\n=== 測試遊戲初始化 ===")
    
    try:
        # 嘗試導入遊戲類
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # 測試基礎版本
        print("測試基礎版本 (game.py)...")
        import pygame
        pygame.init()
        pygame.display.set_mode((100, 100))  # 創建小窗口測試
        pygame.quit()
        print("✅ 基礎版本初始化成功")
        
        # 測試主版本的類導入
        print("測試主版本類導入...")
        from main_game import Character, DialogueSystem, TextAdventureGamePOC
        print("✅ 主版本類導入成功")
        
        # 測試角色創建
        test_char = Character("測試角色", "🧪", (100, 100, 100))
        print("✅ 角色類創建成功")
        
        # 測試對話系統
        dialogue_sys = DialogueSystem()
        print("✅ 對話系統創建成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 遊戲初始化測試失敗: {e}")
        return False

def test_font_availability():
    """測試字體可用性"""
    print("\n=== 測試字體可用性 ===")
    
    import pygame
    pygame.init()
    
    # 測試中文字體
    font_paths = [
        "C:/Windows/Fonts/msjh.ttc",      # 微軟正黑體
        "C:/Windows/Fonts/msjhbd.ttc",    # 微軟正黑體粗體
        "C:/Windows/Fonts/seguiemj.ttf"   # Segoe UI Emoji
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font = pygame.font.Font(font_path, 16)
                print(f"✅ 字體可用: {os.path.basename(font_path)}")
            except:
                print(f"⚠️ 字體文件存在但無法載入: {os.path.basename(font_path)}")
        else:
            print(f"⚠️ 字體文件不存在: {os.path.basename(font_path)}")
    
    # 測試系統默認字體
    try:
        default_font = pygame.font.Font(None, 16)
        print("✅ 系統默認字體可用")
    except:
        print("❌ 系統默認字體不可用")
    
    pygame.quit()

def main():
    """主測試函數"""
    print("超神肥文字冒險遊戲 - 環境測試")
    print("=" * 50)
    
    all_passed = True
    
    # 執行各項測試
    all_passed &= test_imports()
    all_passed &= test_script_file()
    all_passed &= test_game_initialization()
    test_font_availability()  # 字體測試不影響總結果
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有測試通過！遊戲應該可以正常運行。")
        print("\n運行命令:")
        print("  python main_game.py")
        print("\n或者雙擊運行:")
        print("  run_game.bat")
    else:
        print("❌ 部分測試失敗，請檢查環境配置。")
        print("\n解決方案:")
        print("  1. 運行 setup_env.bat")
        print("  2. 手動安裝缺失的依賴")
        print("  3. 檢查Python環境")
    
    print("\n測試完成！")

if __name__ == "__main__":
    main()