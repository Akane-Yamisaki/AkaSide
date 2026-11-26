import config
import pygame
import sys
from engine.load_character_module import load_and_scale_character as lasc
from scenes.BaseScene import Scene

class Menu(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        config.is_onScreen = False

        self.choose = 1

        pygame.font.init()
        self.font = pygame.font.Font(None, int(self.SCREEN_H // 15))

        self.menu_items = [
            "Новая игра",
            "Загрузить",
            "Галерея",
            "Настройки",
            "Выход",
        ]

        self.menu_x = int(self.SCREEN_W // 10)
        self.menu_start_y = int(self.SCREEN_H // 2)
        self.menu_spacing = int(self.SCREEN_H // 12)

        try:
            bg = pygame.image.load("assets/Images/Menu_BG.png").convert()
            self.Akane = lasc("assets/Images/Akane/Normal.png", self.SCREEN_H * 0.95)

            self.bg = pygame.transform.smoothscale(bg, (self.SCREEN_W, self.SCREEN_H))
            self.akane_x = int(self.SCREEN_W // 2 + self.SCREEN_W // 10)
            self.akane_y = int(self.SCREEN_H // 4 - self.SCREEN_H // 14)
        except (FileNotFoundError, pygame.error) as e:
            print(f"Error loading menu resources: {e}")
            self.bg = pygame.Surface((self.SCREEN_W, self.SCREEN_H))
            self.Akane = pygame.Surface((0, 0))
            self.akane_x = 0
            self.akane_y = 0

    def actions(self):
        match self.choose:
            case 1:
                if config.new_game == True: return
                self.manager.scene = "Bedroom_Day1"
            case 2:
                self.manager.scene = "Saves"
            case 3:
                self.manager.scene = "Gallery"
            case 4:
                # settings logic
                pass
            case 5:
                pygame.quit()
                sys.exit()

    def on_enter(self):
        self.manager.play_music('sound/Akane-menu.mp3')

    def handle_events(self, event):
        action_triggered = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                action_triggered = True

            if event.key in (pygame.K_DOWN, pygame.K_s):
                self._move_selection(1)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self._move_selection(-1)

            if action_triggered:
                self.actions()

    def _move_selection(self, direction):
        self.choose = (self.choose - 1 + direction) % len(self.menu_items) + 1

    def update(self):
        super().update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.Akane, (self.akane_x, self.akane_y))

        for index, item_text in enumerate(self.menu_items):
            item_number = index + 1

            if item_number == self.choose:
                color = (200, 0, 0)
                display_text = f"> {item_text}"
                current_x = self.menu_x + 15
            else:
                color = (180, 180, 180)
                display_text = item_text
                current_x = self.menu_x

            text_surface = self.font.render(display_text, True, color)
            current_y = self.menu_start_y + index * self.menu_spacing
            self.screen.blit(text_surface, (current_x, current_y))
