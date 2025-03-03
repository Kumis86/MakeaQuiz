import customtkinter as ctk
from tkinter import messagebox
import os

class Quiz:
    def __init__(self, app):
        self.app = app
        self.create_quiz_frame()

    def create_quiz_frame(self):
        self.quiz_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")
        ctk.CTkLabel(self.quiz_frame, text="Mode Kuis", font=("Arial", 18, "bold")).pack(pady=20)

        self.quiz_question_label = ctk.CTkLabel(self.quiz_frame, text="", font=("Arial", 14))
        self.quiz_question_label.pack(pady=10)

        self.entry_answer = ctk.CTkEntry(self.quiz_frame, width=400, placeholder_text="Masukkan Jawaban")
        self.entry_answer.pack(pady=5)

        ctk.CTkButton(self.quiz_frame, text="Jawab", width=200, command=self.submit_answer).pack(pady=10)
        ctk.CTkButton(self.quiz_frame, text="Kembali", width=200, command=self.back_to_user).pack(pady=10)

    def open_quiz_mode(self, username):
        self.username = username
        self.app.user.user_frame.pack_forget()
        self.quiz_frame.pack(expand=True, fill="both")
        self.load_question()

    def load_question(self):
        if os.path.exists("quiz_questions.txt"):
            with open("quiz_questions.txt", "r") as file:
                questions = [line.strip().split("|") for line in file.readlines()]
            if questions:
                self.current_question, self.correct_answer = questions[0]
                self.quiz_question_label.configure(text=self.current_question)
            else:
                self.quiz_question_label.configure(text="Tidak ada pertanyaan!")
        else:
            self.quiz_question_label.configure(text="Tidak ada pertanyaan!")

    def submit_answer(self):
        user_answer = self.entry_answer.get().strip()
        if user_answer == self.correct_answer:
            messagebox.showinfo("Jawaban", "Jawaban Anda benar!")
            self.save_score(10)  # Tambahkan skor 10 untuk jawaban benar
        else:
            messagebox.showinfo("Jawaban", "Jawaban Anda salah!")
            self.save_score(0)  # Tambahkan skor 0 untuk jawaban salah

    def save_score(self, score):
        with open("leaderboard.txt", "a") as file:
            file.write(f"{self.username}|{score}\n")

    def back_to_user(self):
        self.quiz_frame.pack_forget()
        self.app.user.user_frame.pack(expand=True, fill="both")