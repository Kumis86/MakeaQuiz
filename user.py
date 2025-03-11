import customtkinter as ctk
from tkinter import messagebox
import bcrypt

class User:
    def __init__(self, app, file="user.txt"):
        self.app = app
        self.file = file
        self.user = self.load_users()

        self.user_frame = None
        self.register_frame = None
        self.login_frame = None

    def load_users(self):
        user = {}
        try:
            with open(self.file, "r") as f:
                for line in f:
                    username, password, role = line.strip().split(",")
                    user[username] = {"password": password, "role": role}
        except FileNotFoundError:
            pass
        return user

    def save_users(self):
        with open(self.file, "w") as f:
            for username, data in self.user.items():
                f.write(f"{username},{data['password']},{data['role']}\n")

    def register(self, username, password, isadmin=False):
        if username in self.user:
            messagebox.showerror("Gagal", "Username sudah ada!")
            return
        
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        role = "admin" if isadmin else "user"
        self.user[username] = {"password": hashed_pw, "role": role}
        self.save_users()
        messagebox.showinfo("Sukses", f"{username} berhasil masuk ke kuis!, silakan login.")

    def login(self, username, password):
        if username in self.user:
            hashed_pw = self.user[username]["password"].encode('utf-8')
            if bcrypt.checkpw(password.encode(), hashed_pw):
                messagebox.showinfo("Sukses", "Login berhasil!")
                return "Login berhasil!", self.user[username]["role"]

        messagebox.showerror("Gagal", "Username atau password salah!")
        return None, None

    def isadmin(self, username):
        return self.user.get(username, {}).get("role") == "admin"

    def open_user_mode(self):
        """Menampilkan halaman User Mode dengan tombol Register dan Login"""
        if self.app.main_frame:
            self.app.main_frame.pack_forget()

        self.user_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")
        self.user_frame.pack(expand=True, fill="both")

        ctk.CTkLabel(self.user_frame, text="User Mode", font=("Arial", 30, "bold")).pack(pady=10)
        ctk.CTkButton(self.user_frame, text="Register", width=200, command=self.open_register).pack(pady=10)
        ctk.CTkLabel(self.user_frame, text="OR", font=("Arial", 10)).pack(pady=5)
        ctk.CTkButton(self.user_frame, text="Login", width=200, command=self.open_login).pack(pady=10)
        ctk.CTkButton(self.user_frame, text="Kembali", width=200, command=self.back_to_main).pack(pady=10)

    def open_register(self):
        """Menampilkan form registrasi"""
        if self.user_frame:
            self.user_frame.pack_forget()

        self.register_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")
        self.register_frame.pack(expand=True, fill="both")

        ctk.CTkLabel(self.register_frame, text="Register", font=("Arial", 30, "bold")).pack(pady=10)

        entry_username = ctk.CTkEntry(self.register_frame, width=200, placeholder_text="Masukkan Username")
        entry_username.pack(pady=5)

        entry_password = ctk.CTkEntry(self.register_frame, width=200, show="*", placeholder_text="Masukkan Password")
        entry_password.pack(pady=5)

        def save_register():
            username = entry_username.get()
            password = entry_password.get()
            self.register(username, password)

        ctk.CTkButton(self.register_frame, text="Daftar", width=200, command=save_register).pack(pady=10)
        ctk.CTkButton(self.register_frame, text="Kembali", width=200, command=self.back_to_user_mode).pack(pady=10)

    def open_login(self):
        """Menampilkan form login"""
        if self.user_frame:
            self.user_frame.pack_forget()

        self.login_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")
        self.login_frame.pack(expand=True, fill="both")

        ctk.CTkLabel(self.login_frame, text="Login", font=("Arial", 30, "bold")).pack(pady=10)

        entry_username = ctk.CTkEntry(self.login_frame, width=200, placeholder_text="Masukkan Username")
        entry_username.pack(pady=5)

        entry_password = ctk.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="Masukkan Password")
        entry_password.pack(pady=5)

        def save_login():
            username = entry_username.get()
            password = entry_password.get()
            status, role = self.login(username, password)
            if status:
                if role == "admin":
                    self.app.admin.open_admin_mode()
                else:
                    if self.login_frame:
                        self.login_frame.pack_forget()
                    self.app.quiz.open_quiz_mode(username)

        ctk.CTkButton(self.login_frame, text="Masuk", width=200, command=save_login).pack(pady=10)
        ctk.CTkButton(self.login_frame, text="Kembali", width=200, command=self.back_to_user_mode).pack(pady=10)


    def back_to_user_mode(self):
        """Kembali ke User Mode dari Register/Login"""
        if self.register_frame:
            self.register_frame.pack_forget()
        if self.login_frame:
            self.login_frame.pack_forget()

        self.open_user_mode()

    def back_to_main(self):
        """Kembali ke menu utama"""
        if self.user_frame:
            self.user_frame.pack_forget()
        if self.register_frame:
            self.register_frame.pack_forget()
        if self.login_frame:
            self.login_frame.pack_forget()

        self.app.main_frame.pack(expand=True, fill="both")