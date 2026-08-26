# config.py

# Данные игрока
player_name = ""
money = 0
Dlc_list = {"Dlc_18": False}

# Отношения с Аканэ
trust_level = 0        # Растет от подарков, еды и поглаживаний
current_day = 1        # Текущий день (влияет на фан-сервис и искажения)

# Состояние Аканэ
is_hungry = True       # Нужно кормить каждый день
is_onScreen = True
akane_x, akane_y = 0, 0
akane_scene = ""

# --- МОБИЛЬНОЕ УПРАВЛЕНИЕ ---
is_mobile = False
mobile_path = "/data/data/com.akaside.akaside/files/app/"
joystick_vector = [0.0, 0.0]  # Направление движения [X, Y] от -1.0 до 1.0

# Гардероб (купленные костюмы)
unlocked_costumes = {
    "default": True,
    "maid": False,
    "swimsuit": False,
    "without": Dlc_list.get("Dlc_18", False)
}

inventory = {}
current_costume = "default"