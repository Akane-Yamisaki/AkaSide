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

        pygame.font.init()
        self.font = pygame.font.Font(None, int(self.SCREEN_H // 15))
        self.spacing = int(self.SCREEN_H // 20)
        self.saves_x = int(self.SCREEN_W // 10)
        self.saves_y = int(self.SCREEN_H * 0.1)
        
        try:
            if config.is_mobile:
                bg = pygame.image.load(config.mobile_path + "assets/Image/Saves_BG.png").convert()
                # same with char
            else:
                bg = pygame.image.load("assets/Image/Saves_BG.png").convert()
                # same with char
            self.bg = pygame.transform.smoothscale(bg,(self.SCREEN_W, self.SCREEN_H))
        except FileNotFoundError as e:
            print(f'Error: {e}')
            pass
            
        self.load_save_btn = pygame.Rect(self.SCREEN_W * 0.1 self.SCREEN_H * 0.1, self.SCREEN_W * 0.8, self.SCREEN_H * 0.2)
        

    def handle_events(self, event):
        self.joystick.handle_events(event)
        action_triggered = False
        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                action_triggered = True
                
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_s]:
                if self.choose < self.max_saves: self.choose += 1
                else: self.choose = 1

            if keys[pygame.K_w]:
                if self.choose < 2: self.choose = self.max_saves
                else: self.choose -= 1
            
        elif event.type == pygame.MOUSEBUTTONDOWN and config.is_mobile:
            mouse_pos = event.pos
            action_triggered = None # btn here

        if action_triggered:
            # function
            pass

    def update(self):
        super().update()
        self.joystick.update()
        
        if not hasattr(self, 'joy_ready'):
            self.joy_ready = True

        joy_y = config.joystick_vector[1]
        
        if joy_y > 0.5 and self.joy_ready:
            if self.choose < self.max_saves: self.choose += 1
            else: self.choose = 1
            self.joy_ready = False
        elif joy_y < -0.5 and self.joy_ready:
            if self.choose < 2: self.choose = self.max_saves
            else: self.choose -= 1
            self.joy_ready = False
        elif abs(joy_y) < 0.2:
            self.joy_ready = True
        
    def draw(self):
        self.screen.blit(self.bg,(0,0))
        # char here

        for item_number in self.max_saves:
            if item_number == self.choose:
                color = (200,0,0)
                display_text = f"> save №{item_number}"
                current_x = self.saves_x + 15
            else:
                color = (180,180,180)
                display_text = f"save №{item_number}"
                current_x = self.saves_x
                
        text = self.font.render(display_text, True, color)
        current_y = self.saves_y + (item_number * self.spacing)
        self.screen.blit(text, (current_x, current_y))
                        
        if config.is_mobile:
            self.joystick.draw(self.screen)
            # btn here
