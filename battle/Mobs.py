import random
import pygame

class GlitchMob:
    def __init__(self, bounds):
        self.name = "Сбой_Файла.exe"
        self.hp = 30
        self.max_hp = 30
        self.current_phrase = "Ошибк4... Данны3 поврежден1..."
        self.left, self.right, self.top, self.bottom = bounds
        
        # Загружаем спрайт моба
        self.image = pygame.image.load("assets/mob_glitch.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 120))

    def draw(self, screen):
        screen.blit(self.image, (screen.get_width() // 2 - 60, 200))

    def update_attack(self, projectiles, timer):
        if timer % 40 == 0:
            projectiles.append({"x": random.randint(self.left + 10, self.right - 25), "y": self.top - 15, "vx": 0, "vy": 4})