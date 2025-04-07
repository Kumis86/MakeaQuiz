# main.py - Entry point utama aplikasi MakeaQuiz
import customtkinter as ctk
import traceback
import sys
import tkinter.messagebox as messagebox

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
    from src.core.user import User
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
            # Mengatur tema dan warna aplikasi
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            
            # Membuat jendela utama
            self.window = ctk.CTk()
            self.window.geometry(f"{self.config.width}x{self.config.height}")
            self.window.title(self.config.app_name)
            self.window.resizable(False, False)
            self.window.configure(fg_color="#3B2869")  # Warna background utama (ungu gelap)
            
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
        """Menampilkan layar login"""
        try:
            if self.current_frame:
                self.current_frame.place_forget()
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
        except Exception as e:
            print(f"Error in show_dashboard: {e}")
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
        except Exception as e:
            print(f"Error in show_dashboard: {e}")
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
                app_instance=self,
                back_callback=self.navigate_to_main_screen
            )
        except Exception as e:
            print(f"Error in show_play_quiz: {e}")
            traceback.print_exc()

    def get_current_logged_in_user(self):
        """Mendapatkan username pengguna yang sedang login."""
        if self.user_instance:
            return self.user_instance.get_current_user()
        return None

    def handle_admin_login(self, admin_instance):
        """Menangani proses login admin."""
        print("[Main.py] Admin login successful...")
        self.admin_instance = admin_instance
        self.navigate_to_dashboard()

    def handle_user_logout(self):
        """Menangani proses logout pengguna."""
        print("[Main.py] User logout...")
        if self.user_instance:
            self.user_instance.logout()
    
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

    def _create_ui(self):
        # ... (existing code)
        self.start_quiz_button = ctk.CTkButton(
            # ...
            fg_color="#3B82C4",  # Warna biru yang kontras
            hover_color="#4F4698",  # Hover ke warna ungu
        )
        # ... (rest of the existing code)

    def _load_slides(self):
        cover_frame = ctk.CTkFrame(self.slider_frame, fg_color="#4F4698", width=780, height=380)

        title_label = ctk.CTkLabel(
            # ...
            text_color="#CFFBF6"  # Warna teks yang kontras (cyan terang)
        )

        desc_label = ctk.CTkLabel(
            # ...
            text_color="#ABBBE5",  # Warna teks yang lebih lembut
        )

if __name__ == "__main__":
    try:
        # Mulai aplikasi
        app = MakeaQuizApp()
    except Exception as e:
        print(f"Error starting application: {e}")
        traceback.print_exc()
        sys.exit(1)
