import config, pygame
from engine.joystick import VirtualJoystick
from engine.load_character_module import load_and_scale_character as lasc
from scenes.BaseScene import Scene

import json
import os


class Saves(Scene):
    """Save/load screen with three save slots.

    Game state is stored in JSON files so the scene does not depend on a
    separate save system. Runtime-only values (platform, paths, joystick
    state) are intentionally not saved.
    """

    SAVE_KEYS = (
        "player_name",
        "money",
        "trust_level",
        "current_day",
        "is_hungry",
        "is_onScreen",
        "akane_x",
        "akane_y",
        "akane_scene",
        "unlocked_costumes",
        "inventory",
        "current_costume",
    )

    def __init__(self, manager):
        super().__init__(manager)

        self.joystick = VirtualJoystick(self.SCREEN_W, self.SCREEN_H)
        self.choose = 1
        self.max_saves = 3
        self.joy_ready = True

        self.status_text = ""
        self.status_timer = 0

        pygame.font.init()
        self.font = pygame.font.Font(None, max(24, int(self.SCREEN_H // 15)))
        self.status_font = pygame.font.Font(None, max(20, int(self.SCREEN_H // 28)))
        self.spacing = int(self.SCREEN_H // 12)
        self.saves_x = int(self.SCREEN_W // 10)
        self.saves_y = int(self.SCREEN_H * 0.1)

        self.bg = self._load_background()

        self.load_save_btn = pygame.Rect(
            int(self.SCREEN_W * 0.1),
            int(self.SCREEN_H * 0.1),
            int(self.SCREEN_W * 0.8),
            int(self.SCREEN_H * 0.2),
        )

    # ------------------------------------------------------------------
    # Paths / files

    def _save_directory(self):
        if config.is_mobile:
            return os.path.join(config.mobile_path, "saves")
        return os.path.join("saves")

    def _save_path(self, slot):
        return os.path.join(self._save_directory(), f"save_{slot}.json")

    # ------------------------------------------------------------------
    # Assets

    def _load_background(self):
        if config.is_mobile:
            path = os.path.join(
                config.mobile_path,
                "assets",
                "Image",
                "Saves_BG.png",
            )
        else:
            path = os.path.join("assets", "Image", "Saves_BG.png")

        try:
            bg = pygame.image.load(path).convert()
            return pygame.transform.smoothscale(
                bg,
                (self.SCREEN_W, self.SCREEN_H),
            )
        except (FileNotFoundError, pygame.error) as e:
            print(f"Error loading Saves background: {e}")
            return pygame.Surface((self.SCREEN_W, self.SCREEN_H))

    # ------------------------------------------------------------------
    # Save system

    def _collect_game_state(self):
        state = {}

        for key in self.SAVE_KEYS:
            if hasattr(config, key):
                state[key] = getattr(config, key)

        return state

    def _apply_game_state(self, state):
        for key in self.SAVE_KEYS:
            if key in state:
                setattr(config, key, state[key])

    def save_game(self, slot=None):
        slot = self.choose if slot is None else slot

        if not 1 <= slot <= self.max_saves:
            return False

        try:
            os.makedirs(self._save_directory(), exist_ok=True)

            data = {
                "version": 1,
                "state": self._collect_game_state(),
            }

            with open(self._save_path(slot), "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)

            self._set_status(f"Игра сохранена в слот {slot}")
            return True

        except (OSError, TypeError, ValueError) as e:
            print(f"Error saving slot {slot}: {e}")
            self._set_status("Ошибка сохранения")
            return False

    def load_game(self, slot=None):
        slot = self.choose if slot is None else slot

        if not 1 <= slot <= self.max_saves:
            return False

        path = self._save_path(slot)

        if not os.path.isfile(path):
            self._set_status(f"Слот {slot} пуст")
            return False

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            state = data.get("state", data)
            if not isinstance(state, dict):
                raise ValueError("Invalid save data")

            self._apply_game_state(state)
            self._set_status(f"Игра загружена из слота {slot}")
            return True

        except (OSError, json.JSONDecodeError, TypeError, ValueError) as e:
            print(f"Error loading slot {slot}: {e}")
            self._set_status("Ошибка загрузки")
            return False

    def has_save(self, slot):
        return os.path.isfile(self._save_path(slot))

    def delete_save(self, slot=None):
        slot = self.choose if slot is None else slot

        if not 1 <= slot <= self.max_saves:
            return False

        try:
            os.remove(self._save_path(slot))
            self._set_status(f"Слот {slot} удалён")
            return True
        except FileNotFoundError:
            self._set_status(f"Слот {slot} пуст")
            return False
        except OSError as e:
            print(f"Error deleting slot {slot}: {e}")
            self._set_status("Ошибка удаления")
            return False

    # ------------------------------------------------------------------
    # Input / UI

    def _select_next(self):
        self.choose = self.choose + 1 if self.choose < self.max_saves else 1

    def _select_previous(self):
        self.choose = self.choose - 1 if self.choose > 1 else self.max_saves

    def _set_status(self, text, duration=120):
        self.status_text = text
        self.status_timer = duration

    def handle_events(self, event):
        self.joystick.handle_events(event)

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self._select_next()
                return

            if event.key in (pygame.K_UP, pygame.K_w):
                self._select_previous()
                return

            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.save_game()
                return

            if event.key == pygame.K_l:
                self.load_game()
                return

            if event.key == pygame.K_DELETE:
                self.delete_save()
                return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not config.is_mobile or event.button != 1:
                return

            mouse_x, mouse_y = event.pos

            for slot in range(1, self.max_saves + 1):
                rect = self._slot_rect(slot)
                if rect.collidepoint(mouse_x, mouse_y):
                    self.choose = slot
                    self.load_game()
                    return

    def update(self):
        super().update()
        self.joystick.update()

        joy_y = config.joystick_vector[1]

        if joy_y > 0.5 and self.joy_ready:
            self._select_next()
            self.joy_ready = False
        elif joy_y < -0.5 and self.joy_ready:
            self._select_previous()
            self.joy_ready = False
        elif abs(joy_y) < 0.2:
            self.joy_ready = True

        if self.status_timer > 0:
            self.status_timer -= 1

    def _slot_rect(self, slot):
        y = self.saves_y + (slot - 1) * self.spacing
        return pygame.Rect(
            self.saves_x,
            y,
            int(self.SCREEN_W * 0.8),
            self.spacing,
        )

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        for slot in range(1, self.max_saves + 1):
            selected = slot == self.choose
            color = (200, 0, 0) if selected else (180, 180, 180)
            prefix = "> " if selected else ""
            state = "" if self.has_save(slot) else " [empty]"

            text = self.font.render(
                f"{prefix}save №{slot}{state}",
                True,
                color,
            )

            rect = self._slot_rect(slot)
            self.screen.blit(text, (rect.x, rect.y))

        if self.status_timer > 0 and self.status_text:
            status = self.status_font.render(self.status_text, True, (220, 220, 220))
            status_rect = status.get_rect(center=(self.SCREEN_W // 2, int(self.SCREEN_H * 0.8)))
            self.screen.blit(status, status_rect)

        if config.is_mobile:
            self.joystick.draw(self.screen)
