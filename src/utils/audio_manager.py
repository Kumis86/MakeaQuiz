import pygame

class AudioManager:
    def __init__(self):
        try:
            pygame.mixer.init()
            print("[AudioManager] Berjalan secara normal")
        except Exception as e:
            print(f"[AudioManager] Gagal menginisialisasi pygame.mixer: {e}")   

        self.current_music = None
        self.paused = False

    def play_music(self, path, volume=1.0, loop=-1):
        try:
            if self.current_music != path:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loop)
                self.current_music = path
                self.paused = False
            elif self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
        except Exception as e:
            print(f"[AudioManager] Error playing music: {e}")

    def pause_music(self):
        if self.current_music and pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True

    def stop_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        self.current_music = None
        self.paused = False
    

    def play_sound_effect(self, path):
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(1.0)
            sound.play()
        except Exception as e:
            print(f"[AudioManager] Error playing sound effect: {e}")