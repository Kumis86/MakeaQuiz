import customtkinter as ctk
from src.utils.assets import AssetManager
from PIL import Image
from src.utils.verifikasi import send_otp
from src.ui.signup_screen import SignupScreen
from tkinter import messagebox

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, user_instance, login_callback, signup_callback, back_callback, user_callback):
        super().__init__(parent, corner_radius=0, width=1260, height=716)
        self.parent = parent
        self.user_instance = user_instance
        self.login_callback = login_callback
        self.signup_callback = signup_callback
        self.back_callback = back_callback
        self.user_callback = user_callback
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
                size=(561, 716)
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
        
        # 👁 Tombol Show/Hide Password
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
        self.toggle_button.place(relx=0.88, rely=0.55, anchor="center")

        forgot_button = ctk.CTkButton(
            self,
            text="Lupa Password?",
            font=("Inter", 14, "underline"),
            fg_color="transparent",
            text_color="#5F9EA0",  # Warna biru
            hover_color="#444444",
            cursor="hand2",
            width=180,
            height=30,
            command=self.forgot_password
        )
        forgot_button.place(relx=0.75, rely=0.62, anchor="center")

        # --- Frame untuk tombol Login & Register --- 
        auth_buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        auth_buttons_frame.place(relx=0.75, rely=0.7, anchor="center")

        login_button = ctk.CTkButton(
            auth_buttons_frame, # <<< Parent baru
            text="Log in", 
            font=("Inter Bold", 16), 
            width=180, # <<< Ubah ukuran
            height=46, 
            corner_radius=5, 
            fg_color="#6357B1", 
            hover_color="#4F44A3", 
            command=self.on_login
        )
        login_button.pack(side="left", padx=10) # <<< Pack di frame baru
        
        signup_button = ctk.CTkButton(
            auth_buttons_frame, # <<< Parent baru
            text="Register", 
            font=("Inter Bold", 16), 
            width=180, # <<< Ubah ukuran
            height=46, 
            corner_radius=5, 
            fg_color="#6357B1", 
            hover_color="#4F44A3", 
            command=self.signup_callback
        )
        signup_button.pack(side="left", padx=10) # <<< Pack di frame baru

        # Back button
        back_button = ctk.CTkButton(
            self,
            text="Back",
            font=("Inter Bold", 16),
            width=180, # Ukuran tetap 180
            height=46,
            corner_radius=5,
            # <<< Kembalikan warna tombol Back >>>
            fg_color="#333333", 
            hover_color="#444444",
            command=self.back_callback
        )
        back_button.place(relx=0.75, rely=0.8, anchor="center")
    
    def toggle_password(self):
        """Fungsi untuk menampilkan atau menyembunyikan password."""
        self.show_password = not self.show_password
        self.password_entry.configure(show="" if self.show_password else "•")

    def forgot_password(self):
        # Langkah 1: Popup untuk minta email
        email_window = ctk.CTkToplevel(self)
        email_window.title("Lupa Password")
        email_window.geometry("450x250")
        email_window.resizable(False, False)
        email_window.transient(self.parent)
        email_window.grab_set()

        frame = ctk.CTkFrame(email_window, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(frame, text="Masukkan Email Terdaftar", font=("Inter Bold", 20)).pack(pady=(0, 20))
        email_entry = ctk.CTkEntry(frame, width=380, height=40)
        email_entry.pack(pady=(0, 15), fill="x", padx=10)

        def kirim_otp():
            email_value = email_entry.get().strip()

            if not email_value or "@" not in email_value or "." not in email_value:
                messagebox.showerror("Error", "Format email tidak valid.")
                return

            if not self.user_instance._check_email_exists(email_value):
                messagebox.showerror("Error", f"Email '{email_value}' tidak ditemukan di database.")
                return
            
            username_found = self.user_instance.get_username_by_email(email_value)
            if not username_found:
                messagebox.showerror("Error", "Username untuk email tersebut tidak ditemukan.")
                return

            # Kirim OTP
            otp = send_otp(email_value, username_found)
            if not otp:
                messagebox.showerror("Gagal", "Gagal mengirim OTP ke email.")
                return

            # Tutup form email
            email_window.destroy()

            # Lanjutkan ke OTP verification
            def lanjut_reset():
                self.open_password_reset(email_value)

            # Panggil OTP popup dari SignupScreen (jika kamu ingin reuse)
            temp_signup = SignupScreen(self.parent, self.user_instance, self.user_callback)
            temp_signup.open_otp(expected_otp=otp, on_success=lanjut_reset)

        kirim_btn = ctk.CTkButton(
            frame, text="Kirim OTP", font=("Inter Bold", 14),
            command=kirim_otp, fg_color="#6357B1", hover_color="#4F44A3"
        )
        kirim_btn.pack(pady=10)


    def open_password_reset(self, email):
        reset_window = ctk.CTkToplevel(self)
        reset_window.title("Reset Password")
        reset_window.geometry("450x350")
        reset_window.resizable(False, False)
        reset_window.transient(self.parent)
        reset_window.grab_set()

        frame = ctk.CTkFrame(reset_window, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(frame, text="Buat Password Baru", font=("Inter Bold", 20)).pack(pady=(0, 20))

        new_pw_entry = ctk.CTkEntry(frame, placeholder_text="Password Baru", show="•", width=380)
        new_pw_entry.pack(pady=10)

        confirm_pw_entry = ctk.CTkEntry(frame, placeholder_text="Konfirmasi Password", show="•", width=380)
        confirm_pw_entry.pack(pady=10)

        def reset_password():
            new_pw = new_pw_entry.get()
            confirm_pw = confirm_pw_entry.get()

            if new_pw != confirm_pw:
                messagebox.showerror("Error", "Password dan konfirmasi tidak cocok.")
                return

            is_valid, msg = self.user_instance.is_valid_password(new_pw)
            if not is_valid:
                messagebox.showerror("Password Lemah", msg)
                return

            # Update password di file
            lines = self.user_instance._read_users_raw()
            updated = False
            for i, line in enumerate(lines):
                parts = line.strip().split(",", 2)
                if len(parts) == 3 and parts[2].lower() == email.lower():
                    hashed = self.user_instance._hash_password(new_pw)
                    lines[i] = f"{parts[0]},{hashed},{parts[2]}\n"
                    updated = True
                    break

            if updated and self.user_instance._write_users_raw(lines):
                messagebox.showinfo("Sukses", "Password berhasil diperbarui.")
                reset_window.destroy()
                self.user_callback()  # Kembali ke tampilan login
            else:
                messagebox.showerror("Gagal", "Gagal menyimpan password baru.")

        submit_btn = ctk.CTkButton(
            frame, text="Simpan Password", font=("Inter Bold", 14),
            command=reset_password, fg_color="#6357B1", hover_color="#4F44A3"
        )
        submit_btn.pack(pady=15)


    def on_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success = self.user_instance.login(username, password)
        if success:
            self.login_callback()