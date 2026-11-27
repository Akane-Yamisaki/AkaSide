import pygame
import config
from scenes.BaseScene import Scene
from scenes.pixelate_Location import pixelate_image
from engine.notify import NotificationManager

class BedRoom(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        config.is_onScreen = False

        self.notifier = NotificationManager(app_id="AkaSide", font_size=32)

        self.Transition = False
        self.transition_start = 0
        self.day_swapped = False

        try:
            raw_bg = pygame.image.load('assets/Images/Locations/Bedroom_pixelate.png').convert()
            self.bg = pixelate_image(raw_bg, self.SCREEN_W, self.SCREEN_H, 6)
        except Exception as e:
            print(f"Ошибка загрузки пиксельного фона: {e}")
            self.bg = pygame.Surface((self.SCREEN_W, self.SCREEN_H))
            self.bg.fill((40, 20, 20))

        shkaf = pygame.Rect(int(self.SCREEN_W * 0.258), int(self.SCREEN_H * 0.18), int(self.SCREEN_W * 0.165), int(self.SCREEN_H * 0.15))
        stol = pygame.Rect(int(self.SCREEN_W * 0.17), int(self.SCREEN_H * 0.70), int(self.SCREEN_W * 0.23), int(self.SCREEN_H * 0.18))
        krovat = pygame.Rect(int(self.SCREEN_W * 0.52), int(self.SCREEN_H * 0.35), int(self.SCREEN_W * 0.27), int(self.SCREEN_H * 0.35))
        
        верхняя_стена = pygame.Rect(0, 0, self.SCREEN_W, int(self.SCREEN_H * 0.28))
        нижняя_стена = pygame.Rect(0, int(self.SCREEN_H * 0.88), self.SCREEN_W, int(self.SCREEN_H * 0.12))
        левая_стена = pygame.Rect(0, 0, int(self.SCREEN_W * 0.14), int(self.SCREEN_H))
        правая_стена = pygame.Rect(int(self.SCREEN_W * 0.79), 0, int(self.SCREEN_W * 0.21), int(self.SCREEN_H * 0.88))

        self.obstacles = [верхняя_стена, нижняя_стена, левая_стена, правая_стена, shkaf, stol, krovat]

        p_x, p_y = int(self.SCREEN_W * 0.48), int(self.SCREEN_H * 0.55)
        p_w = int(self.SCREEN_W * 0.035)
        p_h = int(self.SCREEN_H * 0.06)
        self.player_rect = pygame.Rect(p_x, p_y, p_w, p_h)
        self.player_speed = int(self.SCREEN_H * 0.005) + 1

        if config.player_x > 0 or config.player_y > 0:
            self.player_rect.center = (config.player_x, config.player_y)

        # --- ХИТБОКС ДВЕРИ (Слева по центру стены + 1% внутрь комнаты) ---
        # Считаем координату X левой стены (SCREEN_W * 0.14) + добавляем 1% ширины (SCREEN_W * 0.01)
        door_x = int(self.SCREEN_W * 0.14) + int(self.SCREEN_W * 0.01)
        # Центр левой стены по высоте (примерно 45% от верха экрана)
        door_y = int(self.SCREEN_H * 0.45)
        self.door_rect = pygame.Rect(door_x, door_y, int(self.SCREEN_W * 0.02), int(self.SCREEN_H * 0.12))

        self.active_interaction = None

    def on_enter(self):
        self.manager.play_music('sound/Akane-House.mp3')

    def reload_coordinates(self):
        self.player_rect.center = config.player_x, config.player_y

    def interact_with_object(self):
        if self.active_interaction == "Дверь":
            print("Логика: Игрок выходит из комнаты!")
            # Здесь в будущем будет переключение на коридор или улицу:
            # self.manager.scene = "Corridor_pixel"
            
        elif self.active_interaction == "Кровать":
            if not config.can_sleep: return
            self.Transition = True
            self.transition_start = pygame.time.get_ticks()

    def handle_events(self, event):
        super().handle_events(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.interact_with_object()

            elif event.key == pygame.K_ESCAPE:
                self.get_player_coord()
                self.manager.scene = "Saves"

    def get_player_coord(self):
        config.player_x, config.player_y = self.player_rect.center

    def update(self):
        super().update()
        
        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0
        
        if keys[pygame.K_a]: move_x = -self.player_speed
        if keys[pygame.K_d]: move_x = self.player_speed
        if keys[pygame.K_w]: move_y = -self.player_speed
        if keys[pygame.K_s]: move_y = self.player_speed

        # 4. Твой рабочий блок коллизий (математика движения)
        if move_x != 0:
            self.player_rect.x += int(move_x)
            for obs in self.obstacles:
                if self.player_rect.colliderect(obs): self.player_rect.x -= int(move_x); break
        
        if move_y != 0:
            self.player_rect.y += int(move_y)
            for obs in self.obstacles:
                if self.player_rect.colliderect(obs): self.player_rect.y -= int(move_y); break

        self.active_interaction = None
        check_zone = self.player_rect.inflate(80, 80)
        if check_zone.colliderect(self.door_rect):
            self.active_interaction = "Дверь"
        elif check_zone.colliderect(self.obstacles[-1]):
            self.active_interaction = "Кровать"
        elif check_zone.colliderect(self.obstacles[-3]):
            if "Book" in config.inventory['Items']:
                return

            config.inventory['Items'].append("Book")
            self.notifier.send("Вы взяли книжку", duration_frames=180, win_toast=True)
            print(config.inventory)

            self.active_interaction = "Шкаф"

    def get_pos(self):
        config.player_x, config.player_y = int(self.player_rect.center)

    def draw(self):

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

        # 1. ВСЕГДА сначала рисуем саму сцену (фон, игрока и интерфейс)
        self.screen.blit(self.bg, (0, 0))
        pygame.draw.rect(self.screen, (0, 255, 255), self.player_rect)

        if self.active_interaction and not self.Transition:
            hint_text = f"[E] Взаимодействовать: {self.active_interaction}"
            hint_surf = self.font.render(hint_text, True, (255, 255, 255))
            self.screen.blit(hint_surf, (self.SCREEN_W // 2 - hint_surf.get_width() // 2, int(self.SCREEN_H * 0.75)))

        self.notifier.draw(self.screen, pos=(self.player_rect.centerx - 60, self.player_rect.top - 30))
        self.draw_balance()

        # 2. ПОВЕРХ уже нарисованной сцены накладываем плавное затемнение и свап дня
        if self.Transition:
            elapsed = pygame.time.get_ticks() - self.transition_start
            
            if elapsed < 1000:
                alpha = int((elapsed / 1000) * 255)
            elif elapsed < 3000:
                alpha = 255
            elif elapsed < 4000:
                alpha = max(0, 255 - int(((elapsed - 3000) / 1000) * 255))
            else:
                self.Transition = False
                self.day_swapped = False
                return

            bg = pygame.Surface((self.SCREEN_W, self.SCREEN_H)).convert()
            bg.fill((0, 0, 0))
            bg.set_alpha(alpha)
            self.screen.blit(bg, (0, 0))

            if 1000 <= elapsed <= 3000:
                label_surf = self.font.render("День: ", True, (255, 255, 255))
                
                if elapsed < 1500:
                    text_alpha = 255
                elif elapsed < 2000:
                    text_alpha = int(((2000 - elapsed) / 500) * 255)
                elif elapsed < 2500:
                    text_alpha = int(((elapsed - 2000) / 500) * 255)
                else:
                    text_alpha = 255

                if elapsed < 2000:
                    day_surf = self.font.render(str(config.current_day), True, (255, 215, 0))
                else:
                    if not self.day_swapped:
                        config.current_day += 1
                        self.day_swapped = True
                    color = (255, 215, 0) if config.current_day < 7 else (171, 2, 21)
                    day_surf = self.font.render(str(config.current_day), True, color)

                day_surf.set_alpha(text_alpha)

                x = self.SCREEN_W // 2 - (label_surf.get_width() + day_surf.get_width()) // 2
                y = self.SCREEN_H // 2
                self.screen.blit(label_surf, (x, y))
                self.screen.blit(day_surf, (x + label_surf.get_width(), y))
