import os
import sys
import pygame
import config

from engine.scene_manager import SceneManager


def resource_path(relative_path):
    """Возвращает путь к ресурсу для обычного запуска и PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


os.environ["SDL_VIDEO_CENTERED"] = "1"

# Устанавливаем рабочую директорию для PyInstaller.
if hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Определяем платформу до загрузки платформозависимых ресурсов.
config.is_mobile = hasattr(sys, "getandroidactivity")

pygame.init()

if config.is_mobile:
    pygame.display.set_caption("AkaSide")
    pygame.display.set_icon(
        pygame.image.load(resource_path(config.mobile_path + "assets/icon.png"))
    )
else:
    pygame.display.set_caption("AkaSide")
    pygame.display.set_icon(pygame.image.load(resource_path("assets/icon.png")))

monitor_info = pygame.display.Info()
SCREEN_W = monitor_info.current_w
SCREEN_H = monitor_info.current_h - 60

if config.is_mobile:
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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            pygame.display.toggle_fullscreen()

        scene_manager.handle_events(event)

    scene_manager.update()

    screen.fill((0, 0, 0))
    scene_manager.draw()
    pygame.display.flip()

pygame.quit()
sys.exit()
