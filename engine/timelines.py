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
        "Player_pos": (config.player_x, config.player_y),
        "Can_sleep": config.can_sleep
    }

    data["signature"] = make_signature(data)
    
    app_data = os.getenv("LOCALAPPDATA") or os.path.expanduser("~")
    save_dir = os.path.join(app_data, "AkaSide/saves")
    os.makedirs(save_dir, exist_ok=True)
    
    save_path = os.path.join(save_dir, f"save{slot}.json")
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def delete_data(slot):
    app_data = os.getenv("LOCALAPPDATA") or os.path.expanduser("~")
    save_dir = os.path.join(app_data, "AkaSide/saves")
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, f"save{slot}.json")
    if os.path.exists(save_path):
        os.remove(save_path)
        print(f"Сейв {slot} удалён")
    else:
        print(f"Сейв {slot} не найден.")

def load_data(slot, manager):
    app_data = os.getenv("LOCALAPPDATA") or os.path.expanduser("~")
    save_dir = os.path.join(app_data, "AkaSide/saves")
    os.makedirs(save_dir, exist_ok=True)
        
    save_path = os.path.join(save_dir, f"save{slot}.json")
    try:
        if os.path.isfile(save_path):
            with open(save_path, "r", encoding="utf-8") as f:
                data = json.load(f)
    except json.JSONDecodeError:
        # Игрок сломал синтаксис JSON (забыл запятую или кавычку)
        trigger_hacker_event(manager, reason="broken_json")
        return

    if os.path.isfile(save_path):
        saved_sig = data.get("signature", "")
        if saved_sig != make_signature(data):
            # Игрок изменил любое значение в файле!
            trigger_hacker_event(manager, reason="tampered_data", tampered_data=data, slot=slot)
            return
    
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
            config.player_x, config.player_y = data['Player_pos']
            config.can_sleep = data['Can_sleep']
            manager.game_state = data['Game_state']
            manager.scene = data['Game_state']
