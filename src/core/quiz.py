import customtkinter as ctk
from tkinter import messagebox
import os
from src.core.questions import EssayQuestion, MCQuestion, TFQuestion

class Quiz:
    def __init__(self, app):
        self.app = app
        self.questions = []
        self.current_question_index = 0
        self.total_score = 0
        self.username = ""
        self.create_quiz_frame()
        self.timer_minutes = 0
        self.remaining_time = 0
        self.timer_label = None
        self.timer_running = False
        self.timer_id = None

    def create_quiz_frame(self):
        self.quiz_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")
        ctk.CTkLabel(self.quiz_frame, text="Mode Kuis", font=("Arial", 18, "bold")).pack(pady=20)
        
        self.question_container = ctk.CTkFrame(self.quiz_frame, fg_color="transparent")
        self.question_container.pack(expand=True, fill="both", pady=20)
        
        self.answer_container = ctk.CTkFrame(self.quiz_frame, fg_color="transparent")
        self.answer_container.pack(fill="x", pady=10)
        
        ctk.CTkButton(self.quiz_frame, text="Kembali", width=200, command=self.back_to_user).pack(pady=10)

    def clear_widgets(self, container):
        for widget in container.winfo_children():
            widget.destroy()

    def open_quiz_mode(self, username):
        self.username = username
        self.total_score = 0
        self.current_question_index = 0
        self.app.user.user_frame.pack_forget()
        self.quiz_frame.pack(expand=True, fill="both")
        self.load_questions()
        self.load_next_question()
        self.load_timer_config()
        self.remaining_time = self.timer_minutes * 60  # Convert to seconds
        self.start_timer()

    def load_questions(self):
        self.questions = []
        if not os.path.exists("database/quiz_questions.txt"):
            return
        
        try:
            with open("database/quiz_questions.txt", "r") as file:
                for line in file:
                    parts = line.strip().split("|")
                    q_type = parts[0]
                    
                    if q_type == "Essay":
                        if len(parts) >= 3:
                            self.questions.append(EssayQuestion(parts[1], parts[2]))
                    elif q_type == "MC":
                        if len(parts) >= 6:
                            options = parts[2:-1]
                            correct_idx = parts[-1]
                            self.questions.append(MCQuestion(parts[1], options, correct_idx))
                    elif q_type == "TF":
                        if len(parts) >= 3:
                            self.questions.append(TFQuestion(parts[1], parts[2]))
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat pertanyaan: {str(e)}")

    def load_next_question(self):
        self.clear_widgets(self.question_container)
        self.clear_widgets(self.answer_container)

        if self.current_question_index >= len(self.questions):
            self.stop_timer()
            self.save_final_score()
            messagebox.showinfo("Quiz Selesai", 
                f"Selamat {self.username}! Skor akhir: {self.total_score}")
            self.back_to_user()
            return

        self.current_question = self.questions[self.current_question_index]
        self.current_question_index += 1
        self.display_question()

    def display_question(self):
        ctk.CTkLabel(self.question_container, 
                    text=self.current_question.question_text, 
                    font=("Arial", 14)).pack(pady=10)
        
        answer_widget = self.current_question.display_question(self.answer_container)
        ctk.CTkButton(self.answer_container, 
                     text="Jawab", 
                     command=lambda: self.check_answer(answer_widget)).pack(pady=10)

    def check_answer(self, answer_widget):
        if not self.timer_running:
            return  # Prevent answering after timeout

        try:
            # Validate answer exists
            if isinstance(self.current_question, EssayQuestion):
                if answer_widget.get().strip() == "":
                    messagebox.showwarning("Peringatan", "Harap isi kolom jawaban!")
                    return
            elif isinstance(self.current_question, MCQuestion):
                if answer_widget.get() == -1:
                    messagebox.showwarning("Peringatan", "Harap pilih opsi jawaban!")
                    return
            elif isinstance(self.current_question, TFQuestion):
                if answer_widget.get() == "":
                    messagebox.showwarning("Peringatan", "Harap pilih True/False!")
                    return

            is_correct = self.current_question.check_answer(answer_widget)
            score = 10 if is_correct else 0
            self.total_score += score
            
            feedback = "Benar" if is_correct else "Salah"
            messagebox.showinfo("Hasil", f"Jawaban {feedback}! Skor sementara: {self.total_score}")
            
            self.load_next_question()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memproses jawaban: {str(e)}")

    def save_final_score(self):
        try:
            with open("database/leaderboard.txt", "a") as file:
                file.write(f"{self.username}|{self.total_score}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan skor: {str(e)}")

    def load_timer_config(self):
        # Default to 5 minutes if not configured
        self.timer_minutes = 5
        try:
            with open("database/quiz_settings.txt", "r") as f:
                for line in f:
                    if "timer_minutes" in line:
                        self.timer_minutes = int(line.split("=")[1])
        except FileNotFoundError:
            pass

    def start_timer(self):
        # Create timer container frame
        self.timer_frame = ctk.CTkFrame(self.quiz_frame, fg_color="#333333", corner_radius=8)
        self.timer_frame.pack(side="top", anchor="nw", padx=20, pady=10)
    
        # Create layout grid
        self.timer_frame.grid_columnconfigure(0, weight=1)
        self.timer_frame.grid_columnconfigure(1, weight=1)
    
        # Text label
        ctk.CTkLabel(self.timer_frame, 
                    text="Waktu tersisa:", 
                    font=("Arial", 14, "bold"),
                    anchor="w").grid(row=0, column=0, padx=5, sticky="w")
    
        # Time display label
        self.timer_label = ctk.CTkLabel(self.timer_frame,
                                    text="00:00:00",
                                    font=("Arial", 14, "bold"))
        self.timer_label.grid(row=0, column=1, padx=5, sticky="e")
    
        # Initialize timer
        self.update_timer_display()
        self.timer_running = True
        self.update_timer()

    def update_timer_display(self):
        hours = self.remaining_time // 3600
        remainder = self.remaining_time % 3600
        minutes = remainder // 60
        seconds = remainder % 60
        self.timer_label.configure(text=f"{hours:02}:{minutes:02}:{seconds:02}")

    def update_timer(self):
        if self.timer_running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_timer_display()
            self.timer_id = self.app.root.after(1000, self.update_timer)
        elif self.remaining_time <= 0:
            self.timer_expired()

    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False
        if self.timer_id is not None:
            self.app.root.after_cancel(self.timer_id)
            self.timer_id = None

    def timer_expired(self):
        self.stop_timer()
        messagebox.showinfo("Time's Up!", "Time has expired! Submitting answers...")
        self.force_submit()

    def force_submit(self):
        # Answer all remaining questions as incorrect
        while self.current_question_index < len(self.questions):
            self.total_score += 0  # No points for unanswered questions
            self.current_question_index += 1
        self.save_final_score()
        self.back_to_user()

    def back_to_user(self):
        if 0 < self.current_question_index < len(self.questions):
            confirm = messagebox.askyesno(
                "Konfirmasi Keluar", 
                "Quiz belum selesai. Jika keluar sekarang, progres tidak akan disimpan.\nApakah Anda yakin ingin keluar?"
            )
            if not confirm:
                return
            
        self.quiz_frame.pack_forget()
        self.app.user.user_frame.pack(expand=True, fill="both")
