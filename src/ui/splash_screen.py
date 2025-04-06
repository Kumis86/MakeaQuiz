# src/gui/splash_screen.py
import customtkinter as ctk
import time
import threading
from src.utils.assets import AssetManager
from PIL import Image

class SplashScreen(ctk.CTkFrame):
    """Layar pembuka aplikasi dengan animasi loading"""
    def __init__(self, parent, next_callback):
        super().__init__(parent, corner_radius=0, width=1260, height=716)
        self.parent = parent
        self.next_callback = next_callback
        self.asset_manager = AssetManager()
        
        # Variabel untuk animasi
        self.animation_active = True
        self.progress_value = 0
        self.loading_text_idx = 0
        self.loading_texts = ["Loading", "Loading.", "Loading..", "Loading..."]
        
        # Konfigurasi frame utama
        self.configure(fg_color="#000000")
        self.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Membuat elemen-elemen UI
        self._create_ui()
        
        # Memulai animasi loading
        self._start_animation()
        
        # Secara otomatis pindah ke layar berikutnya setelah 5 detik
        self.after(5000, self._complete_loading)
        
    def _create_ui(self):
        """Membuat elemen-elemen antarmuka pengguna"""
        # Mengatur latar belakang UI menjadi hitam
        self.configure(fg_color="#000000")
        
        # Frame tengah untuk judul, gambar dan elemen animasi
        center_frame = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0, width=1260, height=716)
        center_frame.place(x=0, y=0)
        
        # Memuat gambar Pacman
        try:
            image_path = self.asset_manager.get_asset_path("images/pacman.jpg")
            original_image = Image.open(image_path)
            
            # Membuat CTkImage dengan ukuran yang sesuai
            bg_image = ctk.CTkImage(
                light_image=original_image,
                dark_image=original_image,
                size=(640, 716)  # Ukuran disesuaikan untuk tampilan yang lebih baik
            )
            
            # Membuat label gambar yang berada di tengah
            image_label = ctk.CTkLabel(
                center_frame,
                image=bg_image,
                text="",
                fg_color="#000000"
            )
            image_label.place(x=0, y=0)
            
        except Exception as e:
            print(f"Error loading image: {e}")

        # Memuat gambar judul sebagai pengganti teks
        try:
            title_path = self.asset_manager.get_asset_path("images/title.png")
            title_image = Image.open(title_path)
            
            # Membuat CTkImage untuk judul
            self.title_ctk_image = ctk.CTkImage(
                light_image=title_image,
                dark_image=title_image,
                size=(600, 120)  # Sesuaikan ukuran yang dibutuhkan
            )
            
            # Membuat label untuk gambar judul dengan latar belakang transparan
            self.title_label = ctk.CTkLabel(
                center_frame,
                image=self.title_ctk_image,
                text="",
                fg_color="transparent"
            )
            self.title_label.place(relx=0.5, rely=0.25, anchor="center")
            
        except Exception as e:
            print(f"Error loading title image: {e}")
            # Menggunakan teks jika gambar gagal dimuat
            self.title_label = ctk.CTkLabel(
                center_frame, 
                text="MakeaQuiz", 
                font=("Inter ExtraBoldItalic", 128), 
                text_color="#FFFFFF"
            )
            self.title_label.place(relx=0.5, rely=0.25, anchor="center")
        
        # Subtitle dengan animasi
        self.subtitle_label = ctk.CTkLabel(
            center_frame, 
            text="Create and Play Interactive Quizzes", 
            font=("Inter Light", 24), 
            text_color="#DDDDDD"
        )
        self.subtitle_label.place(relx=0.5, rely=0.75, anchor="center")
        
        # Teks loading dengan animasi
        self.loading_label = ctk.CTkLabel(
            center_frame, 
            text="Loading...", 
            font=("Inter", 18), 
            text_color="#DDDDDD"
        )
        self.loading_label.place(relx=0.5, rely=0.82, anchor="center")
        
        # Progress bar untuk animasi loading
        self.progress_bar = ctk.CTkProgressBar(
            center_frame,
            width=400,
            height=15,
            corner_radius=5,
            mode="determinate"
        )
        self.progress_bar.place(relx=0.5, rely=0.87, anchor="center")
        self.progress_bar.set(0)
        
        # Informasi versi aplikasi
        version_label = ctk.CTkLabel(
            center_frame, 
            text="v2.0.0", 
            font=("Inter Light", 12), 
            text_color="#888888"
        )
        version_label.place(relx=0.9, rely=0.95, anchor="center")
    
    def _start_animation(self):
        """Memulai animasi loading dalam thread terpisah"""
        self.animation_thread = threading.Thread(target=self._run_animation)
        self.animation_thread.daemon = True
        self.animation_thread.start()
    
    def _run_animation(self):
        """Menjalankan animasi loading"""
        while self.animation_active and self.progress_value < 1:
            # Memperbarui progress bar
            self.progress_value += 0.02
            if self.progress_value > 1:
                self.progress_value = 1
                
            # Memperbarui teks loading
            self.loading_text_idx = (self.loading_text_idx + 1) % len(self.loading_texts)
            
            # Memperbarui elemen UI
            self.after(0, self._update_ui)
            
            # Jeda untuk animasi
            time.sleep(0.1)
    
    def _update_ui(self):
        """Memperbarui elemen UI dengan animasi"""
        # Memperbarui progress bar
        self.progress_bar.set(self.progress_value)
        
        # Memperbarui teks loading
        self.loading_label.configure(text=self.loading_texts[self.loading_text_idx])
        
        # Animasi judul (efek skala halus)
        if hasattr(self, 'title_ctk_image'):
            # Untuk judul gambar, sedikit mengubah ukuran
            scale = 1 + 0.02 * (0.5 - abs(0.5 - (self.progress_value % 1)))
            new_size = (int(600 * scale), int(120 * scale))
            self.title_ctk_image.configure(size=new_size)
        else:
            # Untuk judul teks, mengubah ukuran font
            scale = 1 + 0.02 * (0.5 - abs(0.5 - (self.progress_value % 1)))
            self.title_label.configure(font=("Inter ExtraBoldItalic", int(128 * scale)))
    
    def _complete_loading(self):
        """Menyelesaikan animasi loading dan berpindah ke layar berikutnya"""
        self.animation_active = False
        self.progress_bar.set(1)
        self.loading_label.configure(text="Complete!")
        self.after(500, self.next_callback)
