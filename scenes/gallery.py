import config, pygame
from engine.joystick import VirtualJoystick
from scenes.BaseScene import Scene

class Gallery(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.joystick = VirtualJoystick(self.SCREEN_W, self.SCREEN_H)
        self.choose = 1

        try:
            if config.is_mobile:
                self.bg = pygame.image.load(config.mobile_path + "assets/Images/Gallery_BG.png").convert()
            else:
                self.bg = pygame.image.load("assets/Images/Gallery_BG.png").convert()
        except:
            self.bg = pygame.Surface((self.SCREEN_W, self.SCREEN_H))

    def handle_events(self, event):
        self.joystick.handle_events(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.scene = "menu"

    def update(self):
        super().update()
        self.joystick.update()
    
        if config.joystick_vector[1] > 0.5 and self.joy_ready:
            pass
    
        elif config.joystick_vector[1] < -0.5 and self.joy_ready:
           pass
    
        elif abs(config.joystick_vector[1]) < 0.2:
            self.joy_ready = True

    def draw(self):
        self.screen.blit(self.bg, (0, 0))


        if config.is_mobile:
            self.joystick.draw(self.screen)