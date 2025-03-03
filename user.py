import customtkinter as ctk
from tkinter import messagebox

class User:
    def __init__(self, app):
        self.app = app
        self.create_user_frame()

    def create_user_frame(self):
        self.user_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")
        ctk.CTkLabel(self.user_frame, text="User Mode", font=("Arial", 18, "bold")).pack(pady=20)

        self.entry_username = ctk.CTkEntry(self.user_frame, width=200, placeholder_text="Masukkan Nama")
        self.entry_username.pack(pady=5)

        ctk.CTkButton(self.user_frame, text="Mulai Kuis", width=200, command=self.start_quiz).pack(pady=10)
        ctk.CTkButton(self.user_frame, text="Kembali", width=200, command=self.back_to_main).pack(pady=10)

    def open_user_mode(self):
        self.app.main_frame.pack_forget()
        self.user_frame.pack(expand=True, fill="both")

    def start_quiz(self):
        username = self.entry_username.get().strip()
        if username:
            with open("user.txt", "a") as file:
                file.write(username + "\n")
            messagebox.showinfo("Sukses", f"{username} berhasil masuk ke kuis!")
            self.app.quiz.open_quiz_mode(username)
        else:
            messagebox.showerror("Error", "Nama tidak boleh kosong!")

    def back_to_main(self):
        self.user_frame.pack_forget()
        self.app.main_frame.pack(expand=True, fill="both")