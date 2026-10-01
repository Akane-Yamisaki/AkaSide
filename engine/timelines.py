import json, config, os

def save_data(slot, manager):
    data = {
        "Player_name": config.player_name,
        "Money": config.money,
        "Trust_level": config.trust_level,
        "Current_day": config.current_day,
        "Akane_coordinates": (config.akane_x, config.akane_y),
        "Is_hungry": config.is_hungry,
        "Is_OnScreen": config.is_onScreen,
        "Akane_location": config.akane_scene,
        "Inventory": config.inventory,
        "Costume": config.current_costume,
        "Game_state": manager.prev_game_state,
        "Player_pos": (config.player_x, config.player_y)
    }

    # for key, value in data.items():
    #     print(f"{key}: {type(value)}")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_dir = os.path.join(base_dir, "saves")
    
    os.makedirs(save_dir, exist_ok=True)
    
    save_path = os.path.join(save_dir, f"save{slot}.json")
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

def delete_data(slot):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_dir = os.path.join(base_dir, "saves")
        
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, f"save{slot}.json")
    if os.path.exists(save_path):
        os.remove(save_path)
        print(f"Сейв {slot} удалён")
    else:
        print(f"Сейв {slot} не найден.")

def load_data(slot, manager):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_dir = os.path.join(base_dir, "saves")
        
    os.makedirs(save_dir, exist_ok=True)
        
    save_path = os.path.join(save_dir, f"save{slot}.json")
    if os.path.isfile(save_path):
        with open(save_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            config.player_name = data['Player_name']
            config.money = data['Money']
            config.trust_level = data['Trust_level']
            config.current_day = data['Current_day']
            config.akane_x, config.akane_y = data['Akane_coordinates']
            config.is_hungry = data['Is_hungry']
            config.is_onScreen = data['Is_OnScreen']
            config.akane_scene = data['Akane_location']
            config.inventory = data['Inventory']
            config.current_costume = data['Costume']
            manager.game_state = data['Game_state']
            manager.scene = data['Game_state']
