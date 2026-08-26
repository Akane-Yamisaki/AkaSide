import pygame
import config
from scenes.BaseScene import Scene
from scenes.pixelate_Location import pixelate_image
from engine.joystick import VirtualJoystick

class BedRoom(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        config.is_onScreen = False

        self.joystick = VirtualJoystick(self.SCREEN_W, self.SCREEN_H)

        # --- 1. ВОЗВРАЩАЕМ ЗАГРУЗКУ И ПИКСЕЛИЗАЦИЮ ТВОЕГО БГ ---
        try:
            
            if config.is_mobile: raw_bg = pygame.image.load(config.mobile_path + 'assets/Images/Locations/Bedroom_pixelate.png').convert() 
            else: raw_bg = pygame.image.load('assets/Images/Locations/Bedroom_pixelate.png').convert()
            self.bg = pixelate_image(raw_bg, self.SCREEN_W, self.SCREEN_H, 6)
        except Exception as e:
            print(f"Ошибка загрузки пиксельного фона: {e}")
            self.bg = pygame.Surface((self.SCREEN_W, self.SCREEN_H))
            self.bg.fill((40, 20, 20))

        # --- ТВОЯ СВЕРХТОЧНАЯ МЕБЕЛЬ И СТЕНЫ ---
        shkaf = pygame.Rect(int(self.SCREEN_W * 0.258), int(self.SCREEN_H * 0.18), int(self.SCREEN_W * 0.165), int(self.SCREEN_H * 0.15))
        stol = pygame.Rect(int(self.SCREEN_W * 0.17), int(self.SCREEN_H * 0.70), int(self.SCREEN_W * 0.23), int(self.SCREEN_H * 0.18))
        krovat = pygame.Rect(int(self.SCREEN_W * 0.52), int(self.SCREEN_H * 0.35), int(self.SCREEN_W * 0.27), int(self.SCREEN_H * 0.35))
        
        верхняя_стена = pygame.Rect(0, 0, self.SCREEN_W, int(self.SCREEN_H * 0.28))
        нижняя_стена = pygame.Rect(0, int(self.SCREEN_H * 0.88), self.SCREEN_W, int(self.SCREEN_H * 0.12))
        левая_стена = pygame.Rect(0, 0, int(self.SCREEN_W * 0.14), int(self.SCREEN_H))
        правая_стена = pygame.Rect(int(self.SCREEN_W * 0.79), 0, int(self.SCREEN_W * 0.21), int(self.SCREEN_H * 0.88))

        self.obstacles = [верхняя_стена, нижняя_стена, левая_стена, правая_стена, shkaf, stol, krovat]

        # --- СПАВН АКАНЭ И ИГРОКА ---
        p_w = int(self.SCREEN_W * 0.035)
        p_h = int(self.SCREEN_H * 0.06)
        self.player_rect = pygame.Rect(int(self.SCREEN_W * 0.48), int(self.SCREEN_H * 0.55), p_w, p_h)
        self.player_speed = int(self.SCREEN_H * 0.005) + 1
        self.akane_rect = pygame.Rect(int(self.SCREEN_W * 0.25), int(self.SCREEN_H * 0.73), p_w, p_h)

        # --- ХИТБОКС ДВЕРИ (Слева по центру стены + 1% внутрь комнаты) ---
        # Считаем координату X левой стены (SCREEN_W * 0.14) + добавляем 1% ширины (SCREEN_W * 0.01)
        door_x = int(self.SCREEN_W * 0.14) + int(self.SCREEN_W * 0.01)
        # Центр левой стены по высоте (примерно 45% от верха экрана)
        door_y = int(self.SCREEN_H * 0.45)
        self.door_rect = pygame.Rect(door_x, door_y, int(self.SCREEN_W * 0.02), int(self.SCREEN_H * 0.12))

        self.active_interaction = None

    def interact_with_object(self):
        """Логика выполнения действий при нажатии кнопки взаимодействия"""
        if self.active_interaction == "Акане":
            print("Логика: Запускаем диалог с Акане!")
            # Переключаем статус движка обратно на Визуальную Новеллу
            self.manager.game_state = "dialogue"
            # Возвращаем игрока в сцену разговора
            self.manager.scene = "Bedroom_Day1"
            
        elif self.active_interaction == "Дверь":
            print("Логика: Игрок выходит из комнаты!")
            # Здесь в будущем будет переключение на коридор или улицу:
            # self.manager.scene = "Corridor_pixel"
            
        elif self.active_interaction == "Кровать":
            print("Логика: Вы осмотрели кровать.")

    def handle_events(self, event):
        super().handle_events(event)
        
        # Нажатие на E для ПК (взаимодействие) оставляем здесь
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.interact_with_object()

    def update(self):
        super().update()
        
        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0
        
        # 2. Управление клавиатурой
        if keys[pygame.K_a]: move_x = -self.player_speed
        if keys[pygame.K_d]: move_x = self.player_speed
        if keys[pygame.K_w]: move_y = -self.player_speed
        if keys[pygame.K_s]: move_y = self.player_speed

        # 3. Обновляем джойстик
        self.joystick.update()
        if config.is_mobile:
            move_x += config.joystick_vector[0] * self.player_speed
            move_y += config.joystick_vector[1] * self.player_speed

        # 4. Твой рабочий блок коллизий (математика движения)
        if move_x != 0:
            self.player_rect.x += int(move_x)
            for obs in self.obstacles:
                if self.player_rect.colliderect(obs): self.player_rect.x -= int(move_x); break
        
        if move_y != 0:
            self.player_rect.y += int(move_y)
            for obs in self.obstacles:
                if self.player_rect.colliderect(obs): self.player_rect.y -= int(move_y); break

        # 5. ПРОВЕРКА ДИСТАНЦИИ ВЗАИМОДЕЙСТВИЯ (Перенеси этот блок сюда, если он стерся)
        self.active_interaction = None
        check_zone = self.player_rect.inflate(80, 80)
        if check_zone.colliderect(self.akane_rect):
            self.active_interaction = "Акане"
        elif check_zone.colliderect(self.door_rect):
            self.active_interaction = "Дверь"
        elif check_zone.colliderect(self.obstacles[-1]):
            self.active_interaction = "Кровать"

    # --- ВОТ ОН, ТОТ САМЫЙ ОБЯЗАТЕЛЬНЫЙ МЕТОД DRAW! ТЕПЕРЬ ОН ЕСТЬ! ---
    def draw(self):
        # 1. Рисуем фон
        self.screen.blit(self.bg, (0, 0))

        # 2. Отладочная подсветка мебели и стен (твоя полупрозрачная магия)
        # for obs in self.obstacles:
        #     debug_surf = pygame.Surface((obs.width, obs.height), pygame.SRCALPHA)
        #     debug_surf.fill((255, 0, 0, 80))
        #     pygame.draw.rect(debug_surf, (255, 0, 0, 255), (0, 0, obs.width, obs.height), 3)
        #     self.screen.blit(debug_surf, (obs.x, obs.y))

        # 3. ОТЛАДКА ДВЕРИ (Синий маркер)
        # door_surf = pygame.Surface((self.door_rect.width, self.door_rect.height), pygame.SRCALPHA)
        # door_surf.fill((0, 0, 255, 100))
        # pygame.draw.rect(door_surf, (0, 0, 255, 255), (0, 0, self.door_rect.width, self.door_rect.height), 3)
        # self.screen.blit(door_surf, (self.door_rect.x, self.door_rect.y))

        # 4. Отрисовка Аканэ и Игрока
        pygame.draw.rect(self.screen, (255, 105, 180), self.akane_rect) 
        pygame.draw.rect(self.screen, (0, 255, 255), self.player_rect)

        # 5. Рисуем джойстик поверх персонажей
        self.joystick.draw(self.screen)

        # 6. Кнопка и надпись взаимодействия
        if self.active_interaction:
            hint_text = f"[E] Взаимодействовать: {self.active_interaction}"
            hint_surf = self.font.render(hint_text, True, (255, 255, 255))
            self.screen.blit(hint_surf, (self.SCREEN_W // 2 - hint_surf.get_width() // 2, int(self.SCREEN_H * 0.75)))
            
            if config.is_mobile:
                btn_w, btn_h = int(self.SCREEN_W * 0.2), int(self.SCREEN_H * 0.08)
                btn_x, btn_y = int(self.SCREEN_W * 0.4), int(self.SCREEN_H * 0.8)
                btn_bg = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
                btn_bg.fill((0, 0, 0, 200))
                pygame.draw.rect(btn_bg, (0, 255, 255), (0, 0, btn_w, btn_h), 2)
                btn_text = self.font.render("Действие", True, (0, 255, 255))
                btn_bg.blit(btn_text, (btn_w // 2 - btn_text.get_width() // 2, btn_h // 2 - btn_text.get_height() // 2))
                self.screen.blit(btn_bg, (btn_x, btn_y))

        # 7. Самый главный финальный слой — баланс
        self.draw_balance()