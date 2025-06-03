import customtkinter as ctk

class PlayMusicButton(ctk.CTkButton):
    def __init__(self, parent, audio_manager, music_path):
        super().__init__(parent, text="▶️ Play Music", command=self.play_music)
        self.audio_manager = audio_manager
        self.music_path = music_path

    def play_music(self):
        self.audio_manager.play_music(self.music_path)