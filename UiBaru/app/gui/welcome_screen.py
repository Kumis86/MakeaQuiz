# app/gui/welcome_screen.py
import customtkinter as ctk
from app.utils.assets import AssetManager
from PIL import Image

class WelcomeScreen(ctk.CTkFrame):
    """Welcome screen for the application"""
    def __init__(self, parent, login_callback, signup_callback):
        super().__init__(parent, corner_radius=0, width=1260, height=716)
        self.parent = parent
        self.login_callback = login_callback
        self.signup_callback = signup_callback
        self.asset_manager = AssetManager()
        
        # Configure the frame
        self.configure(fg_color="#000000")
        self.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create UI elements
        self._create_ui()
        
    def _create_ui(self):
        """Create the UI elements"""
        # Set the entire UI background to black
        self.configure(fg_color="#000000")
        
        # Load background image directly via PIL for better control
        try:
            image_path = self.asset_manager.get_asset_path("images/pacman.jpg")
            original_image = Image.open(image_path)
            
            # Create CTkImage with appropriate size to fill the left side
            bg_image = ctk.CTkImage(
                light_image=original_image,
                dark_image=original_image,
                size=(600, 716)  # Full height and appropriate width
            )
            
            # Create image label directly on the main frame
            image_label = ctk.CTkLabel(
                self,
                image=bg_image,
                text="",
                fg_color="#000000"
            )
            image_label.place(x=0, y=0)
            
        except Exception as e:
            print(f"Error loading image: {e}")
            # Fallback if image doesn't load
            left_panel = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0, width=600, height=716)
            left_panel.place(x=0, y=0)
        
        # Right side content
        # Title text
        title = ctk.CTkLabel(
            self, 
            text="MakeaQuiz", 
            font=("Inter ExtraBoldItalic", 72), 
            text_color="#FFFFFF"
        )
        title.place(relx=0.75, rely=0.3, anchor="center")
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            self, 
            text="Create and Play Interactive Quizzes", 
            font=("Inter Light", 16), 
            text_color="#BBBBBB"
        )
        subtitle.place(relx=0.75, rely=0.38, anchor="center")
        
        # Login button
        login_button = ctk.CTkButton(
            self,
            text="Login",
            font=("Inter Bold", 18),
            width=180,
            height=60,
            corner_radius=5,
            fg_color="#6357B1",  # Purple color
            hover_color="#4F44A3",
            command=self.login_callback
        )
        login_button.place(relx=0.68, rely=0.55, anchor="center")
        
        # Sign up button
        signup_button = ctk.CTkButton(
            self,
            text="Sign Up",
            font=("Inter Bold", 18),
            width=180,
            height=60,
            corner_radius=5,
            fg_color="#6357B1",  # Purple color
            hover_color="#4F44A3",
            command=self.signup_callback
        )
        signup_button.place(relx=0.82, rely=0.55, anchor="center")