# main.py - Entry point utama aplikasi MakeaQuiz
import customtkinter as ctk
import traceback
import sys
import tkinter.messagebox as messagebox
import pygame


try:
    # Import komponen-komponen UI
    from src.ui.splash_screen import SplashScreen
    from src.ui.login_screen import LoginScreen
    from src.ui.signup_screen import SignupScreen
    from src.ui.dashboard import Dashboard
    from src.ui.play_quiz import PlayQuizScreen
    from src.ui.main_screen import MainScreen
    from src.ui.admin_login import AdminLogin
    # Import utilitas aplikasi
    from src.utils.config import AppConfig
    from src.utils.assets import AssetManager
    from src.utils.audio_manager import AudioManager
    from src.core.user import User
    from src.core.admin import Admin
    from music_button import MusicButton
except ImportError as e:
    print(f"Error importing modules: {e}")
    traceback.print_exc()
    sys.exit(1)

class MakeaQuizApp:
    def __init__(self):
        try:
            # Inisialisasi konfigurasi dan pengelola aset
            self.user_instance = User(self)
            self.config = AppConfig()
            self.asset_manager = AssetManager()
            self.audio_manager = AudioManager()
            self.window = None
            self.current_frame = None
            self.admin_instance = None
            self.initialize_app()
        except Exception as e:
            print(f"Error initializing application: {e}")
            traceback.print_exc()
            
    def initialize_app(self):
        """Inisialisasi jendela utama aplikasi"""
        try:
            #---Inisialisasi Musik---
            pygame.mixer.init()
            self.audio_manager.play_music(self.config.audio_paths["main_theme"])
            
            # Mengatur tema dan warna aplikasi
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            
            # Membuat jendela utama
            self.window = ctk.CTk()
            self.window.protocol("WM_DELETE_WINDOW", self.on_close)
            self.window.geometry(f"{self.config.width}x{self.config.height}")
            self.window.title(self.config.app_name)
            self.window.resizable(False, False)
            
            # Inisialisasi tombol musik
            self.music_button = MusicButton(self.window, self.audio_manager)
            self.music_button.btn.lift()  # Pastikan tombol di atas widget lain
            
            # Mulai dengan splash screen
            self.show_splash_screen()
            
            # Memulai aplikasi
            self.window.mainloop()
        except Exception as e:
            print(f"Error in initialize_app: {e}")
            traceback.print_exc()

    def on_close(self):
        """Handle application shutdown"""
        # Stop pygame audio
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        
        # Close any matplotlib figures
        import matplotlib.pyplot as plt
        plt.close('all')
        
        # Destroy the window
        self.window.destroy()
        sys.exit(0)



    
    def show_splash_screen(self):
        """Menampilkan splash screen"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
            self.current_frame = SplashScreen(self.window, self.navigate_to_main_screen)
        except Exception as e:
            print(f"Error in show_splash_screen: {e}")
            traceback.print_exc()
    
    def show_main_screen(self):
        """Menampilkan layar utama pemilihan"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
            self.current_frame = MainScreen(
                self.window, 
                admin_callback=self.navigate_to_admin_login,
                user_callback=self.navigate_to_login
            )
            
            self.audio_manager.play_music(self.config.audio_paths["main_theme"])
            # Tambahkan tombol musik di atas frame main
            self.add_music_button(self.current_frame)
        except Exception as e:
            print(f"Error in show_main_screen: {e}")
            traceback.print_exc()

    def show_admin_login(self):
        """Menampilkan layar login admin"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
            self.current_frame = AdminLogin(
                self.window,
                success_callback=self.handle_admin_login,
                back_callback=self.navigate_to_main_screen
            )
            # Tambahkan tombol musik di atas frame main
            self.add_music_button(self.current_frame)
        except Exception as e:
            print(f"Error in show_admin_login: {e}")
            traceback.print_exc()
    
    def show_login_screen(self):
        """Menampilkan layar login"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
                self.current_frame = None

            self.current_frame = LoginScreen(
                self.window,
                self.user_instance,
                login_callback=self.navigate_to_play_quiz,
                signup_callback=self.navigate_to_signup,
                back_callback=self.show_main_screen,
                user_callback=self.navigate_to_login
            )
            self.current_frame.place(x=0, y=0, relwidth=1, relheight=1)
            # Tambahkan tombol musik di atas frame main
            self.add_music_button(self.current_frame)
        except Exception as e:
            print(f"Error in show_login_screen: {e}")
            traceback.print_exc()
            
    def show_signup_screen(self):
        """Menampilkan layar pendaftaran baru"""
        try:
            if self.current_frame:
                self.current_frame.place_forget()
                self.current_frame.destroy()

            self.current_frame = SignupScreen(
                self.window, 
                self.user_instance,
                login_callback=self.show_login_screen
            )
            self.current_frame.place(x=0, y=0, relwidth=1, relheight=1)
            # Tambahkan tombol musik di atas frame main
            self.add_music_button(self.current_frame)
        except Exception as e:
            print(f"Error in show_dashboard: {e}")
            traceback.print_exc()
        
    def show_play_quiz(self):
        """Menampilkan layar bermain quiz"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
            self.current_frame = PlayQuizScreen(
                parent=self.window, 
                app_instance=self,
                back_callback=self.navigate_to_main_screen
            )
            self.audio_manager.play_music(self.config.audio_paths["quiz_theme"])
            # Tambahkan tombol musik di atas frame main
            self.add_music_button(self.current_frame)
        except Exception as e:
            print(f"Error in show_play_quiz: {e}")
            traceback.print_exc()
    
    def handle_user_logout(self):
         """Menangani proses logout pengguna."""
         print("[Main.py] User logout...")
         if self.user_instance:
              self.user_instance.logout()

    # Fungsi navigasi antar layar
    def navigate_to_main_screen(self, from_logout=False):
        if self.admin_instance:
             if hasattr(self.admin_instance, 'dashboard_instance') and self.admin_instance.dashboard_instance:
                  self.admin_instance.back_to_main()
             self.admin_instance = None
        
        if not from_logout and self.user_instance and self.get_current_logged_in_user():
            self.handle_user_logout()
            self.show_main_screen()
        else:
            if self.current_frame and self.current_frame.winfo_exists():
                 print(f"[Main.py] Destroying current frame before showing main screen: {type(self.current_frame)}")
                 self.current_frame.destroy()
                 self.current_frame = None
            self.show_main_screen()
    
    def navigate_to_login(self):
        """Navigasi ke layar login pengguna"""
        self.show_login_screen()
        
    def navigate_to_signup(self):
        """Navigasi ke layar pendaftaran"""
        self.show_signup_screen()
        
    def navigate_to_play_quiz(self):
        """Navigasi ke layar bermain quiz"""
        self.show_play_quiz()

    def handle_admin_login(self):
        """Dipanggil setelah login admin berhasil."""
        print("[Main.py] Login admin berhasil, memanggil Admin.open_dashboard")
        try:
            if self.current_frame:
                self.current_frame.destroy()
                self.current_frame = None
            
            if not self.admin_instance:
                 self.admin_instance = Admin(
                    app=self, 
                    show_login_callback=self.navigate_to_admin_login
                 )
            
            self.admin_instance.open_dashboard()
            
            if hasattr(self.admin_instance, 'dashboard_instance'):
                 self.current_frame = self.admin_instance.dashboard_instance

        except Exception as e:
            print(f"Error handling admin login: {e}")
            traceback.print_exc()
            self.show_admin_login() 

    # --- Metode Helper untuk User --- 
    def get_current_logged_in_user(self):
         """Mendapatkan username pengguna yang sedang login."""
         if self.user_instance:
              return self.user_instance.get_current_user()
         return None

    def navigate_to_admin_login(self):
        """Navigasi ke layar login admin"""
        self.show_admin_login()

    def add_music_button(self, parent):
        # Hapus tombol sebelumnya jika ada
        if hasattr(self, 'music_button') and self.music_button:
            self.music_button.btn.destroy()
        self.music_button = MusicButton(parent, self.audio_manager)
        self.music_button.btn.lift()

if __name__ == "__main__":
    try:
        # Mulai aplikasi
        app = MakeaQuizApp()
    except Exception as e:
        print(f"Error starting application: {e}")
        traceback.print_exc()
        sys.exit(1)
