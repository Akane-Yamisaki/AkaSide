import config, pygame
from engine.joystick import VirtualJoystick
from engine.load_character_module import load_and_scale_character as lasc
from scenes.BaseScene import Scene


class Saves(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.joystick = VirtualJoystick(self.SCREEN_W, self.SCREEN_H)
        self.choose = 1
        self.max_saves = 3
        self.joy_ready = True

        self.font = pygame.font.Font(None, self.SCREEN_H // 15)
        self.spacing = self.SCREEN_H // 12
        self.saves_x = self.SCREEN_W // 10
        self.saves_y = self.SCREEN_H // 10

        self.bg = self.load_background()

    def load_background(self):
        try:
            if config.is_mobile:
                bg = pygame.image.load(
                    config.mobile_path + "assets/Image/Saves_BG.png"
                ).convert()
            else:
                bg = pygame.image.load("assets/Image/Saves_BG.png").convert()

            return pygame.transform.smoothscale(
                bg,
                (self.SCREEN_W, self.SCREEN_H),
            )
        except (FileNotFoundError, pygame.error) as e:
            print(f"Error loading Saves background: {e}")
            return pygame.Surface((self.SCREEN_W, self.SCREEN_H))

    def handle_events(self, event):
        self.joystick.handle_events(event)

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.choose = self.choose + 1 if self.choose < self.max_saves else 1

            elif event.key in (pygame.K_UP, pygame.K_w):
                self.choose = self.choose - 1 if self.choose > 1 else self.max_saves

    def update(self):
        super().update()
        self.joystick.update()

        if config.joystick_vector[1] > 0.5 and self.joy_ready:
            self.choose = self.choose + 1 if self.choose < self.max_saves else 1
            self.joy_ready = False

        elif config.joystick_vector[1] < -0.5 and self.joy_ready:
            self.choose = self.choose - 1 if self.choose > 1 else self.max_saves
            self.joy_ready = False

        elif abs(config.joystick_vector[1]) < 0.2:
            self.joy_ready = True

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        for slot in range(1, self.max_saves + 1):
            color = (200, 0, 0) if slot == self.choose else (180, 180, 180)
            prefix = "> " if slot == self.choose else ""

            text = self.font.render(
                f"{prefix}save №{slot}",
                True,
                color,
            )

            self.screen.blit(
                text,
                (self.saves_x, self.saves_y + (slot - 1) * self.spacing),
            )

        if config.is_mobile:
            self.joystick.draw(self.screen)
