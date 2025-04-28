import customtkinter as ctk
from tkinter import messagebox
import bcrypt
import re
import os
import hashlib

class User:
    def __init__(self, app):
        self.app = app
        self.logged_in_username = None # <<< Simpan username yang login
        self.db_file = "database/user.txt"
        self._ensure_db_exists()

        self.user_frame = None
        self.register_frame = None
        self.login_frame = None

    def _ensure_db_exists(self):
        """Memastikan direktori dan file database ada."""
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                pass # Buat file kosong jika belum ada

    def _hash_password(self, password):
        """Melakukan hash pada password menggunakan SHA-256."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def _check_username_exists(self, username):
        """Memeriksa apakah username sudah ada di database."""
        try:
            with open(self.db_file, 'r') as f:
                for line in f:
                    # Periksa apakah baris tidak kosong sebelum split
                    if line.strip():
                         stored_username, _ = line.strip().split(",", 1)
                         if stored_username == username:
                              return True
        except FileNotFoundError:
            return False # File belum ada, berarti username belum ada
        except Exception as e:
            print(f"Error checking username: {e}")
            messagebox.showerror("Database Error", f"Terjadi kesalahan saat memeriksa username: {e}")
            return True # Anggap ada error sebagai username sudah ada untuk mencegah duplikasi
        return False

    def _check_email_exists(self, email):
        try:
            with open(self.db_file, 'r') as f:
                for line in f:
                    parts = line.strip().split(",", 2)
                    if len(parts) == 3 and parts[2].lower() == email.lower():
                        return True
        except Exception as e:
            print(f"Error checking email: {e}")
            messagebox.showerror("Database Error", f"Terjadi kesalahan saat memeriksa email: {e}")
        return False

    def _read_users_raw(self):
        """Membaca semua baris mentah dari file database pengguna."""
        lines = []
        try:
            with open(self.db_file, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"User database file not found: {self.db_file}")
        except Exception as e:
            print(f"Error reading user file: {e}")
            messagebox.showerror("Database Error", f"Gagal membaca data pengguna: {e}")
        return lines
    

    def _write_users_raw(self, lines):
        """Menulis ulang file database dengan baris yang diberikan."""
        temp_file = self.db_file + ".tmp"
        try:
            with open(temp_file, 'w') as temp_f:
                temp_f.writelines(lines)
            os.replace(temp_file, self.db_file)
            return True
        except Exception as e:
            print(f"Error rewriting user file: {e}")
            messagebox.showerror("Database Error", f"Gagal menyimpan perubahan data pengguna: {e}")
            if os.path.exists(temp_file):
                try: os.remove(temp_file)
                except Exception as remove_e: print(f"Failed to remove temp file: {remove_e}")
            return False

    def register(self, username, password, email):
        """Mendaftarkan pengguna baru dengan password yang di-hash."""
        # Hash password
        hashed_password = self._hash_password(password)

        # Simpan ke file
        try:
            with open(self.db_file, 'a') as f:
                f.write(f"{username},{hashed_password},{email}\n")
            messagebox.showinfo("Registrasi Berhasil", f"Akun untuk '{username}' berhasil dibuat. Silakan login.")
            return True # <<< Kembalikan True jika berhasil
        except Exception as e:
            print(f"Error saving user data: {e}")
            messagebox.showerror("Registrasi Gagal", f"Terjadi kesalahan saat menyimpan data: {e}")
            return False

    def login(self, username, password):
        """Memproses login pengguna dengan membandingkan hash password."""
        if not username or not password:
            messagebox.showerror("Login Gagal", "Username dan password tidak boleh kosong.")
            return False

        try:
            lines = self._read_users_raw()
            for line in lines:
                 if line.strip():
                     parts = line.strip().split(",", 2)
                     if len(parts) >= 2:
                        stored_username, stored_hashed_password = parts[0], parts[1]
                        if stored_username == username:
                            input_hashed_password = self._hash_password(password)
                            if input_hashed_password == stored_hashed_password:
                                self.logged_in_username = username # <<< Simpan username
                                return True # Login sukses
                            else:
                                messagebox.showerror("Login Gagal", "Password salah.")
                                return False # Password salah
            # Jika loop selesai tanpa menemukan username
            messagebox.showerror("Login Gagal", f"Username '{username}' tidak ditemukan.")
            return False
        except FileNotFoundError:
             messagebox.showerror("Login Gagal", "Database pengguna tidak ditemukan.")
             return False
        except Exception as e:
            print(f"Error during login: {e}")
            messagebox.showerror("Login Error", f"Terjadi kesalahan saat login: {e}")
            return False

    def logout(self):
        """Melakukan logout pengguna."""
        self.logged_in_username = None # <<< Reset username
        print("User logged out.")

    def get_current_user(self):
        """Mengembalikan username pengguna yang sedang login."""
        return self.logged_in_username
    
    def get_username_by_email(self, email):
        """Mengembalikan username berdasarkan email, jika ditemukan."""
        try:
            lines = self._read_users_raw()
            for line in lines:
                parts = line.strip().split(",", 2)
                if len(parts) == 3 and parts[2].lower() == email.lower():
                    return parts[0]  # username
        except Exception as e:
            print(f"Error getting username from email: {e}")
            messagebox.showerror("Database Error", f"Gagal mencari username dari email: {e}")
        return None

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
    
    def update_password(self, username, old_password, new_password, confirm_password):
        """Memperbarui password pengguna."""
        # Validasi dasar
        if not old_password or not new_password or not confirm_password:
            messagebox.showerror("Ubah Password Gagal", "Semua field harus diisi.")
            return False
        if new_password != confirm_password:
            messagebox.showerror("Ubah Password Gagal", "Password baru dan konfirmasi tidak cocok.")
            return False

        # Validasi Kekuatan Password Baru (Jika metode is_valid_password ada)
        if hasattr(self, 'is_valid_password'):
             is_valid, message = self.is_valid_password(new_password)
             if not is_valid:
                  messagebox.showerror("Ubah Password Gagal", message)
                  return False

        # Verifikasi password lama
        lines = self._read_users_raw()
        user_found = False
        line_index_to_update = -1
        stored_hashed_password = ""

        for i, line in enumerate(lines):
            if line.strip():
                stored_username, current_hash = line.strip().split(",", 1)
                if stored_username == username:
                    user_found = True
                    line_index_to_update = i
                    stored_hashed_password = current_hash
                    break

        if not user_found:
             messagebox.showerror("Error", "Terjadi kesalahan: pengguna saat ini tidak ditemukan di database.")
             return False

        # Cek hash password lama
        old_password_hash = self._hash_password(old_password)
        if old_password_hash != stored_hashed_password:
            messagebox.showerror("Ubah Password Gagal", "Password lama salah.")
            return False

        # Hash password baru
        new_password_hash = self._hash_password(new_password)

        # Update baris di daftar lines
        lines[line_index_to_update] = f"{username},{new_password_hash}\n"

        # Tulis ulang file
        if self._write_users_raw(lines):
            messagebox.showinfo("Sukses", "Password berhasil diperbarui.")
            return True
        else:
            # Error sudah ditampilkan oleh _write_users_raw
            return False

    def delete_account(self, username, password):
        """Menghapus akun pengguna setelah verifikasi password."""
        # Verifikasi password untuk keamanan
        lines = self._read_users_raw()
        user_found = False
        stored_hashed_password = ""

        for line in lines:
            if line.strip():
                stored_username, current_hash = line.strip().split(",", 1)
                if stored_username == username:
                    user_found = True
                    stored_hashed_password = current_hash
                    break

        if not user_found:
             messagebox.showerror("Error", "Terjadi kesalahan: pengguna saat ini tidak ditemukan di database.")
             return False

        # Cek hash password
        password_hash = self._hash_password(password)
        if password_hash != stored_hashed_password:
            messagebox.showerror("Hapus Akun Gagal", "Password salah. Penghapusan dibatalkan.")
            return False

        # Buat daftar baris baru tanpa pengguna yang dihapus
        lines_to_keep = [line for line in lines if not line.startswith(username + ",")]

        # Tulis ulang file
        if self._write_users_raw(lines_to_keep):
            messagebox.showinfo("Sukses", f"Akun '{username}' telah berhasil dihapus.")
            return True
        else:
            # Error sudah ditampilkan oleh _write_users_raw
            return False
def search_user(username):
    with open("database/user.txt", "r", encoding="utf-8") as f:
        for line in f:
            user, _ = line.strip().split(",", 1)
            if user.lower() == username.lower():
                return True
    return False