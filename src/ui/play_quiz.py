# src/gui/play_quiz.py
import customtkinter as ctk
from PIL import Image
from src.utils.assets import AssetManager

class PlayQuizScreen(ctk.CTkFrame):
    """Play Quiz screen for the application"""
    def __init__(self, parent, back_callback):
        super().__init__(parent, corner_radius=0, width=1260, height=716)
        self.parent = parent
        self.back_callback = back_callback
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
        
        # Center frame for title, image and button
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
        
        # Start Quiz button - placed in the center of the screen
        start_quiz_button = ctk.CTkButton(
            center_frame,
            text="Start Quiz",
            font=("Inter Bold", 18),
            width=200,
            height=50,
            corner_radius=20,
            fg_color="#6357B1",  # Purple color from image
            hover_color="#4F44A3",
            command=self._start_quiz
        )
        start_quiz_button.place(relx=0.5, rely=0.85, anchor="center")
    
    def _start_quiz(self):
        """Start a quiz"""
        print("Starting quiz")
        # Here you would implement the logic to start a quiz 
        # For now, just go back
        self.back_callback() 
