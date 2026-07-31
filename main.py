import os
import sys
import pygame
import config

from engine.scene_manager import SceneManager

os.environ['SDL_VIDEO_CENTERED'] = '1'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

pygame.init()
if config.is_mobile:
    pygame.display.set_caption(config.mobile_path + 'AkaSide')
    pygame.display.set_icon(pygame.image.load(config.mobile_path + 'assets/icon.png'))
else:
    pygame.display.set_caption('AkaSide')
    pygame.display.set_icon(pygame.image.load('assets/icon.png'))

monitor_info = pygame.display.Info()
SCREEN_W = monitor_info.current_w
SCREEN_H = monitor_info.current_h - 60
# SCREEN_W = 1080
# SCREEN_H = 2400  - 60

if hasattr(sys, 'getandroidactivity'): # Флаг того, что мы запустились на Android
    config.is_mobile = True
    flags = pygame.FULLSCREEN | pygame.SCALED
else:
    flags = pygame.RESIZABLE

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), flags)

scene_manager = SceneManager(screen, SCREEN_W, SCREEN_H)

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60) 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
        
        # Передаем клики и нажатия клавиш в текущую сцену через Менеджер
        scene_manager.handle_events(event)

    scene_manager.update()

    screen.fill((0, 0, 0)) # Очищаем старый кадр
    scene_manager.draw()   # Просим менеджер нарисовать активную сцену
    
    pygame.display.flip()

pygame.quit()
sys.exit()