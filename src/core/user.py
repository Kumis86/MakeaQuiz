import customtkinter as ctk
from tkinter import messagebox
import bcrypt
import re
import os

class User:
    def __init__(self, app, file="database/user.txt"):
        self.app = app
        self.file = file
        # Ensure database directory exists
        os.makedirs("database", exist_ok=True)
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

        is_valid, message = self.is_valid_password(password)
        if not is_valid:
            messagebox.showerror("Gagal", message)
            return
        
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        role = "admin" if isadmin else "user"
        self.user[username] = {"password": hashed_pw, "role": role}
        self.save_users()
        messagebox.showinfo("Sukses", f"{username} berhasil masuk ke kuis!, silakan login.")

    def is_valid_password(self, password):
        """Memeriksa apakah password memenuhi kriteria keamanan"""

        if len(password) < 8:
            return False, "Kata sandi harus memiliki minimal 8 karakter."
        if not re.search(r"[A-Z]", password):
            return False, "Kata sandi harus mengandung minimal satu huruf besar."
        if not re.search(r"[a-z]", password):
            return False, "Kata sandi harus mengandung minimal satu huruf kecil."
        if not re.search(r"\d", password):
            return False, "Kata sandi harus mengandung minimal satu angka."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Kata sandi harus mengandung minimal satu simbol."
        if re.search(r"(password|12345678|admin|qwerty)", password, re.IGNORECASE):
            return False, "Kata sandi tidak boleh mengandung kata umum yang mudah ditebak."
 
        return True, "Password valid."
    
    def login(self, username, password):
        if username in self.user:
            hashed_pw = self.user[username]["password"].encode('utf-8')
            if bcrypt.checkpw(password.encode(), hashed_pw):
                messagebox.showinfo("Sukses", "Login berhasil!")
                return True, self.user[username]["role"]

        messagebox.showerror("Login Gagal", "Username atau Password salah!")
        return None

    def isadmin(self, username):
        return self.user.get(username, {}).get("role") == "admin"