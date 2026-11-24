import pygame
from scenes.BaseScene import Scene

class Gallery(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.choose = 1

        try:
            self.bg = pygame.image.load("assets/Images/Gallery_BG.png").convert()
        except:
            self.bg = pygame.Surface((self.SCREEN_W, self.SCREEN_H))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.scene = "menu"

    def update(self):
        super().update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
