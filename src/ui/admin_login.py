# src/gui/admin_login.py
import customtkinter as ctk
from src.utils.assets import AssetManager
from PIL import Image
import tkinter.messagebox as messagebox

class AdminLogin(ctk.CTkFrame):
    """Admin login screen requiring password"""
    def __init__(self, parent, success_callback, back_callback):
        super().__init__(parent, corner_radius=0, width=1260, height=716)
        self.parent = parent
        self.success_callback = success_callback
        self.back_callback = back_callback
        self.asset_manager = AssetManager()
        
        # Set admin password
        self.admin_password = "admin123"  # In a real application, this would be securely stored
        
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
                size=(561, 716)  # Full height and appropriate width
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
            text="Admin Login", 
            font=("Inter ExtraBoldItalic", 48), 
            text_color="#FFFFFF"
        )
        title.place(relx=0.75, rely=0.15, anchor="center")
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            self, 
            text="Enter admin password to continue", 
            font=("Inter", 16), 
            text_color="#BBBBBB"
        )
        subtitle.place(relx=0.75, rely=0.22, anchor="center")
        
        # Password
        password_label = ctk.CTkLabel(
            self, 
            text="Password", 
            font=("Inter", 16), 
            text_color="#FFFFFF"
        )
        password_label.place(relx=0.75, rely=0.35, anchor="center")
        
        self.password_entry = ctk.CTkEntry(
            self,
            width=371,
            height=47,
            font=("Inter", 14),
            fg_color="#333333",
            border_color="#444444",
            text_color="white",
            corner_radius=5,
            show="•"
        )
        self.password_entry.place(relx=0.75, rely=0.42, anchor="center")
        
        # Login button
        login_button = ctk.CTkButton(
            self,
            text="Login",
            font=("Inter Bold", 16),
            width=160,
            height=46,
            corner_radius=5,
            fg_color="#E6B36A",  
            hover_color="#C99A4B",
            text_color="#000000",
            command=self._verify_password
        )
        login_button.place(relx=0.75, rely=0.55, anchor="center")
        
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
            command=self.back_callback
        )
        back_button.place(relx=0.75, rely=0.65, anchor="center")
    
    def _verify_password(self):
        """Verify the entered password"""
        entered_password = self.password_entry.get()
        
        if entered_password == self.admin_password:
            # Password correct, proceed to dashboard
            self.success_callback()
        else:
            # Password incorrect, show error message
            messagebox.showerror("Access Denied", "Incorrect admin password. Please try again.") 
