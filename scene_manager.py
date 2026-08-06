from scenes.Akane_Bedroom_Day1 import HouseScene
from scenes.Akane_Bedroom import BedRoom
from scenes.menu import Menu
from scenes.Saves import Saves

class SceneManager:
    def __init__(self, screen, SCREEN_W, SCREEN_H):
        self.screen = screen
        self.SCREEN_W = SCREEN_W
        self.SCREEN_H = SCREEN_H

        self.loaded_scenes = {}

        self.scenes = {
            'menu': Menu,
            'saves': Saves,
            'Bedroom_Day1': HouseScene,
            'Bedroom_pixel': BedRoom
        }

        self.__game_state = "menu" 

        self.__current_scene = self.load_scene("menu")

    def load_scene(self, scene_name):
        if scene_name in self.loaded_scenes:
            return self.loaded_scenes[scene_name]

        scene = self.scenes[scene_name]
        new_scene = scene(self) 
        
        self.loaded_scenes[scene_name] = new_scene
        return new_scene

    @property
    def scene(self):
        return self.__current_scene

    @scene.setter
    def scene(self, scene_name):
        if scene_name in self.scenes:
            self.__current_scene = self.load_scene(scene_name)

    @property
    def game_state(self):
        return self.__game_state

    @game_state.setter
    def game_state(self, state):
        self.__game_state = state

    def handle_events(self, event):
        self.__current_scene.handle_events(event)

    def update(self):
        self.__current_scene.update()

    def draw(self):
        self.__current_scene.draw()