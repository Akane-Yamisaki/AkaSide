# engine/input.py
import pygame

def get_movement_vector(game_state):
    """
    Возвращает направление движения (x, y).
    Если идет диалог или ввод имени, возвращает (0, 0) - игрок стоит на месте.
    """
    # Если состояние НЕ свободное исследование — полностью блокируем ходьбу
    if game_state != "free_roam":
        return 0, 0

    # Если ходить можно, опрашиваем клавиши WASD или стрелочки
    keys = pygame.key.get_pressed()
    dx = 0
    dy = 0

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        dx = -1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        dx = 1
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        dy = -1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dy = 1

    return dx, dy