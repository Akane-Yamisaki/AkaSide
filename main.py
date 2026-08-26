import os
import sys
import pygame
import config

from engine.scene_manager import SceneManager

# --- БЛОК СОВМЕСТИМОСТИ С PYINSTALLER (ОДИН ФАЙЛ) ---
def resource_path(relative_path):
    """Возвращает путь к ресурсу для обычного запуска и PyInstaller."""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def is_android():
    """Определяет запуск через Android activity."""
    return hasattr(sys, "getandroidactivity")

os.environ["SDL_VIDEO_CENTERED"] = "1"

# Определяем платформу до загрузки платформозависимых ресурсов.
if is_android():
    config.is_mobile = True

# Устанавливаем рабочую директорию для PyInstaller.
if hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

if config.is_mobile:
    pygame.display.set_caption(config.mobile_path + "AkaSide")
    pygame.display.set_icon(
        pygame.image.load(resource_path(config.mobile_path + "assets/icon.png"))
    )
else:
    pygame.display.set_caption("AkaSide")
    pygame.display.set_icon(
        pygame.image.load(resource_path("assets/icon.png"))
    )

monitor_info = pygame.display.Info()
SCREEN_W = monitor_info.current_w
SCREEN_H = monitor_info.current_h - 60
# SCREEN_W = 1080
# SCREEN_H = 2400 - 60

flags = pygame.FULLSCREEN | pygame.SCALED if config.is_mobile else pygame.RESIZABLE
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
