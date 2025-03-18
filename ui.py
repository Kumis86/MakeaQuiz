import customtkinter as ctk
from tkinter import messagebox
from user import User
from admin import Admin
from quiz import Quiz

class App:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("MakeaQuiz v2")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)

        self.user = User(self)
        self.admin = Admin(self)
        self.quiz = Quiz(self)

        self.create_main_menu()

    def create_main_menu(self):
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both")

        title_label = ctk.CTkLabel(self.main_frame, text="MakeaQuiz", font=("Arial", 80, "bold"))
        title_label.pack(pady=10)

        ctk.CTkLabel(self.main_frame, text="Uji Pengetahuanmu, Raih Skor Terbaikmu", font=("Arial", 10)).pack(pady=10)

        ctk.CTkButton(self.main_frame, text="User", width=200, command=self.user.open_user_mode).pack(pady=10)
        ctk.CTkLabel(self.main_frame, text="OR", font=("Arial", 10)).pack(pady=5)
        ctk.CTkButton(self.main_frame, text="Admin", width=200, command=self.admin.open_admin_mode).pack(pady=10)

    def run(self):
        self.root.mainloop()
