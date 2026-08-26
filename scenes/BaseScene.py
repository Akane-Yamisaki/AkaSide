import pygame
import config
from abc import ABC, abstractmethod

class Scene(ABC):
    def __init__(self, manager):
        self.manager = manager
        self.screen = manager.screen
        self.SCREEN_W = manager.SCREEN_W
        self.SCREEN_H = manager.SCREEN_H

        self.pet_timer = 0
        self.current_state = self.manager.game_state

        font_size = int(self.SCREEN_H * 0.045)
        self.font = pygame.font.SysFont('arial', font_size)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            config.money += 100
        
        # Клик для поглаживания в центре экрана
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and config.is_onScreen == True:
            m_x, m_y = pygame.mouse.get_pos()
            akane_center_x = self.SCREEN_W // 2
                
            # Зона клика по голове
            if (akane_center_x - 140) < m_x < (akane_center_x + 110) and int(self.SCREEN_H * 0.15) < m_y < int(self.SCREEN_H * 0.38):
                config.trust_level += 5
                self.pet_timer = 40

    def update(self):
        if self.pet_timer > 0:
            self.pet_timer -= 1

    @abstractmethod
    def draw(self):
        pass

    def draw_balance(self):
        money_text = f"Баланс: {config.money}$"
        money_surf = self.font.render(money_text, True, (255, 215, 0))
        money_x = self.SCREEN_W - money_surf.get_width() - 30
        money_y = 30
        
        money_bg = pygame.Surface((money_surf.get_width() + 20, money_surf.get_height() + 10), pygame.SRCALPHA)
        money_bg.fill((0, 0, 0, 150))
        
        self.screen.blit(money_bg, (money_x - 10, money_y - 5))
        self.screen.blit(money_surf, (money_x, money_y))

    def pat_pat(self):
        if self.pet_timer > 0 and config.is_onScreen == True:
            trust_popup = self.font.render("+<3 Доверие Акане", True, (255, 105, 180))
            popup_x = (self.SCREEN_W // 2) - (trust_popup.get_width() // 2)
            popup_y = int(self.SCREEN_H * 0.12)
            
            popup_bg = pygame.Surface((trust_popup.get_width() + 20, trust_popup.get_height() + 10), pygame.SRCALPHA)
            popup_bg.fill((0, 0, 0, 100))
            
            self.screen.blit(popup_bg, (popup_x - 10, popup_y - 5))
            self.screen.blit(trust_popup, (popup_x, popup_y))
