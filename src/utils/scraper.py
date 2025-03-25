import os
from tkinter import filedialog, messagebox
import customtkinter as ctk
from docx import Document

class Scraper:
    def __init__(self, app=None):
        if app:
            self.app = app
            self.root = app.root
        else:
            # Jika dijalankan sendiri
            self.root = ctk.CTk()
            self.root.title("Upload Soal Quiz")
            self.root.geometry("800x600")
            self.create_standalone_gui()

    def create_standalone_gui(self):
        """Membuat GUI untuk mode standalone"""
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text="Upload Soal Quiz",
            font=("Arial", 24, "bold"),
            text_color="white"
        ).pack(pady=20)
        
        # Content Frame
        content_frame = ctk.CTkFrame(main_frame, fg_color="#333333")
        content_frame.pack(expand=True, fill="both", pady=10)
        
        # Format Info Frame
        format_frame = ctk.CTkFrame(content_frame, fg_color="#2b2b2b")
        format_frame.pack(padx=20, pady=20, fill="x")
        
        ctk.CTkLabel(
            format_frame,
            text="Format File Soal",
            font=("Arial", 18, "bold"),
            text_color="#4CAF50"
        ).pack(pady=10)
        
        formats = [
            ("1. Essay", "ESSAY|Pertanyaan|Jawaban"),
            ("2. Multiple Choice", "MC|Pertanyaan|Opsi1|Opsi2|Opsi3|Opsi4|JawabanBenar(0-3)"),
            ("3. True/False", "TF|Pertanyaan|True/False")
        ]
        
        for title, format_text in formats:
            format_item = ctk.CTkFrame(format_frame, fg_color="#333333")
            format_item.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(
                format_item,
                text=title,
                font=("Arial", 14, "bold"),
                text_color="#90CAF9"
            ).pack(anchor="w", padx=10, pady=(5,0))
            
            ctk.CTkLabel(
                format_item,
                text=format_text,
                font=("Arial", 12),
                text_color="#E0E0E0"
            ).pack(anchor="w", padx=10, pady=(0,5))
        
        # Note
        note_frame = ctk.CTkFrame(content_frame, fg_color="#2b2b2b")
        note_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            note_frame,
            text="Catatan:",
            font=("Arial", 14, "bold"),
            text_color="#FFA726"
        ).pack(anchor="w", padx=10, pady=(5,0))
        
        ctk.CTkLabel(
            note_frame,
            text="• Format yang sama berlaku untuk file .txt dan .docx\n"
                 "• Setiap soal harus ditulis dalam baris baru\n"
                 "• Gunakan tanda | (pipe) sebagai pemisah\n"
                 "• Untuk MC, jawaban benar adalah indeks opsi (0-3)\n"
                 "• Jangan ada spasi di akhir baris",
            font=("Arial", 12),
            text_color="#E0E0E0"
        ).pack(anchor="w", padx=10, pady=(0,5))
        
        # Buttons Frame
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        ctk.CTkButton(
            buttons_frame,
            text="Upload File .txt",
            width=200,
            height=40,
            command=lambda: self.upload_question_file("txt"),
            fg_color="#4CAF50",
            hover_color="#388E3C"
        ).pack(pady=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="Upload File .docx",
            width=200,
            height=40,
            command=lambda: self.upload_question_file("docx"),
            fg_color="#2196F3",
            hover_color="#1976D2"
        ).pack(pady=5)

    def create_upload_frame(self, parent_frame):
        """Membuat frame untuk fitur upload soal (untuk mode terintegrasi)"""
        upload_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.create_standalone_gui()
        return upload_frame

    def read_docx_file(self, file_path):
        """Membaca soal dari file docx"""
        doc = Document(file_path)
        questions = []
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if text:  # Skip paragraf kosong
                questions.append(text)
        return questions

    def upload_question_file(self, file_type="txt"):
        """Mengunggah dan memvalidasi file soal"""
        filetypes = [("Text files", "*.txt")] if file_type == "txt" else [("Word files", "*.docx")]
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        if not file_path:
            return
        
        try:
            if file_type == "txt":
                with open(file_path, "r", encoding="utf-8") as file:
                    questions = file.readlines()
            else:  # docx
                questions = self.read_docx_file(file_path)
            
            if not questions:
                messagebox.showerror("Error", "File kosong! Harap unggah file dengan format yang benar.")
                return
            
            # Validasi format soal
            valid_questions = []
            for line_num, line in enumerate(questions, 1):
                line = line.strip()
                if not line:  # Skip baris kosong
                    continue
                    
                parts = line.split("|")
                q_type = parts[0].upper() if parts else ""
                
                if q_type == "ESSAY":
                    if len(parts) != 3:
                        messagebox.showerror("Error", f"Format soal Essay salah pada baris {line_num}.\nFormat: ESSAY|Pertanyaan|Jawaban")
                        return
                elif q_type == "MC":
                    if len(parts) != 7:
                        messagebox.showerror("Error", f"Format soal Multiple Choice salah pada baris {line_num}.\nFormat: MC|Pertanyaan|Opsi1|Opsi2|Opsi3|Opsi4|JawabanBenar(0-3)")
                        return
                    # Validasi jawaban MC harus 0-3
                    try:
                        answer_idx = int(parts[6])
                        if answer_idx < 0 or answer_idx > 3:
                            messagebox.showerror("Error", f"Jawaban MC pada baris {line_num} harus antara 0-3")
                            return
                    except ValueError:
                        messagebox.showerror("Error", f"Jawaban MC pada baris {line_num} harus berupa angka")
                        return
                elif q_type == "TF":
                    if len(parts) != 3 or parts[2].upper() not in ["TRUE", "FALSE"]:
                        messagebox.showerror("Error", f"Format soal True/False salah pada baris {line_num}.\nFormat: TF|Pertanyaan|True/False")
                        return
                else:
                    messagebox.showerror("Error", f"Tipe soal tidak valid pada baris {line_num}.\nTipe yang didukung: ESSAY, MC, TF")
                    return
                    
                valid_questions.append(line)
            
            # Simpan soal yang valid
            with open("quiz_questions.txt", "w", encoding="utf-8") as quiz_file:
                for question in valid_questions:
                    quiz_file.write(question + "\n")
            
            messagebox.showinfo("Sukses", f"{len(valid_questions)} soal berhasil diunggah!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def get_questions(self):
        """Mengambil soal dari file quiz_questions.txt"""
        questions = []
        if os.path.exists("quiz_questions.txt"):
            with open("quiz_questions.txt", "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split("|")
                    if len(parts) >= 3:  # Minimal harus ada tipe, pertanyaan, dan jawaban
                        q_type = parts[0].upper()
                        question = parts[1]
                        
                        if q_type == "ESSAY":
                            answer = parts[2]
                            questions.append({
                                "type": "Essay",
                                "question": question,
                                "answer": answer
                            })
                        elif q_type == "MC":
                            options = parts[2:6]
                            answer = parts[6]
                            questions.append({
                                "type": "MC",
                                "question": question,
                                "options": options,
                                "answer": answer
                            })
                        elif q_type == "TF":
                            answer = parts[2]
                            questions.append({
                                "type": "TF",
                                "question": question,
                                "answer": answer
                            })
                        
        return questions

if __name__ == "__main__":
    # Set tema aplikasi
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Jalankan aplikasi
    app = Scraper()
    app.root.mainloop()
    
