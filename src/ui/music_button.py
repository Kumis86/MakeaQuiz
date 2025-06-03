import customtkinter as ctk
import pygame

class MusicButton:
    def __init__(self, parent, play_func, stop_func):
        self.play_func = play_func
        self.stop_func = stop_func
        
        # Inisialisasi tombol dengan style awal
        self.btn = ctk.CTkButton(
            parent,
            text="▶",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="#2CC985",
            hover_color="#25A56F",
            command=self.toggle
        )
        
        # Posisikan tombol di kanan bawah
        self.btn.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)
        
        # Mulai auto-update status tombol
        self.update_button_state()
    
    def toggle(self):
        """Toggle status musik dan update tampilan tombol"""
        if pygame.mixer.music.get_busy():
            self.stop_func()
            self.update_button_appearance(False)
        else:
            self.play_func()
            self.update_button_appearance(True)
    
    def update_button_appearance(self, is_playing):
        """Update tampilan tombol berdasarkan status musik"""
        if is_playing:
            self.btn.configure(text="⏹", fg_color="#FF4D4D", hover_color="#E64444")
        else:
            self.btn.configure(text="▶", fg_color="#2CC985", hover_color="#25A56F")
    
    def update_button_state(self):
        """Auto-update status tombol setiap 100ms"""
        is_playing = pygame.mixer.music.get_busy()
        self.update_button_appearance(is_playing)
        self.btn.after(100, self.update_button_state) 