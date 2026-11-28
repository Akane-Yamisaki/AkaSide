import math
import pygame
from scenes.BaseScene import Scene
from engine.load_character_module import load_and_scale_character as lasc

class Gallery(Scene):
    def __init__(self, manager):
        super().__init__(manager)

        self.choose = 0
        self.page = 0
        self.selected_art = None

        try:
            self.bg = pygame.image.load("assets/Images/Gallery_BG.png").convert()
            self.bg = pygame.transform.smoothscale(self.bg, (self.SCREEN_W, self.SCREEN_H))
        except Exception:
            self.bg = pygame.Surface((self.SCREEN_W, self.SCREEN_H))
            self.bg.fill((20, 20, 25))

        path = "assets/Images/gallery/"

        art_files = [
            # jpg files
        ]

        self.arts = []
        for filename in art_files:
            full_img = pygame.image.load(path + filename).convert()
            self.arts.append(full_img)

        self.total_pages = max(1, math.ceil(len(self.arts) / 4))

        self.slots = self.create_grid()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if self.selected_art is not None:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                    self.selected_art = None
                return

            if event.key == pygame.K_ESCAPE:
                self.manager.scene = "menu"
                return

            if event.key in (pygame.K_LEFT, pygame.K_a):
                if self.choose % 2 == 1:
                    self.choose -= 1
                elif self.page > 0:
                    self.page -= 1
                    self.choose += 1

            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                if self.choose % 2 == 0:
                    self.choose += 1
                elif self.page < self.total_pages - 1:
                    self.page += 1
                    self.choose -= 1

            elif event.key in (pygame.K_UP, pygame.K_w):
                if self.choose >= 2:
                    self.choose -= 2

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                if self.choose <= 1:
                    self.choose += 2

            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                art_index = self.page * 4 + self.choose
                if art_index < len(self.arts):
                    self.selected_art = self.arts[art_index]

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.selected_art is not None:
                self.selected_art = None
            else:
                for i, rect in enumerate(self.slots):
                    art_index = self.page * 4 + i
                    if rect.collidepoint(event.pos) and art_index < len(self.arts):
                        self.choose = i
                        self.selected_art = self.arts[art_index]
                        break

    def update(self):
        super().update()

    def create_grid(self):
        box_size = int(self.SCREEN_H * 0.3)
        gap = int(self.SCREEN_H * 0.04)

        total_width = box_size * 2 + gap
        total_height = box_size * 2 + gap

        start_x = (self.SCREEN_W - total_width) // 2
        start_y = (self.SCREEN_H - total_height) // 2

        rects = []
        for i in range(4):
            col = i % 2
            row = i // 2
            x = start_x + col * (box_size + gap)
            y = start_y + row * (box_size + gap)
            rects.append(pygame.Rect(x, y, box_size, box_size))

        return rects

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        if self.selected_art is not None:
            overlay = pygame.Surface((self.SCREEN_W, self.SCREEN_H))
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            img_w, img_h = self.selected_art.get_size()
            scale = min(self.SCREEN_W / img_w, self.SCREEN_H / img_h)
            new_w, new_h = int(img_w * scale), int(img_h * scale)

            full_view = pygame.transform.smoothscale(self.selected_art, (new_w, new_h))
            pos_x = (self.SCREEN_W - new_w) // 2
            pos_y = (self.SCREEN_H - new_h) // 2
            self.screen.blit(full_view, (pos_x, pos_y))
            return

        current_arts = self.arts[self.page * 4 : (self.page + 1) * 4]

        for i, rect in enumerate(self.slots):
            is_selected = (i == self.choose)
            border_color = (217, 117, 199) if is_selected else (230, 151, 216)
            border_width = 5 if is_selected else 2

            if i < len(current_arts):
                preview = pygame.transform.smoothscale(current_arts[i], (rect.width, rect.height))
                self.screen.blit(preview, rect.topleft)
            else:
                pygame.draw.rect(self.screen, (30, 30, 35), rect, border_radius=8)

            pygame.draw.rect(self.screen, border_color, rect, width=border_width, border_radius=8)
