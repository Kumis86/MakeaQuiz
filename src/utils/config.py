# src/utils/config.py
class AppConfig:
    """Konfigurasi aplikasi MakeaQuiz"""
    def __init__(self):
        # Properti umum aplikasi
        self.app_name = "MakeaQuiz"
        
        # Warna tema
        self.bg_color = "#000000"
        self.text_color = "#FFFFFF"
        
        # Ukuran jendela aplikasi
        self.width = 1260
        self.height = 716
        
        # Konfigurasi sidebar
        self.sidebar_width = 299
        self.sidebar_color = "#1E1E1E"
        
        # Font yang digunakan di aplikasi
        self.font_title = ("Inter ExtraBoldItalic", 64)
        self.font_large_title = ("Inter ExtraBoldItalic", 128)
        self.font_small_title = ("Inter ExtraBoldItalic", 36)
        self.font_regular = ("Roboto", 16)
        self.font_input_label = ("Roboto Regular", 32)

        #path background music
        self.audio_paths = {
            "main_theme": "assets/audio/main_theme.mp3",
            "quiz_theme": "assets/audio/quiz_theme.mp3",
            "success": "assets/audio/success.wav",
            "fail": "assets/audio/fail.wav",
        }
