import customtkinter as ctk
from tkinter import messagebox
import os
from abc import ABC, abstractmethod

class Question(ABC):
    def __init__(self, question_text, correct_answer):
        self.question_text = question_text
        self.correct_answer = correct_answer
    
    @abstractmethod
    def display_question(self, container):
        pass
    
    @abstractmethod
    def check_answer(self, user_input):
        pass

class EssayQuestion(Question):
    def display_question(self, container):
        entry = ctk.CTkEntry(container, width=400)
        entry.pack(pady=10)
        return entry
    
    def check_answer(self, user_input):
        return user_input.lower().strip() == self.correct_answer.lower()

class MCQuestion(Question):
    def __init__(self, question_text, options, correct_index):
        super().__init__(question_text, int(correct_index))
        self.options = options
        self.selected = ctk.IntVar(value=-1)
    
    def display_question(self, container):
        for idx, option in enumerate(self.options):
            btn = ctk.CTkRadioButton(container, 
                                   text=option,
                                   variable=self.selected,
                                   value=idx)
            btn.pack(pady=5)
        return self.selected
    
    def check_answer(self, user_input):
        return self.correct_answer == self.selected.get()

class TFQuestion(Question):
    def __init__(self, question_text, correct_answer):
        super().__init__(question_text, correct_answer)
        self.selected = ctk.StringVar(value="")
    
    def display_question(self, container):
        ctk.CTkRadioButton(container, 
                         text="True",
                         variable=self.selected,
                         value="True").pack()
        ctk.CTkRadioButton(container, 
                         text="False",
                         variable=self.selected,
                         value="False").pack()
        return self.selected
    
    def check_answer(self, user_input):
        return self.selected.get() == self.correct_answer

class Quiz:
    def __init__(self, app):
        self.app = app
        self.current_question = None
        self.create_quiz_frame()

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
        self.app.user.user_frame.pack_forget()
        self.quiz_frame.pack(expand=True, fill="both")
        self.load_next_question()

    def load_next_question(self):
        self.clear_widgets(self.question_container)
        self.clear_widgets(self.answer_container)
        
        questions = self.load_questions()
        if not questions:
            ctk.CTkLabel(self.question_container, text="Tidak ada pertanyaan tersedia!", font=("Arial", 14)).pack()
            return
        
        self.current_question = questions[0]
        self.display_question()

    def load_questions(self):
        if not os.path.exists("quiz_questions.txt"):
            return []
        
        with open("quiz_questions.txt", "r") as file:
            questions = []
            for line in file:
                parts = line.strip().split("|")
                q_type = parts[0]
                
                if q_type == "Essay":
                    questions.append(EssayQuestion(parts[1], parts[2]))
                elif q_type == "MC":
                    options = parts[2:-1]
                    correct_idx = parts[-1]
                    questions.append(MCQuestion(parts[1], options, correct_idx))
                elif q_type == "TF":
                    questions.append(TFQuestion(parts[1], parts[2]))
            return questions

    def display_question(self):
        # Display question text
        ctk.CTkLabel(self.question_container, 
                    text=self.current_question.question_text, 
                    font=("Arial", 14)).pack(pady=10)
        
        # Display answer UI
        answer_widget = self.current_question.display_question(self.answer_container)
        
        # Submit button
        ctk.CTkButton(self.answer_container, 
                     text="Jawab", 
                     command=lambda: self.check_answer(answer_widget)).pack(pady=10)

    def check_answer(self, answer_widget):
        is_correct = self.current_question.check_answer(answer_widget)
        
        if is_correct:
            messagebox.showinfo("Hasil", "Jawaban Benar!")
            self.save_score(10)
        else:
            messagebox.showinfo("Hasil", "Jawaban Salah!")
            self.save_score(0)
        
        self.load_next_question()

    def save_score(self, score):
        with open("leaderboard.txt", "a") as file:
            file.write(f"{self.username}|{score}\n")

    def back_to_user(self):
        self.quiz_frame.pack_forget()
        self.app.user.user_frame.pack(expand=True, fill="both")
