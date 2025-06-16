import customtkinter as ctk
from src.utils.assets import AssetManager
from src.ui.Play_Music_Button import PlayMusicButton
from PIL import Image

class MainScreen(ctk.CTkFrame):
    """Main menu screen with Admin and User options"""
    def __init__(self, parent, admin_callback, user_callback, audio_manager):
        super().__init__(parent, corner_radius=0, width=1260, height=716)
        self.parent = parent
        self.admin_callback = admin_callback
        self.user_callback = user_callback
        self.audio_manager = audio_manager
        self.asset_manager = AssetManager()
        
        # Configure the frame
        self.configure(fg_color="#000000")
        self.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create UI elements
        self._create_ui()
        
    def _create_ui(self):
        """Create the UI elements"""
        self.configure(fg_color="#000000")

        # --- LEFT SIDE  ---
        left_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0, width=600, height=716)
        left_frame.place(x=0, y=0)

        # Slogan image 
        try:
            slogan_path = self.asset_manager.get_asset_path("images/slogan.png")
            slogan_img = Image.open(slogan_path)
            slogan_ctk_img = ctk.CTkImage(
                light_image=slogan_img,
                dark_image=slogan_img,
                size=(466, 220)
            )
            slogan_label = ctk.CTkLabel(left_frame, image=slogan_ctk_img, text="", fg_color="transparent")
            slogan_label.place(x=100, y=120)
        except Exception as e:
            print(f"Error loading slogan image: {e}")

        # Buttons frame 
        buttons_frame = ctk.CTkFrame(left_frame, fg_color="transparent", corner_radius=0)
        buttons_frame.place(x=152, y=495)

        # Admin button 
        admin_button = ctk.CTkButton(
            buttons_frame,
            text="Admin",
            font=("Inter Bold", 20),
            width=140,
            height=50,
            corner_radius=25,
            fg_color="#E6B36A",
            hover_color="#C99A4B",
            text_color="#000000",
            command=self.admin_callback
        )
        admin_button.pack(side="left", padx=18)

        # User button
        user_button = ctk.CTkButton(
            buttons_frame,
            text="User",
            font=("Inter Bold", 20),
            width=140,
            height=50,
            corner_radius=25,
            fg_color="#222222",
            hover_color="#444444",
            text_color="#FFFFFF",
            command=self.user_callback
        )
        user_button.pack(side="left", padx=18)

        # --- RIGHT SIDE (Logo) ---
        right_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0, width=680, height=716)
        right_frame.place(x=630, y=30)

        try:
            logo_path = self.asset_manager.get_asset_path("images/logo.png")
            logo_img = Image.open(logo_path)

            logo_ctk_img = ctk.CTkImage(
                light_image=logo_img,
                dark_image=logo_img,
                size=(677, 543)
            )

            shadow1 = ctk.CTkLabel(right_frame, text="", fg_color="#222222", width=480, height=480, corner_radius=240)
            shadow1.place(relx=0.5, rely=0.5, anchor="center")
            shadow2 = ctk.CTkLabel(right_frame, text="", fg_color="#181818", width=420, height=420, corner_radius=210)
            shadow2.place(relx=0.54, rely=0.54, anchor="center")
            # Logo utama
            logo_label = ctk.CTkLabel(right_frame, image=logo_ctk_img, text="", fg_color="transparent", width=400, height=400)
            logo_label.place(relx=0.52, rely=0.52, anchor="center")
        except Exception as e:
            print(f"Error loading logo image: {e}")
            # penanganan jika gagal
            logo_placeholder = ctk.CTkLabel(right_frame, text="LOGO", fg_color="#444444", text_color="#E6B36A", font=("Inter Bold", 32), width=340, height=340, corner_radius=170)
            logo_placeholder.place(relx=0.52, rely=0.52, anchor="center")

        self.play_music_btn = PlayMusicButton(
            self,
            audio_manager=self.audio_manager,
            music_path=self.asset_manager.get_asset_path("audio/main_theme.mp3")
        )
        #self.play_music_btn.place(x=1100, y=20, width=120, height=40)