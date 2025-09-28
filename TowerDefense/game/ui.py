"""
User Interface for the tower defense game
"""

import pygame
from config import *

class UI:
    """Handles all UI elements"""
    
    def __init__(self):
        self.panel_rect = pygame.Rect(
            SCREEN_WIDTH - UI_PANEL_WIDTH, 0, 
            UI_PANEL_WIDTH, UI_PANEL_HEIGHT
        )
        
        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Tower buttons
        self.tower_buttons = {
            "basic": pygame.Rect(SCREEN_WIDTH - 180, 100, 80, 40),
            "sniper": pygame.Rect(SCREEN_WIDTH - 90, 100, 80, 40),
            "machine_gun": pygame.Rect(SCREEN_WIDTH - 180, 150, 80, 40),
            "cannon": pygame.Rect(SCREEN_WIDTH - 90, 150, 80, 40),
        }
        
        # Control buttons
        self.start_wave_button = pygame.Rect(SCREEN_WIDTH - 180, 300, 160, 40)
        self.pause_button = pygame.Rect(SCREEN_WIDTH - 180, 350, 160, 40)
        
        self.selected_tower_type = "basic"
        
        # Tower info
        self.tower_info = {
            "basic": {"name": "Basic", "cost": 50, "damage": 25, "range": 80},
            "sniper": {"name": "Sniper", "cost": 100, "damage": 75, "range": 150},
            "machine_gun": {"name": "M.Gun", "cost": 75, "damage": 10, "range": 60},
            "cannon": {"name": "Cannon", "cost": 150, "damage": 100, "range": 90},
        }
    
    def handle_click(self, pos):
        """Handle mouse clicks on UI elements"""
        # Check tower buttons
        for tower_type, button_rect in self.tower_buttons.items():
            if button_rect.collidepoint(pos):
                self.selected_tower_type = tower_type
                return f"select_tower_{tower_type}"
        
        # Check control buttons
        if self.start_wave_button.collidepoint(pos):
            return "start_wave"
        
        if self.pause_button.collidepoint(pos):
            return "pause_game"
        
        return None
    
    def draw(self, screen, game_state):
        """Draw the UI panel"""
        # Draw panel background
        pygame.draw.rect(screen, LIGHT_GRAY, self.panel_rect)
        pygame.draw.rect(screen, BLACK, self.panel_rect, 2)
        
        # Draw game stats
        y_offset = 20
        
        # Money
        money_text = self.font_medium.render(f"Money: ${game_state.get('money', 0)}", 
                                           True, BLACK)
        screen.blit(money_text, (SCREEN_WIDTH - 190, y_offset))
        y_offset += 30
        
        # Lives
        lives_text = self.font_medium.render(f"Lives: {game_state.get('lives', 0)}", 
                                           True, BLACK)
        screen.blit(lives_text, (SCREEN_WIDTH - 190, y_offset))
        y_offset += 30
        
        # Wave info
        wave_text = self.font_medium.render(f"Wave: {game_state.get('wave', 1)}", 
                                          True, BLACK)
        screen.blit(wave_text, (SCREEN_WIDTH - 190, y_offset))
        y_offset += 40
        
        # Tower selection title
        title_text = self.font_medium.render("Select Tower:", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH - 190, y_offset))
        y_offset += 30
        
        # Draw tower buttons
        for tower_type, button_rect in self.tower_buttons.items():
            info = self.tower_info[tower_type]
            
            # Button background
            color = YELLOW if tower_type == self.selected_tower_type else WHITE
            pygame.draw.rect(screen, color, button_rect)
            pygame.draw.rect(screen, BLACK, button_rect, 2)
            
            # Button text
            name_text = self.font_small.render(info["name"], True, BLACK)
            cost_text = self.font_small.render(f"${info['cost']}", True, BLACK)
            
            # Center text in button
            name_rect = name_text.get_rect(center=(button_rect.centerx, button_rect.y + 12))
            cost_rect = cost_text.get_rect(center=(button_rect.centerx, button_rect.y + 28))
            
            screen.blit(name_text, name_rect)
            screen.blit(cost_text, cost_rect)
        
        # Tower stats for selected tower
        y_offset = 200
        selected_info = self.tower_info[self.selected_tower_type]
        stats_title = self.font_small.render("Tower Stats:", True, BLACK)
        screen.blit(stats_title, (SCREEN_WIDTH - 190, y_offset))
        y_offset += 20
        
        damage_text = self.font_small.render(f"Damage: {selected_info['damage']}", True, BLACK)
        screen.blit(damage_text, (SCREEN_WIDTH - 190, y_offset))
        y_offset += 15
        
        range_text = self.font_small.render(f"Range: {selected_info['range']}", True, BLACK)
        screen.blit(range_text, (SCREEN_WIDTH - 190, y_offset))
        y_offset += 15
        
        cost_text = self.font_small.render(f"Cost: ${selected_info['cost']}", True, BLACK)
        screen.blit(cost_text, (SCREEN_WIDTH - 190, y_offset))
        
        # Control buttons
        # Start wave button
        wave_color = GREEN if not game_state.get('wave_active', False) else GRAY
        pygame.draw.rect(screen, wave_color, self.start_wave_button)
        pygame.draw.rect(screen, BLACK, self.start_wave_button, 2)
        
        wave_button_text = "Start Wave" if not game_state.get('wave_active', False) else "Wave Active"
        wave_text = self.font_small.render(wave_button_text, True, BLACK)
        wave_text_rect = wave_text.get_rect(center=self.start_wave_button.center)
        screen.blit(wave_text, wave_text_rect)
        
        # Pause button
        pause_color = ORANGE if not game_state.get('paused', False) else RED
        pygame.draw.rect(screen, pause_color, self.pause_button)
        pygame.draw.rect(screen, BLACK, self.pause_button, 2)
        
        pause_button_text = "Pause" if not game_state.get('paused', False) else "Resume"
        pause_text = self.font_small.render(pause_button_text, True, BLACK)
        pause_text_rect = pause_text.get_rect(center=self.pause_button.center)
        screen.blit(pause_text, pause_text_rect)
        
        # Game over or victory message
        if game_state.get('game_over', False):
            game_over_text = self.font_large.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
        
        elif game_state.get('victory', False):
            victory_text = self.font_large.render("VICTORY!", True, GREEN)
            text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(victory_text, text_rect)