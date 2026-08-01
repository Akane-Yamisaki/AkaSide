import config, pygame, sys
from engine.joystick import VirtualJoystick
from engine.load_character_module import load_and_scale_character as lasc
from scenes.BaseScene import Scene

class Menu(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        config.is_onScreen = False

        self.joystick = VirtualJoystick(self.SCREEN_W, self.SCREEN_H)
        self.choose = 1

        # Инициализация шрифта (None — стандартный системный, 50 — размер)
        pygame.font.init()
        self.font = pygame.font.Font(None, int(self.SCREEN_H // 15))

        self.menu_items = ["Новая игра", "Загрузить", "Галерея", "Настройки", "Выход"]
        
        self.menu_x = int(self.SCREEN_W // 10)
        self.menu_start_y = int(self.SCREEN_H // 2)
        self.menu_spacing = int(self.SCREEN_H // 12) # Расстояние между строками

        try:
            if config.is_mobile:
                bg = pygame.image.load(config.mobile_path + 'assets/Images/Menu_BG.png').convert()
            else:
                bg = pygame.image.load('assets/Images/Menu_BG.png').convert()
            self.Akane = lasc('assets/Images/Akane/Normal.png', self.SCREEN_H * 0.95)
            self.bg = pygame.transform.smoothscale(bg, (self.SCREEN_W, self.SCREEN_H))

            self.akane_x = int(self.SCREEN_W // 2 + self.SCREEN_W // 10)
            self.akane_y = int(self.SCREEN_H // 4 - self.SCREEN_H // 14)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            pass

        self.btn = pygame.Rect(self.SCREEN_W * 0.9, self.SCREEN_H * 0.6, self.SCREEN_W * 0.05, self.SCREEN_H * 0.1)
        self.btn_font = pygame.font.Font(None, int(self.SCREEN_H // 30))
        self.btn_text = self.btn_font.render("Choose", True, "Black")
        self.BtnRect = self.btn_text.get_rect()
        self.BtnRect.center = self.btn.center

    def actions(self):
        match self.choose:
            case 1:
                self.manager.game_state = "dialogue"
                self.manager.scene = "Bedroom_Day1"
            case 2:
                # game saves logic
                pass
            case 3:
                #gallery mechanic
                pass
            case 4:
                # settings logic
                pass
            case 5:
                pygame.quit()
                sys.exit()

    def handle_events(self, event):
        self.joystick.handle_events(event)
        action_triggered = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                action_triggered = True

            keys = pygame.key.get_pressed()
                
            if keys[pygame.K_s]:
                if self.choose < len(self.menu_items): self.choose += 1 
                else: self.choose = 1
            if keys[pygame.K_w]:
                if self.choose < 2: self.choose = len(self.menu_items)
                else: self.choose -= 1

        elif event.type == pygame.MOUSEBUTTONDOWN and config.is_mobile:
            mouse_pos = event.pos
            action_triggered = self.btn.collidepoint(mouse_pos)

        if action_triggered:
            self.actions()

    def update(self):
        super().update()

        self.joystick.update()
        if not hasattr(self, 'joy_ready'):
            self.joy_ready = True
    
        joy_y = config.joystick_vector[1]
    
        if joy_y > 0.5 and self.joy_ready:
            if self.choose < len(self.menu_items): self.choose += 1
            else: self.choose = 1
            self.joy_ready = False
    
        elif joy_y < -0.5 and self.joy_ready:
            if self.choose < 2: self.choose = len(self.menu_items)
            else: self.choose -= 1
            self.joy_ready = False
    
        elif abs(joy_y) < 0.2:
            self.joy_ready = True

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.Akane, (self.akane_x, self.akane_y))

        for index, item_text in enumerate(self.menu_items):
            item_number = index + 1 

            if item_number == self.choose:
                # Цвет для ВЫБРАННОГО пункта
                color = (200, 0, 0)
                # Эффект анимации: сдвигаем выбранный текст чуть вправо, создавая динамику
                display_text = f"> {item_text}"
                current_x = self.menu_x + 15
            else:
                # Цвет для НЕАКТИВНЫХ пунктов (бледно-серый/белый)
                color = (180, 180, 180)
                display_text = item_text
                current_x = self.menu_x

            text_surface = self.font.render(display_text, True, color)
            
            current_y = self.menu_start_y + (index * self.menu_spacing)

            self.screen.blit(text_surface, (current_x, current_y))

        if config.is_mobile:
            self.joystick.draw(self.screen)
            # pygame.draw.rect(self.bg, (128, 128, 128), self.btn)
            pygame.draw.circle(self.screen, (128,128,128), self.btn.center, self.SCREEN_H * 0.05)
            self.screen.blit(self.btn_text, self.BtnRect)
