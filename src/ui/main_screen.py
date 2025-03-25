import customtkinter as ctk
from src.utils.assets import AssetManager
from PIL import Image

class MainScreen(ctk.CTkFrame):
    """Main menu screen with Admin and User options"""
    def __init__(self, parent, admin_callback, user_callback):
        super().__init__(parent, corner_radius=0, width=1260, height=716)
        self.parent = parent
        self.admin_callback = admin_callback
        self.user_callback = user_callback
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
        
        # Center frame for title and buttons
        center_frame = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0, width=1260, height=716)
        center_frame.place(x=0, y=0)
        
        # Load Pacman image
        try:
            image_path = self.asset_manager.get_asset_path("images/pacman.jpg")
            original_image = Image.open(image_path)
            
            # Create CTkImage with appropriate size
            bg_image = ctk.CTkImage(
                light_image=original_image,
                dark_image=original_image,
                size=(640, 716)  # Adjusted size for better display
            )
            
            # Create image label centered
            image_label = ctk.CTkLabel(
                center_frame,
                image=bg_image,
                text="",
                fg_color="#000000"
            )
            image_label.place(x=0, y=0)
            
        except Exception as e:
            print(f"Error loading image: {e}")
            
        # Load title image instead of text
        try:
            title_path = self.asset_manager.get_asset_path("images/title.png")
            title_image = Image.open(title_path)
            
            # Create CTkImage for title
            title_ctk_image = ctk.CTkImage(
                light_image=title_image,
                dark_image=title_image,
                size=(600, 120)  # Adjust size as needed
            )
            
            # Create label for title image - transparent background
            title_label = ctk.CTkLabel(
                center_frame,
                image=title_ctk_image,
                text="",
                fg_color="transparent"
            )
            title_label.place(relx=0.5, rely=0.25, anchor="center")
            
        except Exception as e:
            print(f"Error loading title image: {e}")
            # Fallback to text if image fails to load
            title = ctk.CTkLabel(
                center_frame, 
                text="MakeaQuiz", 
                font=("Inter ExtraBoldItalic", 128), 
                text_color="#FFFFFF"
            )
            title.place(relx=0.5, rely=0.25, anchor="center")
        
        # Create a buttons frame to hold both buttons side by side
        buttons_frame = ctk.CTkFrame(center_frame, fg_color="transparent", corner_radius=0)
        buttons_frame.place(relx=0.5, rely=0.85, anchor="center")
        
        # Admin button - placed on left side of buttons frame
        admin_button = ctk.CTkButton(
            buttons_frame,
            text="Admin",
            font=("Inter Bold", 16),
            width=150,
            height=46,
            corner_radius=20,
            fg_color="#111111",  # Dark background
            hover_color="#222222",
            border_width=1,
            border_color="#FFFFFF",
            command=self.admin_callback
        )
        admin_button.pack(side="left", padx=20)
        
        # User button - placed on right side of buttons frame
        user_button = ctk.CTkButton(
            buttons_frame,
            text="User",
            font=("Inter Bold", 16),
            width=150,
            height=46,
            corner_radius=20,
            fg_color="#333333",  # Dark gray background
            hover_color="#444444",
            command=self.user_callback
        )
        user_button.pack(side="left", padx=20)
