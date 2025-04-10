import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None

    def play_music(self, path, volume=1.0, loop=-1):
        try:
            if self.current_music != path:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loop)
                self.current_music = path
        except Exception as e:
            print(f"[AudioManager] Error playing music: {e}")

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None

    def play_sound_effect(self, path):
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(1.0)
            sound.play()
        except Exception as e:
            print(f"[AudioManager] Error playing sound effect: {e}")