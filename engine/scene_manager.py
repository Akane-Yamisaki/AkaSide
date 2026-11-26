import pygame
from scenes.Akane_Bedroom_Day1 import HouseScene
from scenes.Akane_Bedroom import BedRoom
from scenes.menu import Menu
from scenes.Saves import Saves
from scenes.gallery import Gallery

class SceneManager:
    def __init__(self, screen, SCREEN_W, SCREEN_H):
        self.screen = screen
        self.SCREEN_W = SCREEN_W
        self.SCREEN_H = SCREEN_H

        self.loaded_scenes = {}

        # True = keep the scene instance in memory.
        # False = create a fresh instance every time the scene is opened.
        self.scenes = {
            'menu': (Menu, True),
            'Saves': (Saves, False),
            'Bedroom_Day1': (HouseScene, True),
            'Bedroom_pixel': (BedRoom, True),
            'Gallery': (Gallery, False)
        }

        self.blacklist = ['menu', 'Saves', 'Gallery']

        self.__game_state = "menu"
        self.prev_game_state = ""

        self.current_track = None
        self.next_track = None
        self.music_state = "idle"  # "idle", "fading_out", "fading_in"
        self.fade_timer = 0
        self.fade_out_ms = 400
        self.fade_in_ms = 1200
        self.target_volume = 0.65

        self.__current_scene = self.load_scene("menu")
        if hasattr(self.__current_scene, "on_enter"):
            self.__current_scene.on_enter()
            print('music started for scene: ', self.__current_scene)

    def play_music(self, track_path, target_volume=0.65):
        self.target_volume = target_volume

        if self.current_track == track_path and self.music_state != "fading_out" and pygame.mixer.music.get_busy():
            return

        if self.music_state == "fading_out" and self.next_track == track_path:
            return

        if pygame.mixer.music.get_busy() and pygame.mixer.music.get_volume() > 0.01:
            self.next_track = track_path
            if self.music_state != "fading_out":
                self.music_state = "fading_out"
                self.fade_timer = pygame.time.get_ticks()
        else:
            self._start_track(track_path)

    def stop_music(self, fade_ms=500):
        if self.music_state == "idle" and not pygame.mixer.music.get_busy():
            return
        if self.music_state == "fading_out" and self.next_track is None:
            return

        self.next_track = None
        self.fade_out_ms = fade_ms
        self.music_state = "fading_out"
        self.fade_timer = pygame.time.get_ticks()

    def _start_track(self, track_path):
        if not track_path:
            pygame.mixer.music.stop()
            self.current_track = None
            self.music_state = "idle"
            return

        try:
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.set_volume(0.0)
            pygame.mixer.music.play(loops=-1)
            self.current_track = track_path
            self.music_state = "fading_in"
            self.fade_timer = pygame.time.get_ticks()
        except pygame.error as e:
            print(f"Ошибка загрузки трека {track_path}: {e}")

    def update_music(self):
        if self.music_state == "idle":
            return

        now = pygame.time.get_ticks()
        elapsed = now - self.fade_timer

        if self.music_state == "fading_out":
            progress = min(1.0, elapsed / self.fade_out_ms)
            vol = self.target_volume * ((1.0 - progress) ** 2)
            pygame.mixer.music.set_volume(vol)

            if progress >= 1.0:
                self._start_track(self.next_track)
                self.next_track = None

        elif self.music_state == "fading_in":
            progress = min(1.0, elapsed / self.fade_in_ms)
            vol = self.target_volume * (progress ** 2)
            pygame.mixer.music.set_volume(vol)

            if progress >= 1.0:
                self.music_state = "idle"

    def load_scene(self, scene_name):
        scene_class, cache = self.scenes[scene_name]

        if cache and scene_name in self.loaded_scenes:
            return self.loaded_scenes[scene_name]

        new_scene = scene_class(self)

        if cache:
            self.loaded_scenes[scene_name] = new_scene

        return new_scene

    def reload_scene(self, scene_name=None):
        if scene_name is None:
            scene_name = self.__game_state

        if scene_name in self.loaded_scenes:
            del self.loaded_scenes[scene_name]

        if scene_name == self.__game_state:
            self.__current_scene = self.load_scene(scene_name)

        return self.__current_scene

    def clear_cache(self):
        self.loaded_scenes.clear()

    @property
    def scene(self):
        return self.__current_scene

    @scene.setter
    def scene(self, scene_name):
        if scene_name in self.scenes:
            self.prev_game_state = self.__game_state if self.game_state not in self.blacklist else self.prev_game_state
            self.__current_scene = self.load_scene(scene_name)
            self.__game_state = scene_name
            if hasattr(self.__current_scene, "on_enter"):
                self.__current_scene.on_enter()
                # print('music started for scene: ', self.__current_scene)

    @property
    def game_state(self):
        return self.__game_state

    @game_state.setter
    def game_state(self, state):
        self.__game_state = state

    def handle_events(self, event):
        self.__current_scene.handle_events(event)

    def update(self):
        self.update_music()
        self.__current_scene.update()

    def draw(self):
        self.__current_scene.draw()
