import pygame

def pixelate_image(image, target_w, target_h, pixel_size=6):
    small_w = max(1, target_w // pixel_size)
    small_h = max(1, target_h // pixel_size)
    # Сжимаем картинку, теряя мелкие детали
    small_img = pygame.transform.scale(image, (small_w, small_h))
    # Растягиваем обратно без сглаживания — получаем четкие ретро-кубики
    return pygame.transform.scale(small_img, (target_w, target_h))