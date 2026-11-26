import ctypes, pygame, time, sys

IS_WINDOWS = sys.platform == "win32"

def show_boss_error(context):
    if IS_WINDOWS:
        ctypes.windll.user32.MessageBoxW(0, context, "AKANE.EXE", 0x10)

def crash(context):
    if IS_WINDOWS:
        ctypes.windll.user32.MessageBoxW(0, context, "System", 0x10)
        time.sleep(2)
        pygame.quit()
        sys.exit()

# 0x40 — Иконка информации (синяя буква «i») вместо ошибки.
# 0x30 — Иконка предупреждения (желтый треугольник).
# 0x1 — Кнопки «ОК» и «Отмена» (вместо одной «ОК»).
# 0x4 — Кнопки «Да» и «Нет».
# 0x10 - дефолт ошибка
