# app/gui/signup_screen.py
import customtkinter as ctk
from src.utils.assets import AssetManager
from PIL import Image

class SignupScreen(ctk.CTkFrame):
    """Signup screen for the application"""
    def __init__(self, parent, user_instance, login_callback):
        super().__init__(parent, corner_radius=0, width=1260, height=716)
        self.parent = parent
        self.user_instance = user_instance
        self.login_callback = login_callback
        self.asset_manager = AssetManager()
        self.show_password = False
        
        self.configure(fg_color="#000000")
        self.place(x=0, y=0, relwidth=1, relheight=1)
        
        self._create_ui()
        
    def _create_ui(self):
        self.configure(fg_color="#000000")
        
        try:
            image_path = self.asset_manager.get_asset_path("images/pacman.jpg")
            original_image = Image.open(image_path)
            
            bg_image = ctk.CTkImage(
                light_image=original_image,
                dark_image=original_image,
                size=(600, 716)
            )
            
            image_label = ctk.CTkLabel(
                self,
                image=bg_image,
                text="",
                fg_color="#000000"
            )
            image_label.place(x=0, y=0)
        except Exception as e:
            print(f"Error loading image: {e}")
            left_panel = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0, width=600, height=716)
            left_panel.place(x=0, y=0)
        
        title = ctk.CTkLabel(self, text="MakeaQuiz", font=("Inter ExtraBoldItalic", 48), text_color="#FFFFFF")
        title.place(relx=0.75, rely=0.15, anchor="center")

        subtitle = ctk.CTkLabel(
            self, 
            text="Enter username and password to play quiz", 
            font=("Inter", 16), 
            text_color="#BBBBBB"
        )
        subtitle.place(relx=0.75, rely=0.22, anchor="center")
        
        username_label = ctk.CTkLabel(self, text="Username", font=("Inter", 16), text_color="#FFFFFF")
        username_label.place(relx=0.75, rely=0.28, anchor="center")
        
        self.username_entry = ctk.CTkEntry(self, width=371, height=47, font=("Inter", 14), fg_color="#333333", border_color="#444444", text_color="white", corner_radius=5)
        self.username_entry.place(relx=0.75, rely=0.35, anchor="center")
        
        password_label = ctk.CTkLabel(self, text="Password", font=("Inter", 16), text_color="#FFFFFF")
        password_label.place(relx=0.75, rely=0.48, anchor="center")
        
        self.password_entry = ctk.CTkEntry(self, width=371, height=47, font=("Inter", 14), fg_color="#333333", border_color="#444444", text_color="white", corner_radius=5, show="•")
        self.password_entry.place(relx=0.75, rely=0.55, anchor="center")
        
        self.toggle_button = ctk.CTkButton(
            self,
            text="👁",
            width=40,
            height=47,
            font=("Inter", 14),
            fg_color="#444444",
            hover_color="#555555",
            command=self.toggle_password
        )
        self.toggle_button.place(relx=0.88, rely=0.55, anchor="center")  # Letakkan tombol di samping password_entry

        register_button = ctk.CTkButton(self, text="Register", font=("Inter Bold", 16), width=160, height=46, corner_radius=5, fg_color="#6357B1", hover_color="#4F44A3", command=self.on_register)
        register_button.place(relx=0.75, rely=0.7, anchor="center")

        # Back button
        back_button = ctk.CTkButton(
            self,
            text="Back",
            font=("Inter Bold", 16),
            width=160,
            height=46,
            corner_radius=5,
            fg_color="#333333",
            hover_color="#444444",
            command=self.login_callback
        )
        back_button.place(relx=0.75, rely=0.8, anchor="center")
    
    def toggle_password(self):
        """Fungsi untuk menampilkan atau menyembunyikan password."""
        self.show_password = not self.show_password
        self.password_entry.configure(show="" if self.show_password else "•")

    def on_register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.user_instance.register(username, password)
        self.login_callback()