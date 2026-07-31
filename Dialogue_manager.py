import json
import pygame

class DialogueManager:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.nodes = {}          # Здесь будут храниться все реплики сцены
        self.current_node = None # ID текущей реплики (например, "start")
        self.is_active = False   # Идет ли диалог прямо сейчас
        self.selected_choice = 0 # Индекс выбранного игроком ответа

    def load_dialogue(self, json_path):
        """Загружает JSON-файл сюжета и запускает его"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.nodes = data.get("nodes", {})
                self.current_node = "start"
                self.is_active = True
                self.selected_choice = 0
        except Exception as e:
            print(f"Ошибка чтения JSON-сценария {json_path}: {e}")
            self.is_active = False

    def handle_input(self, event):
        if not self.is_active:
            return None

        node = self.nodes.get(self.current_node)
        if not node:
            return None

        # Листаем диалог по нажатию на ПРОБЕЛ или ENTER
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                # Проверяем, есть ли указание на следующую ноду
                next_node = node.get("next")
                
                if not next_node:
                    self.is_active = False
                    return "END_DIALOGUE"
                    
                if next_node.startswith("TRIGGER_"):
                    # Если это триггер (ввод имени или битва) — отдаем его в сцену
                    return next_node

                # Переключаемся на следующую реплику
                self.current_node = next_node
                return None
        return None

    def _advance_to_node(self, next_node):
        """Внутренний метод для перехода на следующую ноду сюжета"""
        if not next_node:
            self.is_active = False
            return "END_DIALOGUE"
            
        # Если строка начинается с TRIGGER_, отдаем этот сигнал в сцену
        if next_node.startswith("TRIGGER_"):
            self.is_active = False
            return next_node

        self.current_node = next_node
        self.selected_choice = 0
        return None

    def get_current_emotion(self):
        """Возвращает эмоцию Акане для текущей реплики"""
        if self.is_active and self.current_node in self.nodes:
            return self.nodes[self.current_node].get("emotion", "Normal")
        return "Normal"

    def draw(self, box_x, box_y, box_w, box_h):
        """Отрисовывает текст и варианты ответов внутри готового текстбокса"""
        if not self.is_active:
            return

        node = self.nodes.get(self.current_node)
        if not node:
            return

        speaker = node.get("speaker", "")
        text = node.get("text", "")
        choices = node.get("choices", [])

        # Отрисовка имени говорящего (если оно есть) чуть выше плашки
        if speaker:
            name_color = (255, 105, 180) if speaker == "Akane" else (0, 255, 255)
            name_surf = self.font.render(f"{speaker}:", True, name_color)
            self.screen.blit(name_surf, (box_x + 20, box_y - 35))

        # Отрисовка основного текста реплики
        text_surf = self.font.render(text, True, (0, 255, 0))
        self.screen.blit(text_surf, (box_x + 30, box_y + 25))

        # Отрисовка вариантов ответов
        if choices:
            for i, choice in enumerate(choices):
                color = (255, 255, 0) if i == self.selected_choice else (255, 255, 255)
                prefix = "> " if i == self.selected_choice else "  "
                choice_surf = self.font.render(f"{prefix}{choice['text']}", True, color)
                self.screen.blit(choice_surf, (box_x + 40, box_y + 80 + (i * 30)))

    def get_akane_config(self):
            """Возвращает настройки Акане для текущей реплики"""
            if self.is_active and self.current_node in self.nodes:
                return self.nodes[self.current_node].get("akane_config", {"spawned": False})
            return {"spawned": False}