# src/gui/play_quiz.py
import customtkinter as ctk
from PIL import Image
from src.utils.assets import AssetManager
import os # <<< Impor os untuk membaca file pertanyaan
import random # <<< Impor random untuk mengacak pertanyaan (opsional)
import tkinter.messagebox as messagebox # <<< Impor messagebox
import tkinter.filedialog # <<< Impor filedialog
from fpdf import FPDF # <<< Impor FPDF

class PlayQuizScreen(ctk.CTkFrame):
    """Play Quiz screen for the application"""
    def __init__(self, parent, app_instance, back_callback):
        super().__init__(parent, corner_radius=0, width=1260, height=716)
        self.parent = parent
        self.app_instance = app_instance
        self.back_callback = back_callback
        self.asset_manager = AssetManager()
        
        # --- State Variables --- 
        self.quiz_modes = ["True/False", "Essay", "Pilihan Ganda"] # Daftar mode
        self.current_mode_index = 1 # Mulai dari Essay (indeks 1)
        self.selected_mode = None # Mode yang dipilih untuk kuis
        self.all_questions = [] # Semua pertanyaan dari file
        self.current_quiz_questions = [] # Pertanyaan untuk kuis saat ini
        self.current_question_index = 0 # Indeks pertanyaan saat ini
        self.score = 0 # Skor pengguna
        self.mode_images = {} # <<< Dictionary untuk menyimpan CTkImage mode
        self.timer_duration = 600 # Default 10 menit (dalam detik)
        self.remaining_time = 0
        self.timer_after_id = None # Untuk menyimpan ID jadwal self.after

        # --- Frames --- 
        self.mode_selection_frame = None
        self.quiz_content_frame = None
        self.result_frame = None
        self.card_frame = None # <<< Frame untuk kartu slider
        self.navbar_frame = None # <<< Frame Navbar

        # --- UI Elements (for quiz content) ---
        self.question_label = None
        self.answer_entry = None # Untuk Essay
        self.option_buttons = [] # Untuk MC
        self.tf_buttons = [] # Untuk TF
        self.feedback_label = None
        self.next_button = None
        self.submit_button = None
        self.timer_label = None # <<< Label untuk timer
        
        # --- UI Elements (for mode selection card) ---
        self.mode_image_label = None
        self.mode_name_label = None

        # --- UI Elements (Navbar) ---
        self.user_icon_button = None
        self.navbar_visible = False # <<< State untuk navbar

        self.configure(fg_color="#000000")
        self.place(x=0, y=0, relwidth=1, relheight=1)
        
        self._read_timer_setting() # <<< Baca setting timer
        self._load_all_questions()
        self._load_mode_images() # <<< Panggil fungsi pemuatan gambar mode
        self._create_ui()
        self._create_navbar() # <<< Panggil pembuatan navbar
        
    def _read_timer_setting(self):
        """Membaca durasi timer dari file settings."""
        try:
            settings_file = "database/quiz_settings.txt"
            if os.path.exists(settings_file):
                with open(settings_file, "r") as f:
                    for line in f:
                        if line.startswith("timer_minutes="):
                            # Admin menyimpan dalam menit, kita gunakan detik
                            minutes = int(line.strip().split("=")[1])
                            self.timer_duration = minutes * 60 # <<< Konversi ke detik
                            print(f"Timer duration loaded: {self.timer_duration} seconds ({minutes} minutes)")
                            break # Ambil baris pertama saja
            else:
                print(f"Timer settings file not found. Using default: {self.timer_duration} seconds.")
        except Exception as e:
            print(f"Error reading timer settings: {e}. Using default: {self.timer_duration} seconds.")
            # Jika error, gunakan default

    def _load_all_questions(self):
        """Membaca semua pertanyaan dari file quiz_questions.txt"""
        self.all_questions = []
        file_path = "database/quiz_questions.txt"
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    for line in f:
                        parts = line.strip().split("|")
                        if len(parts) >= 3:
                             q_type = parts[0].upper()
                             question = parts[1]
                             # Simpan dalam format yang mudah diolah
                             if q_type == "ESSAY" and len(parts) == 3:
                                  self.all_questions.append({"type": "Essay", "question": question, "answer": parts[2]})
                             elif q_type == "TF" and len(parts) == 3:
                                  self.all_questions.append({"type": "True/False", "question": question, "answer": parts[2].lower() == 'true'})
                             elif q_type == "MC" and len(parts) >= 4:
                                  # Pastikan ada setidaknya 4 opsi dan jawaban benar
                                  num_options = len(parts) - 3
                                  if num_options >= 1:
                                      options = parts[2:-1]
                                      try:
                                          correct_index = int(parts[-1])
                                          if 0 <= correct_index < len(options):
                                              self.all_questions.append({
                                                   "type": "Pilihan Ganda", 
                                                   "question": question, 
                                                   "options": options, 
                                                   "correct": correct_index
                                              })
                                          else: print(f"Skipping MC question due to invalid correct index: {line.strip()}")
                                      except ValueError:
                                           print(f"Skipping MC question due to non-integer correct index: {line.strip()}")
                                  else: print(f"Skipping MC question due to insufficient parts: {line.strip()}")
                             else: print(f"Skipping invalid line: {line.strip()}")
                        else: print(f"Skipping short line: {line.strip()}")
            except Exception as e:
                print(f"Error reading questions file: {e}")
                messagebox.showerror("Error", f"Gagal membaca file soal: {e}")
        else:
            print("Question file not found!")
            messagebox.showwarning("Warning", "File soal (database/quiz_questions.txt) tidak ditemukan.")

        # Optional: Shuffle questions globally once loaded
        # random.shuffle(self.all_questions)

    def _load_mode_images(self):
        """Memuat gambar untuk setiap mode kuis.
        Anda perlu membuat file gambar ini di assets/images/
        Contoh: mode_tf.png, mode_essay.png, mode_mc.png
        """
        mode_files = {
            "True/False": "mode_tf.JPG",
            "Essay": "mode_essay.JPG",
            "Pilihan Ganda": "mode_mc.JPG"
        }
        placeholder_size = (200, 150) # Ukuran gambar (sesuaikan jika perlu)

        for mode, filename in mode_files.items():
            try:
                image_path = self.asset_manager.get_asset_path(f"images/{filename}")
                original_image = Image.open(image_path)
                self.mode_images[mode] = ctk.CTkImage(
                    light_image=original_image,
                    dark_image=original_image,
                    size=placeholder_size
                )
                print(f"Loaded image for mode: {mode}")
            except FileNotFoundError:
                print(f"Warning: Image file not found for mode '{mode}': assets/images/{filename}")
                self.mode_images[mode] = None # Tandai jika tidak ada
            except Exception as e:
                print(f"Error loading image for mode '{mode}': {e}")
                self.mode_images[mode] = None
        
    def _create_ui(self):
        """Create the UI elements - starting with mode selection"""
        # Hapus UI lama jika ada
        for widget in self.winfo_children():
             widget.destroy()

        # --- Frame Utama untuk Pemilihan Mode --- 
        self.mode_selection_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mode_selection_frame.pack(expand=True, fill="both")

        # Judul
        title_label = ctk.CTkLabel(
            self.mode_selection_frame,
            text="Pilih Mode Kuis",
            font=("Inter Bold", 36),
            text_color="#FFFFFF"
        )
        title_label.pack(pady=(100, 40)) # Padding atas lebih besar

        # --- Slider Frame --- 
        slider_frame = ctk.CTkFrame(self.mode_selection_frame, fg_color="transparent")
        slider_frame.pack(pady=20)

        # Tombol Panah Kiri
        left_arrow_button = ctk.CTkButton(
            slider_frame,
            text="<",
            font=("Inter Bold", 30),
            width=60,
            height=60,
            fg_color="#E6B36A",
            hover_color="#4F44A3",
            command=lambda: self._change_mode(-1)
        )
        left_arrow_button.pack(side="left", padx=20)

        # --- Kartu Slider (Pengganti Label Mode) ---
        self.card_frame = ctk.CTkFrame(
            slider_frame,
            width=350, # <<< Lebar kartu
            height=250, # <<< Tinggi kartu
            fg_color="#1E1E1E", # <<< Warna latar kartu (abu-abu gelap)
            corner_radius=15
        )
        self.card_frame.pack(side="left", padx=30, pady=20)
        self.card_frame.pack_propagate(False) # Agar ukuran kartu tetap

        # Label Gambar Mode di dalam Kartu
        initial_mode = self.quiz_modes[self.current_mode_index]
        initial_image = self.mode_images.get(initial_mode, None)
        self.mode_image_label = ctk.CTkLabel(
            self.card_frame,
            text="" if initial_image else "Gambar tidak ditemukan", # Teks placeholder jika gambar error
            image=initial_image,
            fg_color="transparent"
        )
        self.mode_image_label.pack(pady=(10, 20)) # Padding atas dan bawah

        # Label Nama Mode di dalam Kartu
        self.mode_name_label = ctk.CTkLabel(
            self.card_frame,
            text=initial_mode,
            font=("Inter Bold", 24), # <<< Ukuran font nama mode
            text_color="#FFFFFF"
        )
        self.mode_name_label.pack(pady=(0, 20)) # Padding bawah

        # Tombol Panah Kanan
        right_arrow_button = ctk.CTkButton(
            slider_frame,
            text=">",
            font=("Inter Bold", 30),
            width=60,
            height=60,
            fg_color="#E6B36A",
            hover_color="#4F44A3",
            command=lambda: self._change_mode(1)
        )
        right_arrow_button.pack(side="left", padx=20)

        # --- Frame untuk Tombol Bawah --- 
        bottom_button_frame = ctk.CTkFrame(self.mode_selection_frame, fg_color="transparent")
        bottom_button_frame.pack(pady=30) # <<< Jarak dari slider

        # Tombol Mulai Mode Ini (di dalam frame tombol bawah)
        start_mode_button = ctk.CTkButton(
            bottom_button_frame, # <<< Parent baru
            text="Mulai Kuis Mode Ini",
            font=("Inter Bold", 18),
            width=250,
            height=50,
            corner_radius=10,
            fg_color="#E6B36A",
            hover_color="#4F44A3",
            command=self._select_mode_and_start
        )
        start_mode_button.pack(pady=10) # <<< Pack di dalam frame tombol bawah
        
        # Tombol Kembali (di bawah, di dalam frame tombol bawah)
        back_button = ctk.CTkButton(
            bottom_button_frame, # <<< Parent baru
            text="Kembali ke Menu Utama",
            font=("Inter Bold", 16),
            width=250, 
            height=50, 
            corner_radius=10,
            fg_color="#E6B36A", 
            hover_color="#4F44A3", 
            command=self.back_callback 
        )
        # <<< Hapus fill='x', biarkan pack default (center) >>>
        back_button.pack(pady=10)

        # --- Ikon User di Pojok Kiri Bawah (di atas semua frame lain) ---
        self.user_icon_button = ctk.CTkButton(
             self, # <<< Parent adalah self (PlayQuizScreen)
             text="👤", # <<< Karakter User Icon
             font=("Arial", 24), # Ukuran icon
             width=50, 
             height=50,
             fg_color="#E6B36A", 
             hover_color="#4F44A3",
             corner_radius=25, # Buat jadi lingkaran
             command=self._toggle_navbar
        )
        # Letakkan di pojok kiri bawah dengan sedikit margin
        self.user_icon_button.place(x=20, rely=1.0, y=-20, anchor="sw")

        # --- Frame untuk Konten Kuis dan Hasil (dibuat tapi tidak di-pack) ---
        self.quiz_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.result_frame = ctk.CTkFrame(self, fg_color="transparent")

    def _create_navbar(self):
        """Membuat frame navbar (awalnya tersembunyi)."""
        navbar_width = 250
        self.navbar_frame = ctk.CTkFrame(
            self, # <<< Parent adalah self (PlayQuizScreen)
            width=navbar_width,
            height=self.winfo_height(), # Tinggi penuh layar
            corner_radius=0,
            fg_color="#1A1A1A" # Warna lebih gelap dari sidebar dashboard
        )
        self.navbar_frame.place(x=-navbar_width, y=0, relheight=1.0)

        # Tambahkan Tombol-tombol ke Navbar
        navbar_buttons = [
            ("Pengaturan Akun", self._open_account_settings_popup),
            ("Skor Akun", self._show_scores),
            ("Simpan Skor ke PDF", self._save_scores_to_pdf),
            ("Tutup", self._toggle_navbar)
        ]

        pady_navbar = 15
        font_navbar = ("Inter Bold", 16)

        # Label Nama User (jika login)
        username = self.app_instance.get_current_logged_in_user()
        user_label_text = f"User: {username if username else 'Guest'}"
        user_label = ctk.CTkLabel(self.navbar_frame, text=user_label_text, font=("Inter Bold", 18), anchor="w")
        user_label.pack(pady=(30, pady_navbar * 2), padx=20, fill="x")

        for text, command in navbar_buttons:
            is_close_button = (text == "Tutup")
            btn = ctk.CTkButton(
                self.navbar_frame,
                text=text,
                font=font_navbar,
                height=45,
                anchor="w", # Rata kiri
                fg_color="#E74C3C" if is_close_button else "#E6B36A",
                hover_color="#C0392B" if is_close_button else "#4F44A3",
                command=command
            )
            btn.pack(pady=pady_navbar, padx=20, fill="x")

    def _toggle_navbar(self):
        """Menampilkan atau menyembunyikan navbar."""
        navbar_width = self.navbar_frame.winfo_width()
        
        if self.navbar_visible:
            # Sembunyikan navbar
            self.navbar_frame.place(x=-navbar_width, y=0)
            self.navbar_visible = False
        else:
            # Tampilkan navbar
            self.navbar_frame.place(x=0, y=0)
            self.navbar_frame.tkraise(self.user_icon_button) # Pastikan navbar di atas tombol icon
            self.navbar_visible = True

    def _open_account_settings_popup(self):
        """Membuka jendela popup untuk pengaturan akun."""
        print("Opening Account Settings Popup")
        if self.navbar_visible:
            self._toggle_navbar()
        current_user = self.app_instance.get_current_logged_in_user()
        if not current_user:
            messagebox.showwarning("Info", "Anda harus login untuk mengakses pengaturan akun.")
            return
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Pengaturan Akun")
        settings_window.geometry("400x350")
        settings_window.resizable(False, False)
        settings_window.transient(self.parent)
        settings_window.grab_set()
        main_frame = ctk.CTkFrame(settings_window, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        title_label = ctk.CTkLabel(main_frame, text="Pengaturan Akun", font=("Inter Bold", 20))
        title_label.pack(pady=(0, 20))
        user_info_label = ctk.CTkLabel(main_frame, text=f"Username: {current_user}", font=("Inter", 14))
        user_info_label.pack(pady=5)
        change_pw_button = ctk.CTkButton(main_frame, text="Ubah Password", font=("Inter Bold", 16), height=45, fg_color="#6357B1", hover_color="#4F44A3", command=self._open_change_password_popup)
        change_pw_button.pack(pady=10, fill="x")
        delete_acc_button = ctk.CTkButton(main_frame, text="Hapus Akun Saya", font=("Inter Bold", 16), height=45, fg_color="#E74C3C", hover_color="#C0392B", command=self._confirm_delete_account)
        delete_acc_button.pack(pady=10, fill="x")
        close_button = ctk.CTkButton(main_frame, text="Tutup", font=("Inter Bold", 16), height=45, fg_color="#555555", hover_color="#444444", command=settings_window.destroy)
        close_button.pack(pady=(20, 0), fill="x")
        settings_window.wait_window()

    def _open_change_password_popup(self):
        """Membuka popup untuk mengubah password."""
        print("Opening Change Password Popup")

        # Tutup popup pengaturan akun jika terbuka
        # (Tidak bisa langsung akses settings_window dari sini,
        #  tapi kita bisa buat popup ini modal terhadap window utama)

        current_user = self.app_instance.get_current_logged_in_user()
        if not current_user: return # Seharusnya tidak terjadi jika tombol bisa diklik

        # Buat window Toplevel baru untuk Ubah Password
        change_pw_window = ctk.CTkToplevel(self)
        change_pw_window.title("Ubah Password")
        change_pw_window.geometry("450x400") # Ukuran sedikit lebih besar
        change_pw_window.resizable(False, False)
        change_pw_window.transient(self.parent)
        change_pw_window.grab_set()

        main_frame = ctk.CTkFrame(change_pw_window, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        title_label = ctk.CTkLabel(main_frame, text="Ubah Password", font=("Inter Bold", 20))
        title_label.pack(pady=(0, 20))

        # Field Password Lama
        old_pw_label = ctk.CTkLabel(main_frame, text="Password Lama:", font=("Inter", 14))
        old_pw_label.pack(anchor="w", padx=10)
        old_pw_entry = ctk.CTkEntry(main_frame, width=380, height=40, show="•")
        old_pw_entry.pack(pady=(0, 15), fill="x", padx=10)

        # Field Password Baru
        new_pw_label = ctk.CTkLabel(main_frame, text="Password Baru:", font=("Inter", 14))
        new_pw_label.pack(anchor="w", padx=10)
        new_pw_entry = ctk.CTkEntry(main_frame, width=380, height=40, show="•")
        new_pw_entry.pack(pady=(0, 15), fill="x", padx=10)

        # Field Konfirmasi Password Baru
        confirm_pw_label = ctk.CTkLabel(main_frame, text="Konfirmasi Password Baru:", font=("Inter", 14))
        confirm_pw_label.pack(anchor="w", padx=10)
        confirm_pw_entry = ctk.CTkEntry(main_frame, width=380, height=40, show="•")
        confirm_pw_entry.pack(pady=(0, 20), fill="x", padx=10)

        # Fungsi untuk menangani submit ubah password
        def handle_submit():
            old_pass = old_pw_entry.get()
            new_pass = new_pw_entry.get()
            confirm_pass = confirm_pw_entry.get()
            # Panggil metode update_password di User
            success = self.app_instance.user_instance.update_password(
                current_user, old_pass, new_pass, confirm_pass
            )
            if success:
                change_pw_window.destroy() # Tutup popup jika sukses

        # Tombol Simpan Perubahan
        save_button = ctk.CTkButton(
            main_frame,
            text="Simpan Perubahan",
            font=("Inter Bold", 16),
            height=45,
            fg_color="#6357B1",
            hover_color="#4F44A3",
            command=handle_submit
        )
        save_button.pack(pady=10, fill="x", padx=10)

        # Tombol Batal
        cancel_button = ctk.CTkButton(
            main_frame,
            text="Batal",
            font=("Inter Bold", 16),
            height=45,
            fg_color="#555555",
            hover_color="#444444",
            command=change_pw_window.destroy
        )
        cancel_button.pack(pady=5, fill="x", padx=10)

        change_pw_window.wait_window()

    def _confirm_delete_account(self):
        """Meminta password untuk konfirmasi hapus akun."""
        print("Opening Confirm Delete Account Popup")

        current_user = self.app_instance.get_current_logged_in_user()
        if not current_user: return

        # Popup untuk memasukkan password konfirmasi
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Konfirmasi Hapus Akun")
        confirm_window.geometry("400x250")
        confirm_window.resizable(False, False)
        confirm_window.transient(self.parent)
        confirm_window.grab_set()

        main_frame = ctk.CTkFrame(confirm_window, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        warning_label = ctk.CTkLabel(
             main_frame,
             text="PERINGATAN!\nMasukkan password Anda untuk mengkonfirmasi penghapusan akun permanen.",
             font=("Inter Bold", 14),
             text_color="#E74C3C", # Merah
             wraplength=350
        )
        warning_label.pack(pady=(0, 15))

        password_label = ctk.CTkLabel(main_frame, text="Password:", font=("Inter", 14))
        password_label.pack(anchor="w", padx=10)
        password_entry = ctk.CTkEntry(main_frame, width=360, height=40, show="•")
        password_entry.pack(pady=(0, 20), fill="x", padx=10)

        # Fungsi untuk menangani submit hapus akun
        def handle_submit_delete():
            password = password_entry.get()
            if not password:
                 messagebox.showerror("Error", "Password harus diisi untuk konfirmasi.", parent=confirm_window)
                 return

            # Konfirmasi terakhir (optional tapi bagus)
            if not messagebox.askyesno("Konfirmasi Akhir", "Anda YAKIN ingin menghapus akun ini?", icon='warning', parent=confirm_window):
                 confirm_window.destroy()
                 return

            # Panggil metode delete_account di User
            success = self.app_instance.user_instance.delete_account(current_user, password)
            if success:
                 confirm_window.destroy() # Tutup popup konfirmasi
                 # Panggil logout dan kembali ke main screen (karena akun sudah tidak ada)
                 messagebox.showinfo("Akun Dihapus", "Akun Anda telah dihapus. Anda akan keluar.")
                 self.app_instance.handle_user_logout() # <-- Panggil logout dari App
            # Jika gagal, messagebox error sudah ditampilkan oleh User.delete_account

        # Tombol Hapus Permanen
        delete_button = ctk.CTkButton(
            main_frame,
            text="Hapus Akun Permanen",
            font=("Inter Bold", 16),
            height=45,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=handle_submit_delete
        )
        delete_button.pack(pady=10, fill="x", padx=10)

        # Tombol Batal
        cancel_button = ctk.CTkButton(
            main_frame,
            text="Batal",
            font=("Inter Bold", 16),
            height=45,
            fg_color="#555555",
            hover_color="#444444",
            command=confirm_window.destroy
        )
        cancel_button.pack(pady=5, fill="x", padx=10)

        confirm_window.wait_window()

    def _show_scores(self):
        """Membaca leaderboard dan menampilkan skor untuk pengguna saat ini."""
        print("Attempting to show user scores")
        current_user = self.app_instance.get_current_logged_in_user()

        if not current_user:
            messagebox.showwarning("Info", "Anda harus login untuk melihat skor.")
            return

        user_scores = []
        leaderboard_file = "database/leaderboard.txt"
        try:
            if os.path.exists(leaderboard_file):
                with open(leaderboard_file, "r") as f:
                    for line in f:
                        if line.strip():
                            parts = line.strip().split("|")
                            # Cek format dan username
                            if len(parts) >= 4 and parts[0] == current_user:
                                try:
                                    score = int(parts[1])
                                    total_q = int(parts[2])
                                    mode = parts[3]
                                    user_scores.append({
                                        "score": score,
                                        "total_q": total_q,
                                        "mode": mode,
                                        "percentage": (score / total_q * 100) if total_q > 0 else 0
                                    })
                                except (ValueError, IndexError):
                                    print(f"Skipping score line due to format/value error: {line.strip()}")
            if not user_scores:
                messagebox.showinfo("Skor Akun", "Belum ada data skor yang tersimpan untuk Anda.")
                return

            # Format pesan untuk messagebox
            scores_text = f"Skor untuk {current_user}:\n\n"
            # Urutkan berdasarkan yang terbaru (atau bisa juga skor tertinggi)
            # Untuk saat ini tampilkan sesuai urutan file
            for record in user_scores:
                 scores_text += f"- Mode: {record['mode']}, Skor: {record['score']}/{record['total_q']} ({record['percentage']:.1f}%)\n"

            messagebox.showinfo("Skor Akun", scores_text)
            
        except Exception as e:
            print(f"Error reading scores for user {current_user}: {e}")
            messagebox.showerror("Error", f"Gagal membaca data skor: {e}")

    def _save_scores_to_pdf(self):
        """Membaca skor pengguna dan menyimpannya ke file PDF."""
        print("Attempting to save user scores to PDF")
        current_user = self.app_instance.get_current_logged_in_user()

        if not current_user:
            messagebox.showwarning("Info", "Anda harus login untuk menyimpan skor.")
            return

        user_scores = []
        leaderboard_file = "database/leaderboard.txt"
        try:
            # Baca dan filter skor (logika sama seperti _show_scores/_print_scores)
            if os.path.exists(leaderboard_file):
                with open(leaderboard_file, "r") as f:
                    for line in f:
                        if line.strip():
                            parts = line.strip().split("|")
                            if len(parts) >= 4 and parts[0] == current_user:
                                try:
                                    score = int(parts[1])
                                    total_q = int(parts[2])
                                    mode = parts[3]
                                    user_scores.append({
                                        "score": score, "total_q": total_q, "mode": mode,
                                        "percentage": (score / total_q * 100) if total_q > 0 else 0
                                    })
                                except (ValueError, IndexError):
                                    print(f"Skipping score line: {line.strip()}")
            
            if not user_scores:
                messagebox.showinfo("Simpan Skor", "Belum ada data skor untuk disimpan.")
                return

            # Minta lokasi penyimpanan file PDF
            file_path = tkinter.filedialog.asksaveasfilename(
                title="Simpan Riwayat Skor ke PDF",
                defaultextension=".pdf", # <<< Ekstensi default PDF
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )

            if file_path:
                try:
                    # Buat objek PDF
                    pdf = FPDF()
                    pdf.add_page()
                    
                    # Judul
                    pdf.set_font("Arial", 'B', 16) # Font Bold
                    pdf.cell(0, 10, f"Riwayat Skor untuk {current_user}", ln=1, align='C')
                    pdf.ln(10) # Spasi setelah judul

                    # Data Skor
                    pdf.set_font("Arial", size=12)
                    for record in user_scores:
                        pdf.cell(0, 7, f"Mode       : {record['mode']}", ln=1)
                        pdf.cell(0, 7, f"Skor       : {record['score']} / {record['total_q']} ({record['percentage']:.1f}%)", ln=1)
                        pdf.ln(5) # Spasi antar record
                    
                    # Simpan file PDF
                    pdf.output(file_path, 'F')
                    messagebox.showinfo("Sukses", f"Riwayat skor berhasil disimpan ke PDF:\n{file_path}")
                
                except Exception as pdf_e:
                    print(f"Error creating or saving PDF: {pdf_e}")
                    messagebox.showerror("Error PDF", f"Gagal membuat atau menyimpan file PDF: {pdf_e}")
            else:
                print("User cancelled saving PDF file.")

        except Exception as read_e:
            print(f"Error preparing scores for PDF: {read_e}")
            messagebox.showerror("Error", f"Gagal mempersiapkan data skor: {read_e}")

    def _update_mode_display(self):
        """Memperbarui tampilan kartu (gambar dan nama mode)."""
        current_mode = self.quiz_modes[self.current_mode_index]
        
        # Update Nama Mode
        if self.mode_name_label:
            self.mode_name_label.configure(text=current_mode)

        new_image = self.mode_images.get(current_mode)
        # Update Gambar Mode
        if self.mode_image_label:
            self.mode_image_label.configure(
                 image=new_image,
                 text="" if new_image else "Gambar tidak ditemukan" # Tampilkan placeholder jika gambar None
            )

    def _change_mode(self, direction):
        """Handles clicks on the arrow buttons to change the mode."""
        self.current_mode_index = (self.current_mode_index + direction) % len(self.quiz_modes)
        self._update_mode_display()

    def _select_mode_and_start(self):
        """Hides mode selection, loads questions for the selected mode, and shows the first question."""
        self.selected_mode = self.quiz_modes[self.current_mode_index]
        print(f"Mode dipilih: {self.selected_mode}")

        # Filter pertanyaan berdasarkan mode yang dipilih
        self.current_quiz_questions = [q for q in self.all_questions if q['type'] == self.selected_mode]
        random.shuffle(self.current_quiz_questions) # Acak pertanyaan untuk mode ini

        if not self.current_quiz_questions:
            messagebox.showerror("Error", f"Tidak ada soal yang ditemukan untuk mode '{self.selected_mode}'.")
            print(f"Tidak ada soal untuk mode {self.selected_mode}")
            return # Jangan lanjutkan jika tidak ada soal

        print(f"Jumlah soal ditemukan: {len(self.current_quiz_questions)}")
        self.current_question_index = 0
        self.score = 0
        self.remaining_time = self.timer_duration # <<< Set waktu awal

        # Sembunyikan frame pemilihan mode
        if self.mode_selection_frame:
            self.mode_selection_frame.pack_forget()

        # Tampilkan frame konten kuis
        if self.quiz_content_frame:
             # Bersihkan frame konten kuis sebelum digunakan
             for widget in self.quiz_content_frame.winfo_children():
                  widget.destroy()
             self.quiz_content_frame.pack(expand=True, fill="both")
             self._display_question() # Tampilkan pertanyaan pertama
             self._start_timer() # <<< Mulai timer setelah UI siap
        else:
             print("Error: quiz_content_frame tidak terdefinisi")
             messagebox.showerror("Error", "Terjadi kesalahan internal saat memulai kuis.")

    def _display_question(self):
        """Menampilkan pertanyaan saat ini di quiz_content_frame."""
        if not self.quiz_content_frame or self.current_question_index >= len(self.current_quiz_questions):
            self._show_results()
            return

        # Bersihkan konten sebelumnya
        for widget in self.quiz_content_frame.winfo_children():
            widget.destroy()

        question_data = self.current_quiz_questions[self.current_question_index]
        # question_text = f"Pertanyaan {self.current_question_index + 1}/{len(self.current_quiz_questions)}:\n\n{question_data['question']}"

        # --- Frame Atas untuk Timer dan Info Pertanyaan ---
        top_frame = ctk.CTkFrame(self.quiz_content_frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(10,0))

        # Label Info Pertanyaan (Kiri)
        info_label = ctk.CTkLabel(
            top_frame,
            text=f"Pertanyaan {self.current_question_index + 1}/{len(self.current_quiz_questions)} | Mode: {self.selected_mode}",
            font=("Inter", 14),
            anchor="w"
        )
        info_label.pack(side="left")

        # Label Timer (Kanan)
        self.timer_label = ctk.CTkLabel(
            top_frame,
            text=self._format_time(self.remaining_time), # Tampilkan waktu awal
            font=("Inter Bold", 18),
            anchor="e"
        )
        self.timer_label.pack(side="right")

        # Tampilkan Teks Pertanyaan
        self.question_label = ctk.CTkLabel(
             self.quiz_content_frame, 
             text=question_data['question'], # <<< Hanya teks soal
             font=("Inter", 20),
             wraplength=800, # Agar teks panjang bisa wrap
             justify="center"
        )
        self.question_label.pack(pady=(30, 30)) # <<< Sesuaikan padding

        # Tampilkan Input Jawaban Sesuai Tipe
        q_type = question_data['type']
        self.option_buttons = []
        self.tf_buttons = []
        self.answer_entry = None
        self.feedback_label = None # Reset feedback label

        button_frame = ctk.CTkFrame(self.quiz_content_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        if q_type == "Essay":
            self.answer_entry = ctk.CTkEntry(
                self.quiz_content_frame,
                width=500,
                height=40,
                font=("Inter", 14),
                placeholder_text="Ketik jawaban Anda di sini..."
            )
            self.answer_entry.pack(pady=10)
            self.submit_button = ctk.CTkButton(
                 button_frame, 
                 text="Submit Jawaban", 
                 font=("Inter Bold", 16),
                 fg_color="#6357B1",
                 hover_color="#4F44A3",
                 command=self._submit_answer
            )
            self.submit_button.pack(pady=10)

        elif q_type == "True/False":
            true_button = ctk.CTkButton(
                 button_frame, 
                 text="True", 
                 width=150, height=50, 
                 font=("Inter Bold", 16),
                 fg_color="#6357B1",
                 hover_color="#4F44A3",
                 command=lambda: self._submit_answer(True)
            )
            false_button = ctk.CTkButton(
                 button_frame, 
                 text="False", 
                 width=150, height=50, 
                 font=("Inter Bold", 16),
                 fg_color="#6357B1",
                 hover_color="#4F44A3",
                 command=lambda: self._submit_answer(False)
            )
            true_button.pack(side="left", padx=20)
            false_button.pack(side="left", padx=20)
            self.tf_buttons = [true_button, false_button]

        elif q_type == "Pilihan Ganda":
            options = question_data['options']
            for i, option in enumerate(options):
                btn = ctk.CTkButton(
                    button_frame,
                    text=f"{i+1}. {option}",
                    width=400, 
            height=50,
                    font=("Inter Bold", 16),
                    fg_color="#6357B1",
                    hover_color="#4F44A3",
                    command=lambda index=i: self._submit_answer(index)
                )
                btn.pack(pady=5)
                self.option_buttons.append(btn)

        # Feedback Label (kosong awalnya)
        self.feedback_label = ctk.CTkLabel(self.quiz_content_frame, text="", font=("Inter", 16))
        self.feedback_label.pack(pady=10)

        # Tombol Next (disable awalnya, hanya untuk Essay)
        self.next_button = ctk.CTkButton(
             self.quiz_content_frame, 
             text="Lanjut >>", 
             font=("Inter Bold", 16),
             fg_color="#6357B1",
            hover_color="#4F44A3",
             command=self._next_question, 
             state="disabled"
        )
        if q_type != "Essay": # Sembunyikan tombol next jika bukan essay
             self.next_button.pack_forget()
        else:
             self.next_button.pack(pady=20) 

        # Tombol Keluar dari Kuis
        quit_quiz_button = ctk.CTkButton(
            self.quiz_content_frame,
            text="Keluar Kuis",
            font=("Inter Bold", 16),
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=self._confirm_quit_quiz
        )
        quit_quiz_button.pack(side="bottom", pady=20)

    def _format_time(self, total_seconds):
        """Format detik menjadi MM:SS"""
        if total_seconds < 0: total_seconds = 0
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def _start_timer(self):
        """Memulai atau melanjutkan countdown timer."""
        # Batalkan timer sebelumnya jika ada
        if self.timer_after_id:
            self.after_cancel(self.timer_after_id)

        # Update tampilan timer awal
        if self.timer_label:
            self.timer_label.configure(text=self._format_time(self.remaining_time))

        # Jalankan _update_timer setiap detik
        self.timer_after_id = self.after(1000, self._update_timer)
        print("Timer started.")

    def _update_timer(self):
        """Dipanggil setiap detik untuk memperbarui timer."""
        self.remaining_time -= 1
        if self.timer_label:
            self.timer_label.configure(text=self._format_time(self.remaining_time))

        if self.remaining_time <= 0:
            print("Time's up!")
            messagebox.showwarning("Waktu Habis", "Waktu pengerjaan kuis telah habis!")
            self._stop_timer() # Hentikan jadwal
            self._show_results() # Tampilkan hasil
        else:
            # Jadwalkan pembaruan berikutnya
            self.timer_after_id = self.after(1000, self._update_timer)

    def _stop_timer(self):
        """Menghentikan jadwal timer."""
        if self.timer_after_id:
            self.after_cancel(self.timer_after_id)
            self.timer_after_id = None
            print("Timer stopped.")

    def _submit_answer(self, selected_answer=None):
        """Memproses jawaban yang diberikan pengguna."""
        if not self.current_quiz_questions or self.current_question_index >= len(self.current_quiz_questions):
             return # Hindari error jika state tidak valid

        question_data = self.current_quiz_questions[self.current_question_index]
        q_type = question_data['type']
        is_correct = False

        # Disable tombol/entry setelah submit
        if self.answer_entry: self.answer_entry.configure(state="disabled")
        if self.submit_button: self.submit_button.configure(state="disabled")
        for btn in self.option_buttons: btn.configure(state="disabled")
        for btn in self.tf_buttons: btn.configure(state="disabled")

        # Cek Jawaban
        if q_type == "Essay":
            user_answer = self.answer_entry.get() if self.answer_entry else ""
            correct_answer = question_data['answer']
            # <<< Selalu tampilkan jawaban pengguna dan jawaban benar >>>
            feedback_text = f"Jawaban Anda:\n{user_answer}\n\nJawaban Seharusnya:\n{correct_answer}"
            # <<< Tampilkan feedback dengan warna netral (misal putih/default) >>>
            feedback_color = "#FFFFFF" # Atau warna default tema
            if self.next_button: self.next_button.configure(state="normal") # Aktifkan tombol next untuk essay

        elif q_type == "True/False":
            correct_answer = question_data['answer'] # boolean
            is_correct = (selected_answer == correct_answer)
            self.app_instance.audio.play_sound_effect(" assets/audio/select.wav")
            if not is_correct :
                self.app_instance.audio.play_sound_effect("assets/audio/wrong.wav")
            else :
                self.app_instance.audio.play_sound_effect("assets/audio/select.wav")
            feedback_text = "Benar!" if is_correct else f"Salah. Jawaban: {correct_answer}"
            feedback_color = "#4CAF50" if is_correct else "#E74C3C"
            if is_correct: self.score += 1 # <<< Skor hanya untuk TF & MC
            self.after(1500, self._next_question) # Jeda 1.5 detik
        
        elif q_type == "Pilihan Ganda":
             correct_index = question_data['correct'] # integer (indeks)
             is_correct = (selected_answer == correct_index)
             self.app_instance.audio.play_sound_effect("assets/audio/select.wav")
             if not is_correct:
                 self.app_instance.audio.play_sound_effect("assets/audio/wrong.wav")
             else :
                self.app_instance.audio.play_sound_effect("assets/audio/select.wav")
             feedback_text = "Benar!" if is_correct else f"Salah. Jawaban: {correct_index + 1}. {question_data['options'][correct_index]}"
             feedback_color = "#4CAF50" if is_correct else "#E74C3C"
             if is_correct: self.score += 1 # <<< Skor hanya untuk TF & MC
             # Highlight jawaban benar (hijau) dan salah (merah)
             if not is_correct:
                  self.option_buttons[selected_answer].configure(fg_color="#E74C3C", hover_color="#C0392B") 
             self.option_buttons[correct_index].configure(fg_color="#4CAF50", hover_color="#388E3C") 
             self.after(1500, self._next_question) # Jeda 1.5 detik

        # Update Skor dan Tampilkan Feedback
        if self.feedback_label:
             # <<< Gunakan feedback_color yang ditentukan >>>
             self.feedback_label.configure(text=feedback_text, text_color=feedback_color)
        
    def _next_question(self):
         """Pindah ke pertanyaan berikutnya."""
         self.current_question_index += 1
         if self.current_question_index < len(self.current_quiz_questions):
              self._display_question()
         else:
              self._show_results()
    
    def _confirm_quit_quiz(self):
        """Meminta konfirmasi sebelum keluar dari kuis dan stop timer."""
        if messagebox.askyesno("Keluar Kuis", "Apakah Anda yakin ingin keluar dari kuis ini? Skor tidak akan disimpan."):
             self._stop_timer() # <<< Hentikan timer saat keluar
             # Kembali ke pemilihan mode
             if self.quiz_content_frame: self.quiz_content_frame.pack_forget()
             if self.result_frame: self.result_frame.pack_forget()
             if self.mode_selection_frame: self.mode_selection_frame.pack(expand=True, fill="both")
             else: self._create_ui() # Buat ulang jika frame hilang

    def _show_results(self):
        """Menampilkan frame hasil kuis dan stop timer."""
        self._stop_timer() # <<< Hentikan timer saat hasil ditampilkan
        print("Menampilkan hasil kuis")
        if self.quiz_content_frame: self.quiz_content_frame.pack_forget()
        if self.result_frame:
            # Hapus konten lama jika ada
            for widget in self.result_frame.winfo_children():
                widget.destroy()
        else:
             # Buat frame jika belum ada
             self.result_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.result_frame.pack(expand=True, fill="both")

        # --- Hitung dan Tampilkan Hasil ---
        total_questions = len(self.current_quiz_questions)
        score_percentage = (self.score / total_questions * 100) if total_questions > 0 else 0
        result_text = (f"Kuis Selesai!\n"
                       f"Mode: {self.selected_mode}\n\n"
                       f"Skor Anda: {self.score} / {total_questions}\n"
                       f"({score_percentage:.1f}%)")
        result_label = ctk.CTkLabel(self.result_frame, text=result_text, font=("Inter Bold", 24))
        result_label.pack(pady=50)

        # --- Simpan Skor ke Leaderboard --- 
        current_user = self.app_instance.get_current_logged_in_user()
        if current_user and total_questions > 0: # Hanya simpan jika user login dan ada soal
             try:
                  leaderboard_file = "database/leaderboard.txt"
                  # Pastikan direktori ada
                  os.makedirs(os.path.dirname(leaderboard_file), exist_ok=True)
                  # Tambahkan baris baru ke file
                  with open(leaderboard_file, "a") as f:
                       # Format: username|score|total_questions|mode\n (Menyimpan lebih banyak info)
                       f.write(f"{current_user}|{self.score}|{total_questions}|{self.selected_mode}\n")
                  print(f"Score saved for user: {current_user}")
             except Exception as e:
                  print(f"Error saving score to leaderboard: {e}")
                  # Tidak perlu tampilkan error ke user, proses penyimpanan bersifat background

        # --- Tombol di Layar Hasil --- 
        # Tombol untuk kembali ke pemilihan mode
        back_to_mode_button = ctk.CTkButton(
             self.result_frame, 
             text="Pilih Mode Lain", 
             font=("Inter Bold", 16),
             fg_color="#6357B1",
             hover_color="#4F44A3",
             command=lambda: [
                  self.result_frame.pack_forget(), 
                  self.mode_selection_frame.pack(expand=True, fill="both") if self.mode_selection_frame else self._create_ui()
             ]
        )
        back_to_mode_button.pack(pady=20)
        
        # Tombol untuk kembali ke menu utama
        back_to_main_button = ctk.CTkButton(
             self.result_frame, 
             text="Kembali ke Menu Utama", 
             font=("Inter Bold", 16),
             fg_color="#6357B1",
             hover_color="#4F44A3",
             command=self.back_callback
        )
        back_to_main_button.pack(pady=20)

    # --- Hapus Metode _start_quiz lama --- 
    # def _start_quiz(self):
    #     """Start a quiz"""
    #     print("Starting quiz")
    #     self.back_callback()
