import config
import pygame
from dialogue.Dialogue_manager import DialogueManager
from engine.load_character_module import load_and_scale_character
from engine.pc_warning import crash, show_boss_error
import interaction.choose as choose
from scenes.BaseScene import Scene

class HouseScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)

        self.input_mode = False
        self.typed_name = ""

        if config.is_mobile:
            self.akane_sprites = {"Normal": load_and_scale_character(config.mobile_path + "assets/Images/Akane/Normal_2.png",int(self.SCREEN_H * 1),)
            }
        else:
            self.akane_sprites = {"Normal": load_and_scale_character("assets/Images/Akane/Normal_2.png", int(self.SCREEN_H * 1))
            }

        try:
            if config.is_mobile:
                raw_bg = pygame.image.load(config.mobile_path + "assets/Images/Locations/Akane_bedroom.png").convert()
            else:
                raw_bg = pygame.image.load("assets/Images/Locations/Akane_bedroom.png").convert()
            self.bg = pygame.transform.smoothscale(raw_bg, (self.SCREEN_W, self.SCREEN_H))
        except Exception as e:
            print(f"Ошибка загрузки фона: {e}")
            self.bg = pygame.Surface((self.SCREEN_W, self.SCREEN_H))

        font_size = int(self.SCREEN_H * 0.03)
        self.font = pygame.font.SysFont("arial", font_size)

        self.dialogue_sys = DialogueManager(self.screen, self.font)
        self.dialogue_sys.load_dialogue("dialogue/Dialogues/intro.json")

    def handle_events(self, event):
        current_state = self.manager.game_state
        super().handle_events(event)

        # Проверяем клик по ПК-кнопке "Choose" через мышку, используя контекст СЦЕНЫ (self)
        activation_triggered = False
        if event.type == pygame.MOUSEBUTTONDOWN and config.is_mobile:
            if hasattr(self, "btn"):
                activation_triggered = choose.draw_btn(self, True, event)

        # СОСТОЯНИЕ: Ввод имени персонажа
        if current_state == "input_name":
            if activation_triggered:
                if self.typed_name.strip() != "":
                    self._confirm_name()
                return

            if event.type == pygame.KEYDOWN:
                # Если нажали ENTER на клавиатуре
                if event.key == pygame.K_RETURN:
                    if self.typed_name.strip() != "":
                        self._confirm_name()

                # Удаление символа (работает и на ПК, и со смартфона через родную клавиатуру)
                elif event.key == pygame.K_BACKSPACE:
                    self.typed_name = self.typed_name[:-1]
                else:
                    if len(self.typed_name) < 12 and (event.unicode.isalnum() or event.unicode == " "):
                        self.typed_name += event.unicode
            return

        # СОСТОЯНИЕ: Обычный диалог / Новелла
        elif current_state == "dialogue":
            if activation_triggered:
                # Симулируем нажатие ENTER для менеджера диалогов
                dummy_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
                trigger = self.dialogue_sys.handle_input(dummy_event)
                activation_triggered = False
            elif event.type == pygame.KEYDOWN:
                trigger = self.dialogue_sys.handle_input(event)
            else:
                return

            # Проверяем триггеры из JSON диалога
            if trigger == "TRIGGER_INPUT_NAME":
                self.manager.game_state = "input_name"
            elif trigger == "BATTLE":
                print("Переключаемся на битву Undertale!")
            elif trigger == "TRIGGER_END_DIALOGUE" or trigger == "END_DIALOGUE":
                print("Интро завершено! Включаем режим исследования.")
                self.manager.game_state = "exploration"
                self.manager.scene = "Bedroom_pixel"
                return

    def _confirm_name(self):
        config.player_name = self.typed_name.strip()
        self.input_mode = False

        if config.player_name.lower() in ["павел", "pavel"]:
            print("ХОРРОР ТРИГГЕР: Аканэ замерла...")
            config.trust_level = -50
            self.dialogue_sys.current_node = "pavel_horror"
            show_boss_error('FATAL ERROR: Akane required admin permissions...')
            crash(f'FATAL ERROR: ACCESS DENIED \nCLOSING AKASIDE.EXE')
        else:
            self.dialogue_sys.current_node = "check_pavel"

        self.dialogue_sys.is_active = True
        self.dialogue_sys.selected_choice = 0
        self.manager.game_state = "dialogue"

    def update(self):
        super().update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        box_w = self.SCREEN_W - 80
        box_h = 160
        box_x = 40
        box_y = self.SCREEN_H - box_h - 40

        akane_config = self.dialogue_sys.get_akane_config()
        is_spawned = (akane_config.get("spawned", False) if self.manager.game_state != "visual_novel_roam" else True)

        if is_spawned:
            current_emotion = (akane_config.get("emotion", "Normal") if self.manager.game_state != "visual_novel_roam" else "Normal")
            base_sprite = self.akane_sprites.get(current_emotion, self.akane_sprites["Normal"])
            final_sprite = base_sprite

            if (self.manager.game_state != "visual_novel_roam"and akane_config.get("status") == "inactive"):
                old_w, old_h = base_sprite.get_size()
                new_w = int(old_w * 0.7)
                new_h = int(old_h * 0.7)
                final_sprite = pygame.transform.smoothscale(base_sprite, (new_w, new_h))

                final_sprite = final_sprite.copy()
                dark_filter = pygame.Surface((new_w, new_h), pygame.SRCALPHA)
                dark_filter.fill((100, 100, 100, 0))
                final_sprite.blit(dark_filter, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                final_sprite.set_alpha(200)

            akane_x = (self.SCREEN_W // 2) - (final_sprite.get_width() // 2)
            akane_y = box_y - final_sprite.get_height() + 120
            self.screen.blit(final_sprite, (akane_x, akane_y))

        if self.manager.game_state != "visual_novel_roam":
            textbox = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
            textbox.fill((0, 0, 0, 180))
            self.screen.blit(textbox, (box_x, box_y))

            if self.manager.game_state == "input_name":
                name_surf = self.font.render("Вы:", True, (0, 255, 255))
                self.screen.blit(name_surf, (box_x + 20, box_y - 35))
                input_hint = self.font.render(f"Введите ваше имя: {self.typed_name}_",True,(255, 255, 255),)
                self.screen.blit(input_hint, (box_x + 30, box_y + 40))
                enter_hint = self.font.render("[Нажмите ENTER для подтверждения]",True,(150, 150, 150),)
                self.screen.blit(enter_hint, (box_x + 30, box_y + 100))
            else:
                self.dialogue_sys.draw(box_x, box_y, box_w, box_h)

        if self.manager.game_state == "visual_novel_roam":
            self.pat_pat()
        self.draw_balance()

        if config.is_mobile:
            choose.draw_btn(self, False, None)
