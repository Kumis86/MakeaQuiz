import os
from pathlib import Path

class AssetManager:
    """Pengelola aset untuk aplikasi"""
    def __init__(self):
        # Menentukan path direktori aplikasi
        self.app_path = Path(__file__).parent.parent.parent
        self.assets_path = self.app_path / "assets"
        
        # Membuat direktori assets jika belum ada
        os.makedirs(self.assets_path, exist_ok=True)
        
    def get_asset_path(self, filename):
        """Mendapatkan path untuk file aset tertentu"""
        return self.assets_path / filename
        
    def load_image(self, filename):
        """Memuat gambar dari folder aset"""
        from customtkinter import CTkImage
        from PIL import Image
        
        # Mendapatkan path lengkap file
        image_path = self.get_asset_path(filename)
        if not image_path.exists():
            print(f"Peringatan: File gambar '{filename}' tidak ditemukan di {image_path}")
            return None
            
        # Mengembalikan objek CTkImage yang dapat digunakan di CustomTkinter
        return CTkImage(light_image=Image.open(image_path), 
                        dark_image=Image.open(image_path)) 