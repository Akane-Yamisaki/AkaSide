import pygame
import math
import config

class VirtualJoystick:
    def __init__(self, screen_w, screen_h):
        scale = screen_h / 1080 
        self.base_radius = int(100 * scale)
        self.stick_radius = int(40 * scale)

        # ВОТ ЭТИ ДВЕ СТРОЧКИ ОБЯЗАНЫ ТАМ БЫТЬ:
        self.base_center = (250, screen_h - 250) # Или (250, 500) для твоего ПК-теста
        self.stick_center = list(self.base_center) # Стик изначально стоит ровно в центре базы

        
        self.is_dragging = False
        self.pointer_id = None # Для корректного мультитача в будущем

    def handle_events(self, event):
        if not config.is_mobile:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            m_x, m_y = pygame.mouse.get_pos()
            # Проверяем, нажал ли игрок именно на джойстик
            distance = math.hypot(m_x - self.base_center[0], m_y - self.base_center[1])
            if distance <= self.base_radius:
                self.is_dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.is_dragging = False
                # Возвращаем стик в центр и обнуляем движение
                self.stick_center = list(self.base_center)
                config.joystick_vector = [0.0, 0.0]

    def update(self):
        if not config.is_mobile or not self.is_dragging:
            return

        m_x, m_y = pygame.mouse.get_pos()
        
        # Считаем вектор от центра базы до пальца
        dx = m_x - self.base_center[0]
        dy = m_y - self.base_center[1]
        distance = math.hypot(dx, dy)

        if distance == 0:
            config.joystick_vector = [0.0, 0.0]
            return

        # Если палец ушел слишком далеко, ограничиваем стик радиусом базы
        if distance > self.base_radius:
            scale = self.base_radius / distance
            self.stick_center[0] = self.base_center[0] + dx * scale
            self.stick_center[1] = self.base_center[1] + dy * scale
            # Нормализуем вектор до максимальной единицы (1.0)
            config.joystick_vector = [dx / distance, dy / distance]
        else:
            self.stick_center[0] = m_x
            self.stick_center[1] = m_y
            # Сила наклона зависит от дальности пальца от центра
            config.joystick_vector = [dx / self.base_radius, dy / self.base_radius]

    def draw(self, screen):
        if not config.is_mobile:
            return

        # Рисуем полупрозрачную базу (внешний круг)
        base_surf = pygame.Surface((self.base_radius * 2, self.base_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(base_surf, (255, 255, 255, 40), (self.base_radius, self.base_radius), self.base_radius)
        pygame.draw.circle(base_surf, (255, 255, 255, 90), (self.base_radius, self.base_radius), self.base_radius, 3)
        screen.blit(base_surf, (self.base_center[0] - self.base_radius, self.base_center[1] - self.base_radius))

        # Рисуем стик (внутренний круг, за который держимся)
        stick_surf = pygame.Surface((self.stick_radius * 2, self.stick_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(stick_surf, (255, 0, 0, 150), (self.stick_radius, self.stick_radius), self.stick_radius)
        screen.blit(stick_surf, (int(self.stick_center[0] - self.stick_radius), int(self.stick_center[1] - self.stick_radius)))