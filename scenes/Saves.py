import config, pygame
from engine.joystick import VirtualJoystick
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
        self.saves_x = self.SCREEN_W // 3
        self.saves_y = self.SCREEN_H // 3

        self.bg = self.load_background()

        self.radius = int(self.SCREEN_H * 0.025)
        self.center_x = int(self.saves_x - self.SCREEN_W * 0.05)
        self.center_y = int(self.saves_y - self.SCREEN_H * 0.05)

        self.circle_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        
        self.rect = pygame.Rect(
            self.center_x - self.radius, 
            self.center_y - self.radius, 
            self.radius * 2, 
            self.radius * 2
        )

        self.button_surf = pygame.Surface((self.SCREEN_W * 0.08, self.SCREEN_H * 0.05), pygame.SRCALPHA)

        self.save_x = int(self.saves_x + self.SCREEN_W * 0.15)

    def load_background(self):
        try:
            if config.is_mobile:
                bg = pygame.image.load(config.mobile_path + "assets/Images/Saves_BG.png").convert()
            else:
                bg = pygame.image.load("assets/Images/Saves_BG.png").convert()

            return pygame.transform.smoothscale(bg,(self.SCREEN_W, self.SCREEN_H))
        
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

            elif event.key == pygame.K_ESCAPE:
                self.manager.scene = "menu"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.manager.scene = "menu"
                    return

                for slot in range(1, self.max_saves + 1):
                    button_rect = pygame.Rect(self.save_x, self.saves_y + (slot - 1) * self.spacing, self.SCREEN_W * 0.08, self.SCREEN_H * 0.05)
                    button_rect2 = pygame.Rect(self.save_x + self.SCREEN_W * 0.1, self.saves_y + (slot - 1) * self.spacing, self.SCREEN_W * 0.08, self.SCREEN_H * 0.05)

                    if button_rect.collidepoint(event.pos):
                        self.timelines(slot, "save")
                        break
                    elif button_rect2.collidepoint(event.pos):
                        self.timelines(slot, "del")
                        break

    def timelines(self, slot, command):
        print(f'{slot}: {command}')
        pass

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
        mouse_pos = pygame.mouse.get_pos()

        self.circle_surface.fill((0, 0, 0, 0)) 
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.circle(self.circle_surface, (194, 27, 38, 200), (self.radius, self.radius), self.radius)
        else:
            pygame.draw.circle(self.circle_surface, (242, 121, 129, 130), (self.radius, self.radius), self.radius)

        pygame.draw.circle(self.circle_surface, (230,70,120), (self.radius, self.radius), self.radius, 3)
        self.screen.blit(self.circle_surface, self.rect.topleft)

        text_surf = self.font.render("X", True, (180, 180, 180))
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.screen.blit(text_surf, text_rect)

        for slot in range(1, self.max_saves + 1):
            color = (200, 0, 0) if slot == self.choose else (180, 180, 180)
            prefix = "> " if slot == self.choose else ""

            text = self.font.render(f"{prefix}слот {slot}",True,color,)
            save_txt = self.font.render("Save", True, (180, 180, 180))
            delete_txt = self.font.render("Del", True, (180, 180, 180))

            button_rect = pygame.Rect(self.save_x, self.saves_y + (slot - 1) * self.spacing, self.SCREEN_W * 0.08, self.SCREEN_H * 0.05)
            outline_rect = button_rect.inflate(3,3)
            button_rect2 = pygame.Rect(self.save_x + self.SCREEN_W * 0.1, self.saves_y + (slot - 1) * self.spacing, self.SCREEN_W * 0.08, self.SCREEN_H * 0.05)
            outline_rect2 = button_rect2.inflate(3,3)

            self.screen.blit(text,(self.saves_x, self.saves_y + (slot - 1) * self.spacing),)

            if button_rect.collidepoint(mouse_pos):
                self.button_surf.fill((50, 30, 70, 200))
            else:
                self.button_surf.fill((30, 20, 40, 130))

            self.screen.blit(self.button_surf, button_rect)
            save_rect = save_txt.get_rect(center=button_rect.center)
            self.screen.blit(save_txt, save_rect)
            pygame.draw.rect(self.screen, (230,70,120), outline_rect, 2, 7)

            if button_rect2.collidepoint(mouse_pos):
                self.button_surf.fill((196, 22, 54, 200))
            else:
                self.button_surf.fill((179, 48, 94, 130))

            self.screen.blit(self.button_surf, button_rect2)
            delete_rect = delete_txt.get_rect(center=button_rect2.center)
            self.screen.blit(delete_txt, delete_rect)
            pygame.draw.rect(self.screen, (237, 123, 144), outline_rect2, 2, 7)

        if config.is_mobile:
            self.joystick.draw(self.screen)
