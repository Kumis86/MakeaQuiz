import customtkinter as ctk
from tkinter import messagebox, ttk
import os
from scraper import Scraper
from question import EssayQuestion, MCQuestion, TFQuestion

ADMIN_PASSWORD = "admin123"

class Admin:
    def __init__(self, app):
        self.app = app
        self.current_edit_question = None
        self.scraper = Scraper(app)  # Inisialisasi Scraper
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
        ctk.CTkButton(self.navbar, text="Upload Soal", command=self.show_upload_question).pack(side="left", padx=10)
        ctk.CTkButton(self.navbar, text="Tambah Pertanyaan", command=self.show_add_question).pack(side="left", padx=10)
        ctk.CTkButton(self.navbar, text="Lihat Pertanyaan", command=self.show_questions).pack(side="left", padx=10)
        ctk.CTkButton(self.navbar, text="Edit Pertanyaan", command=self.show_edit_question).pack(side="left", padx=10)
        ctk.CTkButton(self.navbar, text="Hapus Pertanyaan", command=self.show_delete_question).pack(side="left", padx=10)
        ctk.CTkButton(self.navbar, text="Set Timer", command=self.show_set_timer).pack(side="left", padx=10)
        ctk.CTkButton(self.navbar, text="Kembali", command=self.back_to_admin).pack(side="right", padx=10)

        # Table Frame
        self.table_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.table_frame.pack(expand=True, fill="both", pady=10)

        self.show_active_users()

    def show_active_users(self):
        # Clear all widgets in table frame first
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        if os.path.exists("user.txt"):
            with open("user.txt", "r") as file:
                users = [line.strip().split(",")[0] for line in file.readlines()]
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
        # Clear all widgets in table frame first
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
        # Clear all widgets in table frame first
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.add_question_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.add_question_frame.pack(expand=True, fill="both")

        ctk.CTkLabel(self.add_question_frame, text="Tambah Pertanyaan", font=("Arial", 16, "bold")).pack(pady=10)

        # Question type selector
        self.q_type = ctk.StringVar(value="Essay")
        ctk.CTkOptionMenu(self.add_question_frame, 
                        values=["Essay", "MC", "TF"],
                        variable=self.q_type).pack(pady=5)

        # Common fields
        self.entry_question = ctk.CTkEntry(self.add_question_frame, width=400, placeholder_text="Pertanyaan")
        self.entry_question.pack(pady=5)

        # Dynamic fields container
        self.dynamic_fields = ctk.CTkFrame(self.add_question_frame, fg_color="transparent")
        self.dynamic_fields.pack(pady=5)
        
        # Initial fields for essay
        self.answer_field = ctk.CTkEntry(self.dynamic_fields, width=400, placeholder_text="Jawaban")
        self.answer_field.pack()
        
        # Configure type change
        self.q_type.trace_add("write", self.update_add_fields)
        
        ctk.CTkButton(self.add_question_frame, text="Tambah", command=self.add_question).pack(pady=10)

    def update_add_fields(self, *args):
        for widget in self.dynamic_fields.winfo_children():
            widget.destroy()
            
        q_type = self.q_type.get()
        
        if q_type == "Essay":
            self.answer_field = ctk.CTkEntry(self.dynamic_fields, width=400, placeholder_text="Jawaban")
            self.answer_field.pack()
            
        elif q_type == "MC":
            self.option1 = ctk.CTkEntry(self.dynamic_fields, placeholder_text="Opsi 1")
            self.option2 = ctk.CTkEntry(self.dynamic_fields, placeholder_text="Opsi 2")
            self.option3 = ctk.CTkEntry(self.dynamic_fields, placeholder_text="Opsi 3")
            self.option4 = ctk.CTkEntry(self.dynamic_fields, placeholder_text="Opsi 4")
            self.correct_option = ctk.CTkEntry(self.dynamic_fields, placeholder_text="Nomor Opsi Benar (1-4)")
            
            for widget in [self.option1, self.option2, self.option3, self.option4, self.correct_option]:
                widget.pack(pady=2)
                
        elif q_type == "TF":
            self.tf_answer = ctk.CTkOptionMenu(self.dynamic_fields, values=["True", "False"])
            self.tf_answer.pack()

    def add_question(self):
        q_type = self.q_type.get().upper()  # Ubah ke uppercase
        question = self.entry_question.get()
        
        if q_type == "ESSAY":
            answer = self.answer_field.get()
            if not question or not answer:
                messagebox.showerror("Error", "Harap isi semua field")
                return
            line = f"ESSAY|{question}|{answer}"

        elif q_type == "MC":
            options = [self.option1.get(), self.option2.get(), self.option3.get(), self.option4.get()]
            correct_input = self.correct_option.get()
    
            # Validate correct option
            if any(not opt for opt in options):
                messagebox.showerror("Error", "Harap isi semua opsi")
                return
            if not correct_input.isdigit():
                messagebox.showerror("Error", "Nomor opsi benar harus angka!")
                return
        
            correct_idx = int(correct_input)
            if correct_idx < 1 or correct_idx > 4:
                messagebox.showerror("Error", "Nomor opsi benar harus antara 1-4!")
                return
         
            # Convert to 0-based index
            correct_idx -= 1
            line = f"MC|{question}|{'|'.join(options)}|{correct_idx}"
            
        elif q_type == "TF":
            answer = self.tf_answer.get()
            line = f"TF|{question}|{answer}"
       
        with open("quiz_questions.txt", "a") as f:
            f.write(line + "\n")
            
        messagebox.showinfo("Success", "Pertanyaan ditambahkan!")
        self.entry_question.delete(0, ctk.END)
        
        # Clear dynamic fields
        for widget in self.dynamic_fields.winfo_children():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, ctk.END)

    def show_questions(self):
        questions = self.read_questions()
        if not questions:
            messagebox.showinfo("Info", "Tidak ada pertanyaan yang tersedia!")
        else:
            questions_text = "\n\n".join(questions)
            messagebox.showinfo("Daftar Pertanyaan", questions_text)

    def show_edit_question(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.edit_question_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.edit_question_frame.pack(expand=True, fill="both")

        ctk.CTkLabel(self.edit_question_frame, text="Edit Pertanyaan", font=("Arial", 16, "bold")).pack(pady=10)

        # Question number input
        self.entry_edit_number = ctk.CTkEntry(self.edit_question_frame, width=400, placeholder_text="Nomor Pertanyaan")
        self.entry_edit_number.pack(pady=5)

        # Load question button
        ctk.CTkButton(self.edit_question_frame, 
                     text="Muat Pertanyaan", 
                     command=self.load_question_for_edit).pack(pady=10)

        # Edit fields container (will be populated dynamically)
        self.edit_fields_container = ctk.CTkFrame(self.edit_question_frame, fg_color="transparent")
        self.edit_fields_container.pack(pady=10)

    def load_question_for_edit(self):
        try:
            question_number = int(self.entry_edit_number.get()) - 1
            questions = self.read_raw_questions()
            
            if 0 <= question_number < len(questions):
                self.current_edit_question = questions[question_number]
                self.populate_edit_fields()
            else:
                messagebox.showerror("Error", "Nomor pertanyaan tidak valid!")
        except ValueError:
            messagebox.showerror("Error", "Masukkan nomor pertanyaan yang valid!")

    def populate_edit_fields(self):
        # Clear previous fields
        for widget in self.edit_fields_container.winfo_children():
            widget.destroy()

        q_type = self.current_edit_question[0]
        question_text = self.current_edit_question[1]

        # Question type selector (disabled in edit mode)
        self.edit_q_type = ctk.StringVar(value=q_type)
        ctk.CTkOptionMenu(self.edit_fields_container, 
                         values=["ESSAY", "MC", "TF"],
                         variable=self.edit_q_type,
                         state="disabled").pack(pady=5)

        # Common question field
        self.edit_question_entry = ctk.CTkEntry(self.edit_fields_container, 
                                              width=400, 
                                              placeholder_text="Pertanyaan")
        self.edit_question_entry.insert(0, question_text)
        self.edit_question_entry.pack(pady=5)

        # Dynamic fields container
        self.edit_dynamic_fields = ctk.CTkFrame(self.edit_fields_container, fg_color="transparent")
        self.edit_dynamic_fields.pack(pady=5)

        # Type-specific fields
        if q_type == "ESSAY":
            self.edit_answer_entry = ctk.CTkEntry(self.edit_dynamic_fields, 
                                                width=400, 
                                                placeholder_text="Jawaban")
            self.edit_answer_entry.insert(0, self.current_edit_question[2])
            self.edit_answer_entry.pack()
            
        elif q_type == "MC":
            options = self.current_edit_question[2:-1]
            correct = str(int(self.current_edit_question[-1]) + 1)  # convert to 1-based
            
            self.edit_options_entries = []
            for i, opt in enumerate(options, 1):
                entry = ctk.CTkEntry(self.edit_dynamic_fields, 
                                   width=400, 
                                   placeholder_text=f"Opsi {i}")
                entry.insert(0, opt)
                entry.pack(pady=2)
                self.edit_options_entries.append(entry)
            
            self.edit_correct_entry = ctk.CTkEntry(self.edit_dynamic_fields, 
                                                 width=400,
                                                 placeholder_text="Nomor Opsi Benar (1-4)")
            self.edit_correct_entry.insert(0, correct)
            self.edit_correct_entry.pack(pady=5)
            
        elif q_type == "TF":
            self.edit_tf_answer = ctk.CTkOptionMenu(self.edit_dynamic_fields, 
                                                  values=["True", "False"])
            self.edit_tf_answer.set(self.current_edit_question[2])
            self.edit_tf_answer.pack()

        # Save button
        ctk.CTkButton(self.edit_fields_container, 
                     text="Simpan Perubahan",
                     width=200,
                     command=self.save_edited_question).pack(pady=10)

    def save_edited_question(self):
        try:
            # Get all questions
            questions = self.read_raw_questions()
            question_number = int(self.entry_edit_number.get()) - 1
            
            # Update question data
            q_type = self.current_edit_question[0]
            new_question = self.edit_question_entry.get()
            
            if q_type == "ESSAY":
                new_answer = self.edit_answer_entry.get()
                if not new_question or not new_answer:
                    messagebox.showerror("Error", "Harap isi semua field")
                    return
                updated = [q_type, new_question, new_answer]
                
            elif q_type == "MC":
                new_options = [entry.get() for entry in self.edit_options_entries]
                new_correct = self.edit_correct_entry.get()
    
                if any(not opt for opt in new_options):
                    messagebox.showerror("Error", "Harap isi semua opsi")
                    return
                if not new_correct.isdigit():
                    messagebox.showerror("Error", "Nomor opsi benar harus angka!")
                    return
        
                correct_idx = int(new_correct)
                if correct_idx < 1 or correct_idx > 4:
                    messagebox.showerror("Error", "Nomor opsi benar harus antara 1-4!")
                    return
        
                correct_idx -= 1
                updated = [q_type, new_question] + new_options + [str(correct_idx)]
                
            elif q_type == "TF":
                new_answer = self.edit_tf_answer.get()
                updated = [q_type, new_question, new_answer]
            
            # Update questions list
            questions[question_number] = updated
            
            # Write back to file
            with open("quiz_questions.txt", "w") as f:
                for q in questions:
                    f.write("|".join(q) + "\n")
            
            messagebox.showinfo("Success", "Pertanyaan berhasil diupdate!")
            self.current_edit_question = None
            
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

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
                    parts = line.strip().split("|")
                    q_type = parts[0].upper()  # Ubah ke uppercase untuk konsistensi
                    
                    if q_type == "ESSAY":
                        questions.append(f"Essay: {parts[1]} (Answer: {parts[2]})")
                    elif q_type == "MC":
                        options = "/".join(parts[2:-1])
                        correct = str(int(parts[-1]) + 1)  # Show 1-based to admin
                        questions.append(f"MC: {parts[1]} [Options: {options}] (Correct: {correct})")
                    elif q_type == "TF":
                        questions.append(f"TF: {parts[1]} (Answer: {parts[2]})")
        return questions

    def read_raw_questions(self):
        questions = []
        if os.path.exists("quiz_questions.txt"):
            with open("quiz_questions.txt", "r") as file:
                for line in file:
                    questions.append(line.strip().split("|"))
        return questions

    def delete_question(self):
        try:
            question_number = int(self.entry_delete.get()) - 1
            questions = self.read_raw_questions()
            if 0 <= question_number < len(questions):
                questions.pop(question_number)
                with open("quiz_questions.txt", "w") as file:
                    for q in questions:
                        file.write("|".join(q) + "\n")
                messagebox.showinfo("Sukses", "Pertanyaan berhasil dihapus!")
            else:
                messagebox.showerror("Error", "Nomor pertanyaan tidak valid!")
        except ValueError:
            messagebox.showerror("Error", "Input harus berupa angka!")

    def show_set_timer(self):
        # New method to configure timer
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.timer_frame = ctk.CTkFrame(self.table_frame)
        self.timer_frame.pack(expand=True, fill="both")

        ctk.CTkLabel(self.timer_frame, text="Set timer quiz (dalam menit)").pack(pady=10)
        
        self.timer_entry = ctk.CTkEntry(self.timer_frame)
        self.timer_entry.pack(pady=5)
        
        ctk.CTkButton(self.timer_frame, text="Save", 
                     command=self.save_timer_config).pack(pady=10)

    def save_timer_config(self):
        try:
            minutes = int(self.timer_entry.get())
            # Enforce 10-hour maximum (600 minutes)
            if minutes > 600:
                minutes = 600
                messagebox.showinfo("Info", "Waktu maksimum timer adalah 10 jam! (600 menit). Timer akan disetel selama 600 menit.")
        
            with open("quiz_settings.txt", "w") as f:
                f.write(f"timer_minutes={minutes}")
            messagebox.showinfo("Success", "Konfigurasi timer berhasil disimpan!")
        except ValueError:
            messagebox.showerror("Error", "Masukan waktu yang valid")

    def back_to_admin(self):
        # Clear all widgets in table frame first
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.dashboard_frame.pack_forget()
        self.admin_frame.pack(expand=True, fill="both")

    def back_to_main(self):
        self.admin_frame.pack_forget()
        self.app.main_frame.pack(expand=True, fill="both")

    def show_upload_question(self):
        """Menampilkan frame upload soal"""
        # Clear all widgets in table frame first
        for widget in self.table_frame.winfo_children():
            widget.destroy()
            
        # Buat frame baru untuk upload
        self.upload_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.upload_frame.pack(expand=True, fill="both")
        
        # Tambahkan judul
        ctk.CTkLabel(self.upload_frame, text="Upload Soal Quiz", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Tambahkan informasi format
        info_frame = ctk.CTkFrame(self.upload_frame, fg_color="#F5F9FF")
        info_frame.pack(padx=20, pady=20, fill="x")
        
        ctk.CTkLabel(
            info_frame,
            text="Format File Soal",
            font=("Arial", 14, "bold"),
            text_color="#1565C0"
        ).pack(pady=5)
        
        formats = [
            ("1. Essay", "ESSAY|Pertanyaan|Jawaban"),
            ("2. Multiple Choice", "MC|Pertanyaan|Opsi1|Opsi2|Opsi3|Opsi4|JawabanBenar(0-3)"),
            ("3. True/False", "TF|Pertanyaan|True/False")
        ]
        
        for title, format_text in formats:
            format_item = ctk.CTkFrame(info_frame, fg_color="#FFFFFF")
            format_item.pack(fill="x", padx=10, pady=2)
            
            ctk.CTkLabel(
                format_item,
                text=title,
                font=("Arial", 12, "bold"),
                text_color="#1976D2"
            ).pack(anchor="w", padx=10, pady=(5,0))
            
            ctk.CTkLabel(
                format_item,
                text=format_text,
                font=("Arial", 11),
                text_color="#424242"
            ).pack(anchor="w", padx=10, pady=(0,5))

        # Tambahkan catatan
        note_frame = ctk.CTkFrame(self.upload_frame, fg_color="#FFF8E1")  # Warna kuning muda
        note_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            note_frame,
            text="Catatan:",
            font=("Arial", 14, "bold"),
            text_color="#F57F17"  # Orange tua
        ).pack(anchor="w", padx=10, pady=(5,0))
        
        notes = [
            "• Format yang sama berlaku untuk file .txt dan .docx",
            "• Setiap soal harus ditulis dalam baris baru",
            "• Gunakan tanda | (pipe) sebagai pemisah",
            "• Untuk MC, jawaban benar adalah indeks opsi (0-3)",
            "• Jangan ada spasi di akhir baris"
        ]
        
        for note in notes:
            ctk.CTkLabel(
                note_frame,
                text=note,
                font=("Arial", 11),
                text_color="#5D4037"  # Cokelat tua
            ).pack(anchor="w", padx=10, pady=1)
        
        # Tambahkan tombol-tombol upload di bagian bawah
        buttons_frame = ctk.CTkFrame(self.upload_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        ctk.CTkButton(
            buttons_frame,
            text="Upload File .txt",
            width=200,
            height=40,
            command=lambda: self.scraper.upload_question_file("txt"),
            fg_color="#2196F3",
            hover_color="#1976D2",
            text_color="#FFFFFF"
        ).pack(pady=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="Upload File .docx",
            width=200,
            height=40,
            command=lambda: self.scraper.upload_question_file("docx"),
            fg_color="#4CAF50",
            hover_color="#388E3C",
            text_color="#FFFFFF"
        ).pack(pady=5)

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Quiz Admin Panel")
    root.geometry("1200x600")
    
    class App:
        def __init__(self, root):
            self.root = root
            self.main_frame = ctk.CTkFrame(root, fg_color="transparent")
            self.main_frame.pack(expand=True, fill="both")
            
    app = App(root)
    admin = Admin(app)
    admin.open_admin_mode()
    root.mainloop()
