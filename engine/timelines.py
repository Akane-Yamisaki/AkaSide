import json, config
from engine import scene_manager
from scenes import BaseScene

def save_data(slot):
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
        # "Scene": scene_manager.current_scene.scene,
        # "Game_state": BaseScene.Scene.current_state,
        "Player_pos": (config.player_x, config.player_y)
    }

    for key, value in data.items():
        print(f"{key}: {type(value)}")
    
    with open(f"saves/save{slot}.json", "w", encoding="utf-8") as f:
        json.dump(data,f)

def delete_data(slot):
    print(slot)