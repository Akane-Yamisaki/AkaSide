# Full AI code
import sys
import pygame

IS_WINDOWS = sys.platform == "win32"

if IS_WINDOWS:
    try:
        from winotify import Notification, audio
        HAS_WINOTIFY = True
    except ImportError:
        HAS_WINOTIFY = False
else:
    HAS_WINOTIFY = False


class NotificationManager:
    def __init__(self, app_id="AkaSide", font_size=28):
        self.app_id = app_id
        self.text = ""
        self.timer = 0
        self.font = pygame.font.Font(None, font_size)

    def send(self, text, duration_frames=180, win_toast=True, win_title=None):
        """Запускает уведомление в Pygame и (опционально) тост в Windows."""
        self.text = text
        self.timer = duration_frames

        if win_toast and IS_WINDOWS and HAS_WINOTIFY:
            try:
                toast = Notification(
                    app_id=self.app_id,
                    title=win_title or self.app_id,
                    msg=text,
                    duration="short"
                )
                toast.set_audio(audio.Default, loop=False)
                toast.show()
            except Exception:
                pass  # Защита на случай системных сбоев уведомлений

    def draw(self, screen, pos=(20, 20), color=(255, 220, 100)):
        """Отрисовывает текст в углу экрана. Вызывать каждый кадр перед flip()."""
        if self.timer > 0:
            surf = self.font.render(self.text, True, color)
            screen.blit(surf, pos)
            self.timer -= 1