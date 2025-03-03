import customtkinter as ctk
from tkinter import messagebox, ttk
import os

ADMIN_PASSWORD = "admin123"

class Admin:
    def __init__(self, app):
        self.app = app
        self.create_admin_frame()

    def create_admin_frame(self):
        self.admin_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")
        ctk.CTkLabel(self.admin_frame, text="Admin Mode", font=("Arial", 18, "bold")).pack(pady=20)

        self.entry_password = ctk.CTkEntry(self.admin_frame, width=200, placeholder_text="Password", show="*")
        self.entry_password.pack(pady=5)

        ctk.CTkButton(self.admin_frame, text="Lanjut", width=200, command=self.validate_admin_password).pack(pady=10)
        ctk.CTkButton(self.admin_frame, text="Kembali", width=200, command=self.back_to_main).pack(pady=10)

    def validate_admin_password(self):
        if self.entry_password.get() == ADMIN_PASSWORD:
            self.open_dashboard()
        else:
            messagebox.showerror("Error", "Password salah!")

    def open_admin_mode(self):
        self.app.main_frame.pack_forget()
        self.admin_frame.pack(expand=True, fill="both")

    def open_dashboard(self):
        self.admin_frame.pack_forget()
        self.create_dashboard()

    def create_dashboard(self):
        self.dashboard_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")
        self.dashboard_frame.pack(expand=True, fill="both")

        # Navbar
        self.navbar = ctk.CTkFrame(self.dashboard_frame, height=50, fg_color="gray")
        self.navbar.pack(fill="x", pady=5)

        ctk.CTkButton(self.navbar, text="Leaderboard", command=self.show_leaderboard).pack(side="left", padx=10)
        ctk.CTkButton(self.navbar, text="Active Users", command=self.show_active_users).pack(side="left", padx=10)
        ctk.CTkButton(self.navbar, text="Tambah Pertanyaan", command=self.show_add_question).pack(side="left", padx=10)
        ctk.CTkButton(self.navbar, text="Lihat Pertanyaan", command=self.show_questions).pack(side="left", padx=10)
        ctk.CTkButton(self.navbar, text="Edit Pertanyaan", command=self.show_edit_question).pack(side="left", padx=10)
        ctk.CTkButton(self.navbar, text="Hapus Pertanyaan", command=self.show_delete_question).pack(side="left", padx=10)
        ctk.CTkButton(self.navbar, text="Kembali", command=self.back_to_admin).pack(side="right", padx=10)

        # Table Frame
        self.table_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.table_frame.pack(expand=True, fill="both", pady=10)

        self.show_active_users()

    def show_active_users(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        if os.path.exists("user.txt"):
            with open("user.txt", "r") as file:
                users = file.readlines()
            users = [user.strip() for user in users]
        else:
            users = []

        columns = ("#1", "#2")
        self.table = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.table.heading("#1", text="Username")
        self.table.heading("#2", text="Status")

        for user in users:
            self.table.insert("", "end", values=(user, "Active"))

        self.table.pack(expand=True, fill="both")

    def show_leaderboard(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        if os.path.exists("leaderboard.txt"):
            with open("leaderboard.txt", "r") as file:
                scores = [line.strip().split("|") for line in file.readlines()]
        else:
            scores = []

        columns = ("#1", "#2")
        self.table = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.table.heading("#1", text="Username")
        self.table.heading("#2", text="Score")

        for score in scores:
            self.table.insert("", "end", values=(score[0], score[1]))

        self.table.pack(expand=True, fill="both")

    def show_add_question(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.add_question_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.add_question_frame.pack(expand=True, fill="both")

        ctk.CTkLabel(self.add_question_frame, text="Tambah Pertanyaan", font=("Arial", 16, "bold")).pack(pady=10)

        self.entry_question = ctk.CTkEntry(self.add_question_frame, width=400, placeholder_text="Masukkan Pertanyaan")
        self.entry_question.pack(pady=5)

        self.entry_answer = ctk.CTkEntry(self.add_question_frame, width=400, placeholder_text="Masukkan Jawaban")
        self.entry_answer.pack(pady=5)

        ctk.CTkButton(self.add_question_frame, text="Tambah", width=200, command=self.add_question).pack(pady=10)

    def show_questions(self):
        questions = self.read_questions()
        if not questions:
            messagebox.showinfo("Info", "Tidak ada pertanyaan yang tersedia!")
        else:
            questions_text = "\n".join([f"{i+1}. {q['question']} | Jawaban: {q['answer']}" for i, q in enumerate(questions)])
            messagebox.showinfo("Daftar Pertanyaan", questions_text)

    def show_edit_question(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.edit_question_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.edit_question_frame.pack(expand=True, fill="both")

        ctk.CTkLabel(self.edit_question_frame, text="Edit Pertanyaan", font=("Arial", 16, "bold")).pack(pady=10)

        self.entry_edit_number = ctk.CTkEntry(self.edit_question_frame, width=400, placeholder_text="Nomor Pertanyaan")
        self.entry_edit_number.pack(pady=5)

        self.entry_edit_question = ctk.CTkEntry(self.edit_question_frame, width=400, placeholder_text="Pertanyaan Baru")
        self.entry_edit_question.pack(pady=5)

        self.entry_edit_answer = ctk.CTkEntry(self.edit_question_frame, width=400, placeholder_text="Jawaban Baru")
        self.entry_edit_answer.pack(pady=5)

        ctk.CTkButton(self.edit_question_frame, text="Edit", width=200, command=self.edit_question).pack(pady=10)

    def show_delete_question(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.delete_question_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.delete_question_frame.pack(expand=True, fill="both")

        ctk.CTkLabel(self.delete_question_frame, text="Hapus Pertanyaan", font=("Arial", 16, "bold")).pack(pady=10)

        self.entry_delete = ctk.CTkEntry(self.delete_question_frame, width=400, placeholder_text="Nomor Pertanyaan")
        self.entry_delete.pack(pady=5)

        ctk.CTkButton(self.delete_question_frame, text="Hapus", width=200, command=self.delete_question).pack(pady=10)

    def read_questions(self):
        questions = []
        if os.path.exists("quiz_questions.txt"):
            with open("quiz_questions.txt", "r") as file:
                for line in file:
                    question, answer = line.strip().split("|")
                    questions.append({"question": question, "answer": answer})
        return questions

    def add_question(self):
        question = self.entry_question.get()
        answer = self.entry_answer.get()
        if question and answer:
            with open("quiz_questions.txt", "a") as file:
                file.write(f"{question}|{answer}\n")
            messagebox.showinfo("Sukses", "Pertanyaan berhasil ditambahkan!")
            self.entry_question.delete(0, ctk.END)
            self.entry_answer.delete(0, ctk.END)
        else:
            messagebox.showerror("Error", "Pertanyaan dan jawaban tidak boleh kosong!")

    def delete_question(self):
        try:
            question_number = int(self.entry_delete.get()) - 1
            questions = self.read_questions()
            if 0 <= question_number < len(questions):
                questions.pop(question_number)
                with open("quiz_questions.txt", "w") as file:
                    for q in questions:
                        file.write(f"{q['question']}|{q['answer']}\n")
                messagebox.showinfo("Sukses", "Pertanyaan berhasil dihapus!")
            else:
                messagebox.showerror("Error", "Nomor pertanyaan tidak valid!")
        except ValueError:
            messagebox.showerror("Error", "Input harus berupa angka!")

    def edit_question(self):
        try:
            question_number = int(self.entry_edit_number.get()) - 1
            questions = self.read_questions()
            if 0 <= question_number < len(questions):
                new_question = self.entry_edit_question.get()
                new_answer = self.entry_edit_answer.get()
                if new_question and new_answer:
                    questions[question_number] = {"question": new_question, "answer": new_answer}
                    with open("quiz_questions.txt", "w") as file:
                        for q in questions:
                            file.write(f"{q['question']}|{q['answer']}\n")
                    messagebox.showinfo("Sukses", "Pertanyaan berhasil diubah!")
                    self.entry_edit_number.delete(0, ctk.END)
                    self.entry_edit_question.delete(0, ctk.END)
                    self.entry_edit_answer.delete(0, ctk.END)
                else:
                    messagebox.showerror("Error", "Pertanyaan dan jawaban tidak boleh kosong!")
            else:
                messagebox.showerror("Error", "Nomor pertanyaan tidak valid!")
        except ValueError:
            messagebox.showerror("Error", "Input harus berupa angka!")

    def back_to_admin(self):
        self.dashboard_frame.pack_forget()
        self.admin_frame.pack(expand=True, fill="both")

    def back_to_main(self):
        self.admin_frame.pack_forget()
        self.app.main_frame.pack(expand=True, fill="both")