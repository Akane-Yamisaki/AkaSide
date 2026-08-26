import pygame, config

def load_and_scale_character(file_path, target_screen_h):
    """
    Безопасная функция: возвращает Аканэ исходную кожу и свитер.
    """
    # Загружаем чистый PNG после rembg
    if config.is_mobile: raw_img = pygame.image.load(config.mobile_path + file_path).convert_alpha()
    else: raw_img = pygame.image.load(file_path).convert_alpha()
    
    img_rect = raw_img.get_rect()
    desired_height = int(target_screen_h * 0.85) 
    ratio = desired_height / img_rect.height
    new_width = int(img_rect.width * ratio)

    # Качественное сглаживание
    scaled_img = pygame.transform.smoothscale(raw_img, (new_width, desired_height))
    return scaled_img