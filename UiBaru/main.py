# main.py - Entry point utama aplikasi MakeaQuiz
import customtkinter as ctk
import traceback
import sys

try:
    # Import komponen-komponen UI
    from app.gui.splash_screen import SplashScreen
    from app.gui.login_screen import LoginScreen
    from app.gui.signup_screen import SignupScreen
    from app.gui.dashboard import Dashboard
    from app.gui.play_quiz import PlayQuizScreen
    from app.gui.main_screen import MainScreen
    from app.gui.admin_login import AdminLogin
    # Import utilitas aplikasi
    from app.utils.config import AppConfig
    from app.utils.assets import AssetManager
except ImportError as e:
    print(f"Error importing modules: {e}")
    traceback.print_exc()
    sys.exit(1)

class MakeaQuizApp:
    def __init__(self):
        try:
            # Inisialisasi konfigurasi dan pengelola aset
            self.config = AppConfig()
            self.asset_manager = AssetManager()
            self.window = None
            self.current_frame = None
            self.initialize_app()
        except Exception as e:
            print(f"Error initializing application: {e}")
            traceback.print_exc()
            
    def initialize_app(self):
        """Inisialisasi jendela utama aplikasi"""
        try:
            # Mengatur tema dan warna aplikasi
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            
            # Membuat jendela utama
            self.window = ctk.CTk()
            self.window.geometry(f"{self.config.width}x{self.config.height}")
            self.window.title(self.config.app_name)
            self.window.resizable(False, False)
            
            # Mulai dengan splash screen
            self.show_splash_screen()
            
            # Memulai aplikasi
            self.window.mainloop()
        except Exception as e:
            print(f"Error in initialize_app: {e}")
            traceback.print_exc()
    
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
                dashboard_callback=self.navigate_to_dashboard,
                back_callback=self.navigate_to_main_screen
            )
        except Exception as e:
            print(f"Error in show_admin_login: {e}")
            traceback.print_exc()
        
    def show_login_screen(self):
        """Menampilkan layar login pengguna"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
            self.current_frame = LoginScreen(
                self.window, 
                login_callback=self.navigate_to_play_quiz, 
                signup_callback=self.navigate_to_signup
            )
        except Exception as e:
            print(f"Error in show_login_screen: {e}")
            traceback.print_exc()
        
    def show_signup_screen(self):
        """Menampilkan layar pendaftaran baru"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
            self.current_frame = SignupScreen(
                self.window, 
                login_callback=self.navigate_to_login
            )
        except Exception as e:
            print(f"Error in show_signup_screen: {e}")
            traceback.print_exc()
        
    def show_dashboard(self):
        """Menampilkan dashboard admin"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
            self.current_frame = Dashboard(
                self.window, 
                logout_callback=self.navigate_to_main_screen,
                play_quiz_callback=self.navigate_to_play_quiz
            )
        except Exception as e:
            print(f"Error in show_dashboard: {e}")
            traceback.print_exc()
    
    def show_play_quiz(self):
        """Menampilkan layar bermain quiz"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
            self.current_frame = PlayQuizScreen(
                self.window, 
                back_callback=self.navigate_to_main_screen
            )
        except Exception as e:
            print(f"Error in show_play_quiz: {e}")
            traceback.print_exc()
    
    # Fungsi navigasi antar layar
    def navigate_to_main_screen(self):
        """Navigasi ke layar utama"""
        self.show_main_screen()
    
    def navigate_to_admin_login(self):
        """Navigasi ke layar login admin"""
        self.show_admin_login()
    
    def navigate_to_login(self):
        """Navigasi ke layar login pengguna"""
        self.show_login_screen()
        
    def navigate_to_signup(self):
        """Navigasi ke layar pendaftaran"""
        self.show_signup_screen()
        
    def navigate_to_dashboard(self):
        """Navigasi ke dashboard admin"""
        self.show_dashboard()
        
    def navigate_to_play_quiz(self):
        """Navigasi ke layar bermain quiz"""
        self.show_play_quiz()

if __name__ == "__main__":
    try:
        # Mulai aplikasi
        app = MakeaQuizApp()
    except Exception as e:
        print(f"Error starting application: {e}")
        traceback.print_exc()
        sys.exit(1)