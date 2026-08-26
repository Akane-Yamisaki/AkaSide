import random
import pygame

class AkaneBoss:
    def __init__(self, bounds):
        self.name = "Evil Akane"
        self.hp = 100
        self.max_hp = 100
        self.current_phrase = "Продолжай атаковать"
        self.left, self.right, self.top, self.bottom = bounds
        
        # Загружаем и масштабируем спрайт Злой Акане
        self.image = pygame.image.load("assets/akane_evil.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))

    def draw(self, screen):
        # 1280 // 2 = 640. Спрайт 200x200 встанет ровно по центру
        screen.blit(self.image, (640 - 75, 230))


    def update_attack(self, projectiles, timer):
        # (Твой старый код атак остается без изменений)
        if timer % 20 == 0:
            projectiles.append({"x": random.randint(self.left + 10, self.right - 25), "y": self.top - 15, "vx": 0, "vy": 6})
        if timer % 45 == 0:
            projectiles.append({"x": self.left - 15, "y": random.randint(self.top + 10, self.bottom - 25), "vx": 5, "vy": 0})