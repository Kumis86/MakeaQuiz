# app/gui/signup_screen.py
import customtkinter as ctk
from src.utils.assets import AssetManager
from PIL import Image
from src.utils.verifikasi import send_otp
from tkinter import messagebox

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

        email_label = ctk.CTkLabel(self, text="Email", font=("Inter", 16), text_color="#FFFFFF")
        email_label.place(relx=0.75, rely=0.41, anchor="center")

        self.email_entry = ctk.CTkEntry(self, width=371, height=47, font=("Inter", 14), fg_color="#333333", border_color="#444444", text_color="white", corner_radius=5)
        self.email_entry.place(relx=0.75, rely=0.48, anchor="center")

        password_label = ctk.CTkLabel(self, text="Password", font=("Inter", 16), text_color="#FFFFFF")
        password_label.place(relx=0.75, rely=0.54, anchor="center")
        
        self.password_entry = ctk.CTkEntry(self, width=371, height=47, font=("Inter", 14), fg_color="#333333", border_color="#444444", text_color="white", corner_radius=5, show="•")
        self.password_entry.place(relx=0.75, rely=0.61, anchor="center")
        
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
        self.toggle_button.place(relx=0.88, rely=0.61, anchor="center")  # Letakkan tombol di samping password_entry

        register_button = ctk.CTkButton(
            self, 
            text="Register", 
            font=("Inter Bold", 16), 
            width=180,
            height=46, 
            corner_radius=5, 
            fg_color="#E6B36A", 
            hover_color="#4F44A3", 
            command=self.on_register
        )
        register_button.place(relx=0.75, rely=0.76, anchor="center")

        # Back button
        back_button = ctk.CTkButton(
            self,
            text="Back",
            font=("Inter Bold", 16),
            width=180,
            height=46,
            corner_radius=5,
            fg_color="#333333",
            hover_color="#444444",
            command=self.login_callback
        )
        back_button.place(relx=0.75, rely=0.86, anchor="center")
    
    def toggle_password(self):
        """Fungsi untuk menampilkan atau menyembunyikan password."""
        self.show_password = not self.show_password
        self.password_entry.configure(show="" if self.show_password else "•")

    def open_otp(self, expected_otp, on_success):
        """Membuka popup untuk input OTP."""
        print("Opening OTP popup...")

        validasi_otp_window = ctk.CTkToplevel(self)
        validasi_otp_window.title("Verifikasi OTP")
        validasi_otp_window.geometry("450x300")
        validasi_otp_window.resizable(False, False)
        validasi_otp_window.transient(self.parent)
        validasi_otp_window.grab_set()

        main_frame = ctk.CTkFrame(validasi_otp_window, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        title_label = ctk.CTkLabel(main_frame, text="Verifikasi OTP", font=("Inter Bold", 20))
        title_label.pack(pady=(0, 20))

        otp_label = ctk.CTkLabel(main_frame, text="Masukkan OTP:", font=("Inter", 14))
        otp_label.pack(anchor="w", padx=10)

        otp_entry = ctk.CTkEntry(main_frame, width=380, height=40)
        otp_entry.pack(pady=(0, 15), fill="x", padx=10)

        def validate_otp():
            user_otp = otp_entry.get().strip()
            if user_otp == expected_otp:
                messagebox.showinfo("Sukses", "OTP sesuai. Proses dilanjutkan.")
                validasi_otp_window.destroy()
                on_success()
            else:
                messagebox.showerror("OTP Salah", "Kode OTP tidak cocok. Silakan coba lagi.")

        verif_button = ctk.CTkButton(
            main_frame,
            text="Verifikasi",
            command=validate_otp,
            font=("Inter Bold", 14),
            fg_color="#E6B36A",
            hover_color="#4F44A3"
        )
        verif_button.pack(pady=10)

    def on_register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()

        if not username or not password or not email:
            messagebox.showerror("Registrasi Gagal", "Semua field harus diisi.")
            return

        if "@" not in email or "." not in email:
            messagebox.showerror("Email Tidak Valid", "Masukkan email yang valid.")
            return

        if self.user_instance._check_username_exists(username):
            messagebox.showerror("Registrasi Gagal", f"Username '{username}' sudah digunakan.")
            return

        if self.user_instance._check_email_exists(email):
            messagebox.showerror("Registrasi Gagal", f"Email '{email}' sudah digunakan.")
            return

        is_valid, message = self.user_instance.is_valid_password(password)
        if not is_valid:
            messagebox.showerror("Registrasi Gagal", message)
            return

        otp = send_otp(email, username)
        if not otp:
            messagebox.showerror("OTP Gagal", "Batas OTP tercapai. Coba lagi dalam 5 menit.")
            return

        def lanjutkan_registrasi():
            success = self.user_instance.register(username, password, email)
            if success:
                messagebox.showinfo("Registrasi Berhasil", f"Akun untuk '{username}' berhasil dibuat. Silakan login.")
                self.login_callback()

        # Panggil OTP popup
        self.open_otp(expected_otp=otp, on_success=lanjutkan_registrasi)
        messagebox.showinfo("Berhasil", f"Kode OTP berhasil dikirimkan ke akun email anda! Jika tidak ada, cek di bagian Spam")