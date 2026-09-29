import config
import pygame

def joystick_update(self):
    joy_y = config.joystick_vector[1]

    if joy_y > 0.5 and self.joy_ready:
        self._move_selection(1)
        self.joy_ready = False
    elif joy_y < -0.5 and self.joy_ready:
        self._move_selection(-1)
        self.joy_ready = False
    elif abs(joy_y) < 0.2:
        self.joy_ready = True


def draw_btn(self, triggered: bool, event=None):
    if triggered:
        return self.btn.collidepoint(event.pos)
    else:
        self.btn = pygame.Rect(
            self.SCREEN_W * 0.9,
            self.SCREEN_H * 0.6,
            self.SCREEN_W * 0.05,
            self.SCREEN_H * 0.1,
        )
        self.btn_font = pygame.font.Font(None, int(self.SCREEN_H // 30))
        self.btn_text = self.btn_font.render("Choose", True, "Black")
        self.BtnRect = self.btn_text.get_rect(center=self.btn.center)
        pygame.draw.circle( self.screen, (128, 128, 128), self.btn.center, self.SCREEN_H * 0.05)
        self.screen.blit(self.btn_text, self.BtnRect)


def activate(self, event):
    action_triggered = False

    if event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
            action_triggered = True

        if event.key in (pygame.K_DOWN, pygame.K_s):
            self._move_selection(1)
        elif event.key in (pygame.K_UP, pygame.K_w):
            self._move_selection(-1)

    elif event.type == pygame.MOUSEBUTTONDOWN and not config.is_mobile:
        if hasattr(self, "btn"):
            action_triggered = draw_btn(self, True, event)

    return action_triggered