import pygame
import os

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.is_muted = False
        self.background_music = None
        self.wrong_answer_sound = None
        self.load_audio_files()
        
    def load_audio_files(self):
        """Memuat file audio dari folder audio"""
        try:
            # Memuat background music
            if os.path.exists("audio/background_music.mp3"):
                self.background_music = pygame.mixer.Sound("audio/background_music.mp3")
                self.background_music.set_volume(0.5)  # Set volume 50%
            
            # Memuat suara jawaban salah
            if os.path.exists("audio/wrong_answer.mp3"):
                self.wrong_answer_sound = pygame.mixer.Sound("audio/wrong_answer.mp3")
                self.wrong_answer_sound.set_volume(0.7)
        except Exception as e:
            print(f"Error loading audio files: {e}")
    
    def play_background_music(self):
        """Memutar background music dalam loop"""
        if self.background_music and not self.is_muted:
            self.background_music.play(-1)  # -1 untuk loop tak terbatas
    
    def stop_background_music(self):
        """Menghentikan background music"""
        if self.background_music:
            self.background_music.stop()
    
    def play_wrong_answer(self):
        """Memutar suara jawaban salah"""
        if self.wrong_answer_sound and not self.is_muted:
            self.wrong_answer_sound.play()
    
    def toggle_mute(self):
        """Toggle mute/unmute semua suara"""
        self.is_muted = not self.is_muted
        if self.is_muted:
            self.stop_background_music()
        else:
            self.play_background_music()
        return self.is_muted 