#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理工具 - 減肥平衡遊戲
用於切換和管理不同的遊戲配置文件
"""

import os
import shutil
import yaml
from pathlib import Path

class ConfigManager:
    """遊戲配置管理器"""
    
    def __init__(self):
        self.config_dir = Path(__file__).parent / "config"
        self.current_config = self.config_dir / "actions.yaml"
        
    def list_configs(self):
        """列出所有可用的配置文件"""
        configs = []
        for file in self.config_dir.glob("actions*.yaml"):
            configs.append(file.name)
        return sorted(configs)
    
    def get_config_info(self, config_file: str) -> dict:
        """獲取配置文件的基本信息"""
        config_path = self.config_dir / config_file
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            game_settings = config.get('game_settings', {})
            initial_stats = game_settings.get('initial_stats', {})
            
            info = {
                'actions_count': len(config.get('actions', [])),
                'initial_weight': initial_stats.get('weight', 'N/A'),
                'target_weight': game_settings.get('target_weight', 'N/A'),
                'max_days': game_settings.get('max_days', 'N/A'),
                'health_threshold': game_settings.get('failure_thresholds', {}).get('health', 'N/A'),
                'happiness_threshold': game_settings.get('failure_thresholds', {}).get('happiness', 'N/A')
            }
            return info
        except Exception as e:
            return {'error': str(e)}
    
    def switch_config(self, config_file: str) -> bool:
        """切換到指定的配置文件"""
        source_path = self.config_dir / config_file
        if not source_path.exists():
            return False
        
        try:
            # 備份當前配置
            if self.current_config.exists():
                backup_path = self.config_dir / "actions_backup.yaml"
                shutil.copy2(self.current_config, backup_path)
            
            # 切換配置
            shutil.copy2(source_path, self.current_config)
            return True
        except Exception:
            return False
    
    def create_custom_config(self, name: str, base_config: str = "actions.yaml") -> bool:
        """基於現有配置創建自定義配置"""
        base_path = self.config_dir / base_config
        new_path = self.config_dir / f"actions_{name}.yaml"
        
        if new_path.exists():
            return False
        
        try:
            shutil.copy2(base_path, new_path)
            return True
        except Exception:
            return False
    
    def show_menu(self):
        """顯示配置管理選單"""
        while True:
            print("\n" + "=" * 50)
            print("⚙️  遊戲配置管理工具")
            print("=" * 50)
            
            configs = self.list_configs()
            current_name = "actions.yaml"
            
            print("📋 可用配置:")
            for i, config in enumerate(configs, 1):
                info = self.get_config_info(config)
                status = " (當前)" if config == current_name else ""
                
                if 'error' not in info:
                    print(f"{i}. {config}{status}")
                    print(f"   行動數: {info['actions_count']}")
                    print(f"   目標: {info['initial_weight']}kg → {info['target_weight']}kg")
                    print(f"   時限: {info['max_days']}天")
                    print(f"   失敗線: 健康≤{info['health_threshold']}, 快樂≤{info['happiness_threshold']}")
                else:
                    print(f"{i}. {config}{status} (載入錯誤)")
            
            print(f"\n{len(configs)+1}. 創建自定義配置")
            print(f"{len(configs)+2}. 返回主選單")
            
            try:
                choice = input(f"\n請選擇 (1-{len(configs)+2}): ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(configs):
                    selected_config = configs[choice_num - 1]
                    if selected_config != current_name:
                        if self.switch_config(selected_config):
                            print(f"✅ 已切換到配置: {selected_config}")
                            print("重啟遊戲後生效。")
                        else:
                            print("❌ 切換配置失敗。")
                    else:
                        print("ℹ️ 已經是當前配置。")
                        
                elif choice_num == len(configs) + 1:
                    name = input("輸入自定義配置名稱: ").strip()
                    if name and name.isalnum():
                        base = input("基於哪個配置創建？(直接Enter使用預設): ").strip()
                        if not base:
                            base = "actions.yaml"
                        
                        if self.create_custom_config(name, base):
                            print(f"✅ 已創建自定義配置: actions_{name}.yaml")
                            print("可以編輯此文件來自定義遊戲。")
                        else:
                            print("❌ 創建配置失敗（可能已存在）。")
                    else:
                        print("❌ 配置名稱只能包含字母和數字。")
                        
                elif choice_num == len(configs) + 2:
                    break
                else:
                    print("無效的選擇。")
                    
                input("\n按 Enter 鍵繼續...")
                
            except ValueError:
                print("請輸入有效的數字。")
                input("\n按 Enter 鍵繼續...")
            except KeyboardInterrupt:
                print("\n\n退出配置管理工具。")
                break

def main():
    """主程序入口"""
    manager = ConfigManager()
    manager.show_menu()

if __name__ == "__main__":
    main()