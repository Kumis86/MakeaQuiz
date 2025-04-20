import customtkinter as ctk
from tkinter import messagebox, ttk
import os
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg            
from src.utils.scraper import Scraper
from src.core.questions import EssayQuestion, MCQuestion, TFQuestion
from src.ui.dashboard import Dashboard
from src.core.user import search_user

ADMIN_PASSWORD = "admin123"

class Admin:
    def __init__(self, app, show_login_callback):
        self.app = app
        self.show_login_callback = show_login_callback
        self.current_edit_question = None
        self.scraper = Scraper(self.app.window)
        self.dashboard_instance = None
        os.makedirs("database", exist_ok=True)
        self.users_list = []
        self.user_management_frame = None

    def open_admin_mode(self):
        self.app.main_frame.pack_forget()

    def open_dashboard(self):
        admin_callbacks = {
            "show_leaderboard": self.show_leaderboard,
            "show_active_users": self.show_active_users,
            "show_upload_question": self.show_upload_question,
            "show_add_question": self.show_add_question,
            "show_questions": self.show_questions,
            "show_edit_question": self.show_edit_question,
            "show_delete_question": self.show_delete_question,
            "show_set_timer": self.show_set_timer,
            "show_user_management": self.show_user_management,
            "show_search_question": self.show_search_question,
            "show_search_user": self.show_search_user_screen
        }

        self.dashboard_instance = Dashboard(
            parent=self.app.window,
            logout_callback=self.handle_dashboard_logout,
            is_admin=True,
            callbacks=admin_callbacks
        )

        self.show_active_users()

    def _clear_content_area(self):
        if self.dashboard_instance and self.dashboard_instance.content_area:
            for widget in self.dashboard_instance.content_area.winfo_children():
                widget.destroy()

    def show_active_users(self):
        self._clear_content_area()
        target_frame = self.dashboard_instance.content_area

        if os.path.exists("database/user.txt"):
            with open("database/user.txt", "r") as file:
                users = [line.strip().split(",")[0] for line in file.readlines()]
        else:
            users = []

        columns = ("#1", "#2")
        table = ttk.Treeview(target_frame, columns=columns, show="headings")
        table.heading("#1", text="Username")
        table.heading("#2", text="Status")

        for user in users:
            table.insert("", "end", values=(user, "Active"))

        table.pack(expand=True, fill="both", padx=20, pady=20)

    def show_leaderboard(self):
        self._clear_content_area()
        target_frame = self.dashboard_instance.content_area

        # Read and categorize leaderboard data with proper mode mapping
        leaderboard_data = {"MC": [], "TF": [], "ESSAY": []}
        leaderboard_file = "database/leaderboard.txt"
        
        # Mode translation dictionary
        mode_mapping = {
            "Pilihan Ganda": "MC",
            "True/False": "TF",
            "Essay": "ESSAY"
        }

        if os.path.exists(leaderboard_file):
            try:
                with open(leaderboard_file, "r") as file:
                    for line in file:
                        if line.strip():
                            parts = line.strip().split("|")
                            if len(parts) >= 4:
                                try:
                                    raw_mode = parts[3].strip()
                                    quiz_type = mode_mapping.get(raw_mode, None)
                                    
                                    if not quiz_type:
                                        continue  # Skip unknown types
                                        
                                    entry = {
                                        "username": parts[0],
                                        "score": int(parts[1]),
                                        "total_q": parts[2],
                                        "mode": quiz_type
                                    }
                                    leaderboard_data[quiz_type].append(entry)
                                except (ValueError, IndexError) as e:
                                    print(f"Skipping invalid line: {line.strip()} - {str(e)}")
            except Exception as e:
                print(f"Error reading leaderboard file: {e}")
                messagebox.showerror("Error", f"Failed to read leaderboard file: {e}")

        # Sort each category by score descending
        for category in leaderboard_data:
            leaderboard_data[category].sort(key=lambda x: x['score'], reverse=True)

        # Figure tracking
        self.current_figure = None

        # Create main container
        main_container = ctk.CTkFrame(target_frame)
        main_container.pack(expand=True, fill="both")

        # Category selector with translated labels
        category_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        category_frame.pack(pady=10, fill="x")
        
        self.current_category = ctk.StringVar(value="MC")
        category_selector = ctk.CTkSegmentedButton(
            category_frame,
            values=["MC", "TF", "ESSAY"],
            variable=self.current_category,
            command=lambda _: self._update_leaderboard_display(leaderboard_data),
        )
        category_selector.pack(padx=20, pady=5)

        # Table and graph container
        content_container = ctk.CTkFrame(main_container)
        content_container.pack(expand=True, fill="both")
        content_container.grid_rowconfigure(0, weight=3)
        content_container.grid_rowconfigure(1, weight=1)
        content_container.grid_columnconfigure(0, weight=1)

        # Create frames
        self.table_frame = ctk.CTkFrame(content_container)
        self.table_frame.grid(row=0, column=0, sticky="nsew")
        
        self.graph_frame = ctk.CTkFrame(content_container)
        self.graph_frame.grid(row=1, column=0, sticky="nsew")

        # Initial display
        self._update_leaderboard_display(leaderboard_data)

    def _update_leaderboard_display(self, leaderboard_data):
        # Clear previous widgets and figures 
        if hasattr(self, 'current_figure') and self.current_figure:
            plt.close(self.current_figure)

        for widget in self.table_frame.winfo_children():
            widget.destroy()
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        category = self.current_category.get()
        raw_data = leaderboard_data.get(category, [])
        
        # Process data for display - keep all entries sorted
        sorted_data = sorted(raw_data, key=lambda x: x['score'], reverse=True)
        table_data = sorted_data  # All data for table
        graph_data = sorted_data[:10]  # Top 10 for graph

        # Create table with attempt numbers
        columns = ("#1", "#2", "#3", "#4", "#5")
        table = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        
        # Configure columns
        table.heading("#1", text="Peringkat")
        table.heading("#2", text="Username")
        table.heading("#3", text="Skor")
        table.heading("#4", text="Total Soal")
        table.heading("#5", text="Attempt #")
        
        # Track attempts per user for numbering
        attempt_counts = defaultdict(int)
        
        # Populate table with ALL attempts
        for i, entry in enumerate(table_data):
            attempt_counts[entry['username']] += 1
            values = (
                i + 1,
                entry['username'],
                f"{entry['score']}/{entry['total_q']}",
                entry['total_q'],
                attempt_counts[entry['username']]
            )
            table.insert("", "end", values=values)

        table.pack(expand=True, fill="both", padx=20, pady=20)

        # Create graph with top 10 attempts
        try:
            self.current_figure, ax = plt.subplots(figsize=(8, 3.5))   
            self.current_figure.patch.set_facecolor('#2B2B2B')
            ax.set_facecolor('#2B2B2B')    
            
            if graph_data:
                # Create labels with attempt numbers
                labels = [f"{entry['username']} (#{i+1})" 
                        for i, entry in enumerate(graph_data)]
                scores = [entry['score'] for entry in graph_data]
                
                bars = ax.bar(labels, scores, color='#6357B1')
                ax.set_title(f"Top 10 Skor {self._translate_category(category)}", 
                           color='white', pad=15, fontsize=12)
                ax.set_ylabel('Skor', color='white', fontsize=10)
                ax.tick_params(axis='both', colors='white', labelsize=8)
                plt.xticks(rotation=45, ha='right', fontsize=8)
                
                # Add value labels
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'{height}', ha='center', va='bottom',
                            color='white', fontsize=8)
            else:
                ax.text(0.5, 0.5, 'Tidak ada data untuk kategori ini',
                      ha='center', va='center', 
                      color='white', fontsize=10)

            plt.tight_layout()
            
            # Embed graph
            canvas = FigureCanvasTkAgg(self.current_figure, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=10)
            
        except ImportError:
            error_label = ctk.CTkLabel(self.graph_frame, 
                                     text="Install matplotlib: 'pip install matplotlib'",
                                     text_color="#FF5555")
            error_label.pack(pady=20)

    def _translate_category(self, category):
        translations = {
            "MC": "Pilihan Ganda",
            "TF": "True/False",
            "ESSAY": "Essay"
        }
        return translations.get(category, category)

    def show_add_question(self):
        self._clear_content_area()
        target_frame = self.dashboard_instance.content_area

        # --- Frame utama untuk form tambah --- 
        # Beri padding pada frame utama ini, bukan pada pack widget individual
        form_frame = ctk.CTkFrame(target_frame, fg_color="transparent")
        form_frame.pack(expand=True, fill="both", padx=40, pady=30) # <<< Padding lebih besar

        ctk.CTkLabel(form_frame, text="Tambah Pertanyaan Baru", font=("Inter Bold", 24)).pack(pady=(0, 20), anchor="w") # <<< Font lebih besar, rata kiri

        # --- Frame untuk input --- 
        input_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        input_container.pack(fill="x", expand=True)

        # Tipe Pertanyaan
        type_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        type_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(type_frame, text="Tipe Pertanyaan:", font=("Inter", 16)).pack(side="left", padx=(0, 10))
        self.q_type = ctk.StringVar(value="Essay")
        q_type_menu = ctk.CTkOptionMenu(
            type_frame, 
                        values=["Essay", "MC", "TF"],
            variable=self.q_type,
            font=("Inter", 14) # <<< Sesuaikan font jika perlu
        )
        q_type_menu.pack(side="left", fill="x", expand=True)
        self.q_type.trace_add("write", self._update_add_fields) # Pindahkan trace ke sini

        # Input Pertanyaan (memenuhi lebar)
        ctk.CTkLabel(input_container, text="Teks Pertanyaan:", font=("Inter", 16)).pack(anchor="w", pady=(10, 0))
        self.entry_question = ctk.CTkEntry(
            input_container, 
            # width=400, # <<< Hapus width agar fill='x'
            height=40, 
            font=("Inter", 14),
            placeholder_text="Masukkan teks pertanyaan..."
        )
        self.entry_question.pack(fill="x", pady=5)

        # --- Kontainer untuk field dinamis (jawaban/opsi) --- 
        ctk.CTkLabel(input_container, text="Jawaban / Opsi:", font=("Inter", 16)).pack(anchor="w", pady=(10, 0))
        self.dynamic_fields = ctk.CTkFrame(input_container, fg_color="#1E1E1E", corner_radius=10) # <<< Beri latar belakang & radius
        self.dynamic_fields.pack(fill="both", expand=True, pady=5, ipady=10)
        
        # Panggil _update_add_fields untuk menampilkan field awal (Essay)
        self._update_add_fields()
        
        # Tombol Tambah (lebih besar dan di bawah)
        add_button = ctk.CTkButton(
            form_frame, 
            text="Tambah Pertanyaan ke Database", 
            font=("Inter Bold", 16),
            height=50, # <<< Tinggikan tombol
            fg_color="#6357B1", 
            hover_color="#4F44A3",
            command=self.add_question
        )
        add_button.pack(pady=(30, 0), fill='x') # <<< Fill x

    def _update_add_fields(self, *args):
        """Updates the fields in the dynamic_fields container based on q_type."""
        # Pastikan dynamic_fields ada sebelum diakses
        if not hasattr(self, 'dynamic_fields') or not self.dynamic_fields.winfo_exists():
            return
            
        for widget in self.dynamic_fields.winfo_children():
            widget.destroy()
            
        q_type = self.q_type.get()
        
        # Gunakan padding internal untuk frame dynamic_fields
        padx_dynamic = 20
        pady_dynamic = 10
        
        if q_type == "Essay":
            ctk.CTkLabel(self.dynamic_fields, text="Jawaban Essay:", font=("Inter", 14)).pack(anchor="w", padx=padx_dynamic, pady=(pady_dynamic,0))
            self.answer_field = ctk.CTkEntry(
                 self.dynamic_fields, 
                 # width=400, # Hapus width
                 height=40,
                 font=("Inter", 14),
                 placeholder_text="Masukkan jawaban benar untuk essay..."
            )
            self.answer_field.pack(fill="x", padx=padx_dynamic, pady=(0, pady_dynamic))
            
        elif q_type == "MC":
            ctk.CTkLabel(self.dynamic_fields, text="Opsi Jawaban (Minimal 2):", font=("Inter", 14)).pack(anchor="w", padx=padx_dynamic, pady=(pady_dynamic,0))
            options_frame = ctk.CTkFrame(self.dynamic_fields, fg_color="transparent")
            options_frame.pack(fill="x", padx=padx_dynamic)
            
            self.option1 = ctk.CTkEntry(options_frame, placeholder_text="Opsi 1", height=35, font=("Inter", 14))
            self.option2 = ctk.CTkEntry(options_frame, placeholder_text="Opsi 2", height=35, font=("Inter", 14))
            self.option3 = ctk.CTkEntry(options_frame, placeholder_text="Opsi 3", height=35, font=("Inter", 14))
            self.option4 = ctk.CTkEntry(options_frame, placeholder_text="Opsi 4", height=35, font=("Inter", 14))
            
            self.option1.pack(fill="x", pady=2)
            self.option2.pack(fill="x", pady=2)
            self.option3.pack(fill="x", pady=2)
            self.option4.pack(fill="x", pady=2)

            ctk.CTkLabel(self.dynamic_fields, text="Nomor Opsi Jawaban Benar:", font=("Inter", 14)).pack(anchor="w", padx=padx_dynamic, pady=(pady_dynamic,0))
            self.correct_option = ctk.CTkEntry(
                 self.dynamic_fields, 
                 placeholder_text="Masukkan nomor opsi yang benar (1-4)",
                 height=35,
                 font=("Inter", 14)
            )
            self.correct_option.pack(fill="x", padx=padx_dynamic, pady=(0, pady_dynamic))
                
        elif q_type == "TF":
             ctk.CTkLabel(self.dynamic_fields, text="Jawaban Benar:", font=("Inter", 14)).pack(anchor="w", padx=padx_dynamic, pady=(pady_dynamic,0))
             self.tf_answer = ctk.CTkOptionMenu(
                 self.dynamic_fields, 
                 values=["True", "False"], 
                 font=("Inter", 14),
                 height=35,
                 anchor="center"
             )
             self.tf_answer.pack(fill="x", padx=padx_dynamic, pady=(0, pady_dynamic))

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
       
        try:
            with open("database/quiz_questions.txt", "a") as f:
                f.write(line + "\n")
            
            messagebox.showinfo("Success", "Pertanyaan ditambahkan!")
            # Bersihkan field utama
            self.entry_question.delete(0, ctk.END)
            
            # Bersihkan field dinamis setelah sukses
            if hasattr(self, 'dynamic_fields'): # Cek jika dynamic_fields ada
                for widget in self.dynamic_fields.winfo_children():
                    if isinstance(widget, ctk.CTkEntry):
                        widget.delete(0, ctk.END)
                    elif isinstance(widget, ctk.CTkOptionMenu): # Reset OptionMenu
                         if q_type == "TF": self.tf_answer.set("True") # Reset ke default
                         # Tidak perlu reset MC OptionMenu karena tidak pakai StringVar
            
            # Panggil callback pembersihan jika ada (konsisten dgn add_question lama)
            if hasattr(self, 'clear_add_fields_callback') and callable(self.clear_add_fields_callback):
                 self.clear_add_fields_callback()
                 
        except Exception as e:
            print(f"Error adding question: {e}")
            messagebox.showerror("Error Penyimpanan", f"Gagal menyimpan pertanyaan ke file: {e}")

    def show_questions(self):
        questions = self.read_questions()
        if not questions:
            messagebox.showinfo("Info", "Tidak ada pertanyaan yang tersedia!")
        else:
            questions_text = "\n\n".join(questions)
            messagebox.showinfo("Daftar Pertanyaan", questions_text)

    def show_edit_question(self):
        self._clear_content_area()
        target_frame = self.dashboard_instance.content_area

        # --- Frame utama untuk form edit --- 
        edit_main_frame = ctk.CTkFrame(target_frame, fg_color="transparent")
        edit_main_frame.pack(expand=True, fill="both", padx=40, pady=30)

        ctk.CTkLabel(edit_main_frame, text="Edit Pertanyaan", font=("Inter Bold", 24)).pack(pady=(0, 20), anchor="w")

        # --- Frame untuk memuat pertanyaan --- 
        load_frame = ctk.CTkFrame(edit_main_frame, fg_color="transparent")
        load_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(load_frame, text="Masukkan Nomor Pertanyaan yang Akan Diedit:", font=("Inter", 16)).pack(side="left", padx=(0, 10))
        self.entry_edit_number = ctk.CTkEntry(
            load_frame, 
            # width=400, # Hapus width
            height=40, 
            font=("Inter", 14),
            placeholder_text="Nomor"
        )
        self.entry_edit_number.pack(side="left", fill="x", expand=True, padx=5)

        load_button = ctk.CTkButton(
            load_frame, 
                     text="Muat Pertanyaan", 
            font=("Inter Bold", 14), # <<< Sesuaikan font
            height=40, # <<< Samakan tinggi dengan entry
            fg_color="#6357B1", 
            hover_color="#4F44A3",
            command=self.load_question_for_edit
        )
        load_button.pack(side="left", padx=5)

        # --- Kontainer untuk field edit (akan diisi setelah load) --- 
        self.edit_fields_container = ctk.CTkFrame(edit_main_frame, fg_color="#1E1E1E", corner_radius=10)
        self.edit_fields_container.pack(fill="both", expand=True, pady=20, ipady=10)
        # Tampilkan pesan awal di kontainer
        ctk.CTkLabel(self.edit_fields_container, text="Muat pertanyaan untuk melihat detailnya di sini.", font=("Inter", 14), text_color="gray").pack(pady=50)

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
        """Populates the edit_fields_container with the loaded question data."""
        if not self.edit_fields_container.winfo_exists():
            return 
            
        for widget in self.edit_fields_container.winfo_children():
            widget.destroy()
            
        if not self.current_edit_question:
             ctk.CTkLabel(self.edit_fields_container, text="Gagal memuat data pertanyaan.", font=("Inter", 14), text_color="red").pack(pady=50)
             return

        q_type = self.current_edit_question[0]
        question_text = self.current_edit_question[1]

        # Gunakan padding internal
        padx_edit = 20
        pady_edit = 10

        # Tampilkan Tipe (disabled)
        type_frame_edit = ctk.CTkFrame(self.edit_fields_container, fg_color="transparent")
        type_frame_edit.pack(fill="x", padx=padx_edit, pady=(pady_edit, 5))
        ctk.CTkLabel(type_frame_edit, text="Tipe Pertanyaan:", font=("Inter", 16)).pack(side="left", padx=(0, 10))
        self.edit_q_type = ctk.StringVar(value=q_type)
        q_type_menu_edit = ctk.CTkOptionMenu(
            type_frame_edit, 
            values=[q_type], # Hanya tampilkan tipe saat ini
                         variable=self.edit_q_type,
            state="disabled",
            font=("Inter", 14),
            height=35
        )
        q_type_menu_edit.pack(side="left", fill="x", expand=True)

        # Input Teks Pertanyaan
        ctk.CTkLabel(self.edit_fields_container, text="Teks Pertanyaan:", font=("Inter", 16)).pack(anchor="w", padx=padx_edit, pady=(pady_edit, 0))
        self.edit_question_entry = ctk.CTkEntry(
            self.edit_fields_container, 
            # width=400, # Hapus width
            height=40,
            font=("Inter", 14)
        )
        self.edit_question_entry.insert(0, question_text)
        self.edit_question_entry.pack(fill="x", padx=padx_edit, pady=(0, pady_edit))

        # --- Kontainer untuk field jawaban/opsi dinamis --- 
        ctk.CTkLabel(self.edit_fields_container, text="Jawaban / Opsi:", font=("Inter", 16)).pack(anchor="w", padx=padx_edit, pady=(pady_edit, 0))
        self.edit_dynamic_fields = ctk.CTkFrame(self.edit_fields_container, fg_color="transparent") # Tidak perlu background lagi
        self.edit_dynamic_fields.pack(fill="x", expand=True, padx=padx_edit, pady=(0, pady_edit))

        # Isi field sesuai tipe
        if q_type == "ESSAY":
            self.edit_answer_entry = ctk.CTkEntry(self.edit_dynamic_fields, height=40, font=("Inter", 14))
            self.edit_answer_entry.insert(0, self.current_edit_question[2])
            self.edit_answer_entry.pack(fill="x")
            
        elif q_type == "MC":
            options = self.current_edit_question[2:-1]
            correct = str(int(self.current_edit_question[-1]) + 1) # 1-based
            
            self.edit_options_entries = []
            mc_options_frame = ctk.CTkFrame(self.edit_dynamic_fields, fg_color="transparent")
            mc_options_frame.pack(fill="x")
            for i, opt in enumerate(options):
                entry = ctk.CTkEntry(mc_options_frame, height=35, font=("Inter", 14))
                entry.insert(0, opt)
                entry.pack(fill="x", pady=2)
                self.edit_options_entries.append(entry)
            
            ctk.CTkLabel(self.edit_dynamic_fields, text="Nomor Opsi Benar (1-{}):".format(len(options)), font=("Inter", 14)).pack(anchor="w", pady=(pady_edit,0))
            self.edit_correct_entry = ctk.CTkEntry(self.edit_dynamic_fields, height=35, font=("Inter", 14))
            self.edit_correct_entry.insert(0, correct)
            self.edit_correct_entry.pack(fill="x")
            
        elif q_type == "TF":
            self.edit_tf_answer = ctk.CTkOptionMenu(
                 self.edit_dynamic_fields, 
                 values=["True", "False"], 
                 height=35, 
                 font=("Inter", 14),
                 anchor="center"
            )
            self.edit_tf_answer.set(str(self.current_edit_question[2])) # Set nilai awal
            self.edit_tf_answer.pack(fill="x")

        # Tombol Simpan
        save_button = ctk.CTkButton(
             self.edit_fields_container, # <<< Letakkan di dalam container field
                     text="Simpan Perubahan",
             font=("Inter Bold", 16),
             height=50, # <<< Tinggikan tombol
             fg_color="#4CAF50", # Warna hijau untuk simpan
             hover_color="#388E3C",
             command=self.save_edited_question
        )
        save_button.pack(pady=(30, 0), fill='x') # <<< Fill x di paling bawah container edit

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
            with open("database/quiz_questions.txt", "w") as f:
                for q in questions:
                    f.write("|".join(q) + "\n")
            
            messagebox.showinfo("Success", "Pertanyaan berhasil diupdate!")
            self.current_edit_question = None
            
        except Exception as e:
            print(f"Error saving edited question: {e}")
            messagebox.showerror("Error Penyimpanan", f"Gagal menyimpan perubahan pertanyaan ke file: {e}")

    def show_delete_question(self):
        self._clear_content_area()
        target_frame = self.dashboard_instance.content_area

        # --- Frame utama untuk form hapus --- 
        delete_main_frame = ctk.CTkFrame(target_frame, fg_color="transparent")
        delete_main_frame.pack(expand=True, fill="both", padx=40, pady=30)

        ctk.CTkLabel(delete_main_frame, text="Hapus Pertanyaan", font=("Inter Bold", 24)).pack(pady=(0, 20), anchor="w")
        
        ctk.CTkLabel(delete_main_frame, text="Masukkan Nomor Pertanyaan yang Akan Dihapus:", font=("Inter", 16)).pack(anchor="w", pady=(10,0))
        self.entry_delete_number = ctk.CTkEntry(
            delete_main_frame, 
            # width=400, # Hapus width
            height=40,
            font=("Inter", 14),
            placeholder_text="Nomor Pertanyaan"
        )
        self.entry_delete_number.pack(fill="x", pady=5)

        delete_button = ctk.CTkButton(
            delete_main_frame,
            text="Hapus Pertanyaan Ini",
            font=("Inter Bold", 16),
            height=50, # <<< Tinggikan tombol
            fg_color="#E74C3C", # Warna merah untuk hapus
            hover_color="#C0392B",
            command=self.delete_question
        )
        delete_button.pack(pady=(30, 0), fill='x') # <<< Fill x

    def read_questions(self, keyword=None):
        questions = []
        if os.path.exists("database/quiz_questions.txt"):
            with open("database/quiz_questions.txt", "r") as file:
                for line in file:
                    parts = line.strip().split("|")
                    q_type = parts[0].upper()  # Ubah ke uppercase untuk konsistensi
                    question_text = parts[1].lower()
                    
                    if keyword and keyword not in question_text:
                        continue

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
        if os.path.exists("database/quiz_questions.txt"):
            with open("database/quiz_questions.txt", "r") as file:
                for line in file:
                    questions.append(line.strip().split("|"))
        return questions

    def delete_question(self):
        try:
            question_number = int(self.entry_delete_number.get()) - 1
            questions = self.read_raw_questions()
            if 0 <= question_number < len(questions):
                questions.pop(question_number)
                with open("database/quiz_questions.txt", "w") as file:
                    for q in questions:
                        file.write("|".join(q) + "\n")
                messagebox.showinfo("Sukses", "Pertanyaan berhasil dihapus!")
            else:
                messagebox.showerror("Error", "Nomor pertanyaan tidak valid!")
        except ValueError:
            messagebox.showerror("Error", "Input harus berupa angka!")

    def show_set_timer(self):
        self._clear_content_area()
        target_frame = self.dashboard_instance.content_area

        # --- Frame utama untuk set timer --- 
        timer_main_frame = ctk.CTkFrame(target_frame, fg_color="transparent")
        timer_main_frame.pack(expand=True, fill="both", padx=40, pady=30)

        ctk.CTkLabel(timer_main_frame, text="Set Timer Kuis", font=("Inter Bold", 24)).pack(pady=(0, 20), anchor="w")

        ctk.CTkLabel(timer_main_frame, text="Masukkan Durasi Timer (dalam detik):", font=("Inter", 16)).pack(anchor="w", pady=(10,0))
        self.timer_entry = ctk.CTkEntry(
            timer_main_frame,
            height=40,
            font=("Inter", 14),
            placeholder_text="Contoh: 1800 untuk 30 menit"
        )
        self.timer_entry.pack(fill="x", pady=5)

        save_timer_button = ctk.CTkButton(
            timer_main_frame,
            text="Simpan Timer",
            font=("Inter Bold", 16),
            height=50,
            fg_color="#6357B1",
            hover_color="#4F44A3",
            command=self.save_timer_config
        )
        save_timer_button.pack(pady=(30, 0), fill='x')

    def save_timer_config(self):
        try:
            minutes = int(self.timer_entry.get())
            # Enforce 10-hour maximum (600 minutes)
            if minutes > 600:
                minutes = 600
                messagebox.showinfo("Info", "Waktu maksimum timer adalah 10 jam! (600 menit). Timer akan disetel selama 600 menit.")
        
            with open("database/quiz_settings.txt", "w") as f:
                f.write(f"timer_minutes={minutes}")
            messagebox.showinfo("Success", "Konfigurasi timer berhasil disimpan!")
        except ValueError:
            messagebox.showerror("Error", "Masukan waktu yang valid")

    def show_upload_question(self):
        self._clear_content_area()
        target_frame = self.dashboard_instance.content_area

        # --- Frame utama untuk upload --- 
        upload_main_frame = ctk.CTkFrame(target_frame, fg_color="transparent")
        upload_main_frame.pack(expand=True, fill="both", padx=40, pady=30)

        ctk.CTkLabel(upload_main_frame, text="Upload Soal dari File", font=("Inter Bold", 24)).pack(pady=(0, 20), anchor="w")

        # --- Frame untuk informasi format --- 
        info_frame = ctk.CTkFrame(upload_main_frame, fg_color="#1E1E1E", corner_radius=10)
        info_frame.pack(fill='x', pady=10)
        
        ctk.CTkLabel(info_frame, text="Format File Soal (.txt atau .docx)", font=("Inter Bold", 16), text_color="#FFFFFF").pack(pady=10, padx=20, anchor="w")
        
        format_text = ( "ESSAY|Pertanyaan|Jawaban\n"
                        "MC|Pertanyaan|Opsi1|Opsi2|Opsi3|Opsi4|JawabanBenar(0-3)\n"
                        "TF|Pertanyaan|True/False\n\n"
                        "Catatan:\n"
                        "- Setiap soal harus dalam baris baru.\n"
                        "- Gunakan tanda | (pipe) sebagai pemisah.\n"
                        "- Untuk MC, jawaban benar adalah indeks opsi (dimulai dari 0).\n"
                        "- Jangan ada spasi ekstra di awal/akhir baris."
                       )
        
        ctk.CTkLabel(info_frame, text=format_text, font=("Inter", 13), justify="left", anchor="w", wraplength=target_frame.winfo_width()-100).pack(pady=10, padx=20, anchor="w") # <<< Wraplength

        # --- Frame untuk tombol upload --- 
        buttons_frame = ctk.CTkFrame(upload_main_frame, fg_color="transparent")
        buttons_frame.pack(pady=20, fill='x')
        
        upload_txt_button = ctk.CTkButton(
            buttons_frame,
            text="Upload File .txt",
            font=("Inter Bold", 16),
            height=50,
            fg_color="#6357B1",
            hover_color="#4F44A3",
            command=lambda: self.scraper.upload_question_file("txt")
        )
        upload_txt_button.pack(side="left", padx=10, expand=True, fill='x')
        
        upload_docx_button = ctk.CTkButton(
            buttons_frame,
            text="Upload File .docx",
            font=("Inter Bold", 16),
            height=50,
            fg_color="#6357B1",
            hover_color="#4F44A3",
            command=lambda: self.scraper.upload_question_file("docx")
        )
        upload_docx_button.pack(side="left", padx=10, expand=True, fill='x')

    def handle_dashboard_logout(self):
        if self.dashboard_instance:
            # Cleanup matplotlib figures
            if hasattr(self, 'current_figure') and self.current_figure:
                plt.close(self.current_figure)
                self.current_figure = None
            self.dashboard_instance.destroy()
            self.dashboard_instance = None
        self.show_login_callback()

    def back_to_main(self):
        if self.dashboard_instance:
            self.dashboard_instance.destroy()
            self.dashboard_instance = None
            if hasattr(self.app, 'navigate_to_main_screen'):
                self.app.navigate_to_main_screen()
        else:
             if hasattr(self.app, 'main_frame'):
                 self.app.main_frame.pack(expand=True, fill="both")

    def show_user_management(self):
        self._clear_content_area()
        target_frame = self.dashboard_instance.content_area

        self.user_management_frame = ctk.CTkFrame(target_frame, fg_color="transparent")
        self.user_management_frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(self.user_management_frame, text="Manajemen Pengguna Terdaftar", font=("Inter Bold", 24)).pack(pady=(0, 20), anchor="w")

        # Frame untuk tabel dan scrollbar
        table_container = ctk.CTkFrame(self.user_management_frame)
        table_container.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = ctk.CTkScrollbar(table_container)
        scrollbar.pack(side="right", fill="y")

        # Treeview untuk menampilkan pengguna
        columns = ("#1",)
        self.user_table = ttk.Treeview(
            table_container, 
            columns=columns, 
            show="headings", 
            yscrollcommand=scrollbar.set
        )
        self.user_table.heading("#1", text="Username")
        self.user_table.pack(side="left", fill="both", expand=True)
        
        scrollbar.configure(command=self.user_table.yview)

        # Tombol Refresh (untuk memuat ulang daftar)
        refresh_button = ctk.CTkButton(
             self.user_management_frame, 
             text="Refresh Daftar", 
             command=self.refresh_user_list,
             fg_color="#6357B1",
             hover_color="#4F44A3"
        )
        refresh_button.pack(pady=10, anchor="e")
        
        # Muat data pengguna awal
        self.refresh_user_list()
        
        # Tambahkan binding untuk memilih item di tabel (opsional, untuk tombol hapus)
        self.user_table.bind("<<TreeviewSelect>>", self.on_user_select)
        
        # Tombol Hapus (awalnya disable)
        self.delete_user_button = ctk.CTkButton(
            self.user_management_frame,
            text="Hapus Pengguna Terpilih",
            state="disabled",
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=self.confirm_delete_user
        )
        self.delete_user_button.pack(pady=10, anchor="e")

    def refresh_user_list(self):
        """Membersihkan tabel dan memuat ulang daftar pengguna dari file."""
        if not hasattr(self, 'user_table') or not self.user_table.winfo_exists():
             return # Jangan lakukan apa-apa jika tabel belum siap
             
        # Hapus item lama
        for item in self.user_table.get_children():
            self.user_table.delete(item)
            
        # Baca data baru
        self.users_list = self._read_all_users()
        
        # Masukkan data baru ke tabel
        for user_data in self.users_list:
             # Simpan line_index sebagai ID item di treeview untuk referensi
             self.user_table.insert("", "end", iid=user_data['line_index'], values=(user_data['username'],))
        
        # Reset tombol hapus
        if hasattr(self, 'delete_user_button'):
             self.delete_user_button.configure(state="disabled")

    def on_user_select(self, event=None):
        """Dipanggil saat pengguna dipilih di tabel."""
        selected_items = self.user_table.selection()
        if selected_items: # Jika ada item yang dipilih
            if hasattr(self, 'delete_user_button'):
                 self.delete_user_button.configure(state="normal") # Aktifkan tombol hapus
        else:
             if hasattr(self, 'delete_user_button'):
                  self.delete_user_button.configure(state="disabled") # Nonaktifkan jika tidak ada pilihan

    def confirm_delete_user(self):
        """Meminta konfirmasi sebelum menghapus pengguna."""
        selected_items = self.user_table.selection()
        if not selected_items:
            messagebox.showwarning("Peringatan", "Pilih pengguna yang ingin dihapus terlebih dahulu.")
            return
            
        # Ambil data pengguna yang dipilih (hanya satu pilihan diizinkan oleh default Treeview)
        selected_iid = selected_items[0] # iid adalah line_index
        selected_user = next((user for user in self.users_list if user['line_index'] == int(selected_iid)), None)
        
        if not selected_user:
             messagebox.showerror("Error", "Pengguna yang dipilih tidak ditemukan dalam data internal.")
             return
             
        username_to_delete = selected_user['username']
        
        if messagebox.askyesno("Konfirmasi Hapus", f"Apakah Anda yakin ingin menghapus pengguna '{username_to_delete}' secara permanen?"):
             self.delete_user_from_list(selected_user)
             
    def delete_user_from_list(self, user_to_delete):
        """Menghapus pengguna dari daftar dan menulis ulang file."""
        print(f"Attempting to delete user: {user_to_delete['username']} (line index: {user_to_delete['line_index']})")
        
        # Buat daftar pengguna yang akan disimpan (semua kecuali yang dipilih)
        users_to_keep = [user for user in self.users_list if user['line_index'] != user_to_delete['line_index']]
        
        # Tulis ulang file database
        if self._rewrite_user_file(users_to_keep):
             messagebox.showinfo("Sukses", f"Pengguna '{user_to_delete['username']}' berhasil dihapus.")
             # Muat ulang daftar di tabel
             self.refresh_user_list()
        else:
             messagebox.showerror("Gagal", f"Gagal menghapus pengguna '{user_to_delete['username']}'. Cek log untuk detail.")

    def _read_all_users(self):
        """Membaca semua data pengguna dari file database."""
        users = []
        db_file = "database/user.txt"
        try:
            with open(db_file, 'r') as f:
                for i, line in enumerate(f):
                    if line.strip():
                        parts = line.strip().split(",", 1)
                        if len(parts) == 2:
                            # Simpan username dan nomor baris asli (untuk penghapusan)
                            users.append({"username": parts[0], "line_index": i})
                        else:
                            print(f"Skipping malformed user line: {line.strip()}")
        except FileNotFoundError:
            print(f"User database file not found: {db_file}")
        except Exception as e:
            print(f"Error reading user file: {e}")
            messagebox.showerror("Error", f"Gagal membaca data pengguna: {e}")
        return users

    def _rewrite_user_file(self, users_to_keep):
        """Menulis ulang file database hanya dengan pengguna yang ingin disimpan."""
        db_file = "database/user.txt"
        temp_file = db_file + ".tmp"
        original_lines = []
        
        # Baca semua baris asli dulu
        try:
            with open(db_file, 'r') as f:
                original_lines = f.readlines()
        except FileNotFoundError:
            messagebox.showerror("Error", "File database pengguna tidak ditemukan saat mencoba menulis ulang.")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membaca file pengguna untuk penulisan ulang: {e}")
            return False
            
        # Tulis ke file temporary
        try:
            lines_to_keep_indices = {user['line_index'] for user in users_to_keep}
            with open(temp_file, 'w') as temp_f:
                for i, line in enumerate(original_lines):
                    if i in lines_to_keep_indices:
                        temp_f.write(line)
            
            # Ganti file asli dengan file temporary
            os.replace(temp_file, db_file)
            return True
        except Exception as e:
            print(f"Error rewriting user file: {e}")
            messagebox.showerror("Error", f"Gagal menyimpan perubahan data pengguna: {e}")
            # Coba hapus file temporary jika gagal
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception as remove_e:
                    print(f"Failed to remove temporary file: {remove_e}")
            return False
        
    def show_search_question(self):
        self._clear_content_area()
        target_frame = self.dashboard_instance.content_area

        # --- Frame utama untuk cari pertanyaan --- 
        search_question_frame = ctk.CTkFrame(target_frame, fg_color="transparent")
        search_question_frame.pack(expand=True, fill="both", padx=40, pady=30)

        ctk.CTkLabel(search_question_frame, text="Cari Pertanyaan", font=("Inter Bold", 24)).pack(pady=(0, 20), anchor="w")

        ctk.CTkLabel(search_question_frame, text="Masukkan Keyword Pertanyaan:", font=("Inter", 16)).pack(anchor="w", pady=(10,0))
        self.search_question_entry = ctk.CTkEntry(
            search_question_frame,
            height=40,
            font=("Inter", 14),
            placeholder_text="Contoh: informatika"
        )
        self.search_question_entry.pack(fill="x", pady=5)

        save_search_question_button = ctk.CTkButton(
            search_question_frame,
            text="Cari Pertanyaan",
            font=("Inter Bold", 16),
            height=50,
            fg_color="#6357B1",
            hover_color="#4F44A3",
            command=self.search_question
        )
        save_search_question_button.pack(pady=(30, 0), fill='x')

    def search_question(self):
        keyword = self.search_question_entry.get().strip().lower()
        if not keyword:
            messagebox.showwarning("Peringatan", "Masukkan keyword untuk mencari pertanyaan.")
            return

        matching_questions = self.read_questions(keyword=keyword)

        if matching_questions:
            results = "\n\n".join(matching_questions)
            messagebox.showinfo("Hasil Pencarian", f"Ditemukan {len(matching_questions)} pertanyaan:\n\n{results}")
        else:
            messagebox.showinfo("Hasil Pencarian", "Tidak ada pertanyaan yang cocok dengan keyword tersebut.")    
   
    def show_search_user_screen(self):
           self._clear_content_area()
           target_frame = self.dashboard_instance.content_area
           
           search_user_frame = ctk.CTkFrame(target_frame, fg_color="transparent")
           search_user_frame.pack(expand=True, fill="both", padx=40, pady=30)
           
           # ==== JUDUL ====
           title_label = ctk.CTkLabel(
                search_user_frame,
                text="🔎Cari pengguna berdasarkan Username",
                font=("Inter Bold", 24),
            )
           title_label.pack(pady=(30, 5), anchor="w")
           
           # ==== LABEL + ENTRY ====
           input_label = ctk.CTkLabel(
               search_user_frame,
               text ="Masukkan Username yang ingin dicari ",
               font=("Inter", 16)
           )
           input_label.pack(anchor="w", pady=(0,5))

           self.search_entry = ctk.CTkEntry(
                search_user_frame,
                height=40,
                font=("Inter", 14),
                placeholder_text="Contoh: budi123"
            )
           self.search_entry.pack(fill="x", pady=(0, 15))
           
           # ==== TOMBOL CARI ====
           search_button = ctk.CTkButton(
                search_user_frame,
                text="Cari Sekarang",
                height=40,
                font=("Inter Bold", 14),
                fg_color="#6357B1",
                hover_color="#4F44A3",
                command=self._handle_search
            )
           search_button.pack(pady=(0, 20), anchor="e")
           
           #=== HASIL PENCARIAN===
           self.result_label = ctk.CTkLabel(
                search_user_frame,
                text="",  # kosong dulu, nanti diisi setelah search
                font=("Inter", 14),
                text_color="gray"
            )
           self.result_label.pack(anchor="w", pady=(10, 0))


    def _handle_search(self):
        username = self.search_entry.get()
        if not username:
            messagebox.showwarning("Peringatan", "Masukkan username yang ingin dicari.")
            return

        if search_user(username):
            self.result_label.configure(
                text=f"✅ Username '{username}' ditemukan.",
                text_color="green"
            )
        else:   
            self.result_label.configure(
                text=f"❌ Username '{username}' tidak ditemukan.",
                text_color="red"
            )

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
