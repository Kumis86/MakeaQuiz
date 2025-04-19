# src/gui/dashboard.py
import customtkinter as ctk

class Dashboard(ctk.CTkFrame):
    """Dashboard screen for the application"""
    def __init__(self, parent, logout_callback, play_quiz_callback=None, is_admin=False, callbacks=None):
        super().__init__(parent, corner_radius=0, width=1260, height=716)
        self.parent = parent
        self.logout_callback = logout_callback
        self.play_quiz_callback = play_quiz_callback
        self.is_admin = is_admin
        self.callbacks = callbacks if callbacks else {}
        
        # Configure the frame
        self.configure(fg_color="#000000")
        self.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create UI elements
        self._create_ui()
        
    def _create_ui(self):
        """Create the UI elements"""
        # Sidebar
        sidebar = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=0, width=299, height=716)
        sidebar.place(x=0, y=0)
        
        # App title in sidebar
        title = ctk.CTkLabel(
            sidebar, 
            text="MakeaQuiz", 
            font=("Inter ExtraBoldItalic", 36), 
            text_color="#FFFFFF"
        )
        title.place(x=29, y=26)
        
        # === Area Konten Utama ===
        # Dibuat sebelum panel lain agar panel bisa ditempatkan di atasnya jika perlu
        # Atau, kita bisa buat ini sebagai frame utama di sebelah kanan sidebar
        self.content_area = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0)
        self.content_area.place(x=299, y=0, relwidth=(1 - 299/1260), relheight=1) # Menempati sisa ruang
        
        if self.is_admin:
            # === Tombol Navigasi Admin ===
            admin_buttons = [
                # (Nama Tombol, Posisi Y, Nama Callback di dict self.callbacks)
                ("Leaderboard", 89, "show_leaderboard"),
                ("User Aktif", 140, "show_active_users"),
                ("Upload Soal", 191, "show_upload_question"),
                ("Tambah Pertanyaan", 242, "show_add_question"),
                ("Lihat Pertanyaan", 293, "show_questions"),
                ("Edit Pertanyaan", 344, "show_edit_question"),
                ("Cari Pertanyaan", 395, "show_search_question"),
                ("Hapus Pertanyaan", 446, "show_delete_question"),
                ("Manajemen User", 497, "show_user_management"),
                ("Set Timer", 548, "show_set_timer"),
                ("Kembali", 650, "logout")
            ]
            
            for text, y_pos, callback_key in admin_buttons:
                command = self.callbacks.get(callback_key, None) # Dapatkan fungsi dari callbacks
                if callback_key == "logout":
                    command = self.logout_callback # Khusus untuk logout/kembali
                
                btn = ctk.CTkButton(
                    sidebar,
                    text=text,
                    font=("Inter", 16),
                    width=211,
                    height=46,
                    corner_radius=10,
                    command=command,
                    fg_color="#333333" if callback_key != "logout" else "#E74C3C",
                    hover_color="#444444" if callback_key != "logout" else "#C0392B"
                )
                btn.place(x=44, y=y_pos)
        
        else:
            print("[Dashboard.py] Masuk blok else (pengguna biasa)")
            # === Tombol Navigasi Pengguna Biasa ===
            user_buttons = [
                # (Nama Tombol, Posisi Y, Nama Callback di dict self.callbacks)
                ("Dashboard", 89, None), # Mungkin tidak perlu callback khusus?
                ("Create Quiz", 158, "create_quiz"),
                ("My Quizzes", 227, "my_quizzes"),
                ("Take Quiz", 296, None), # Gunakan play_quiz_callback
                ("Results", 365, "results"),
                ("Settings", 434, "settings"),
                ("Logout", 641, None) # Gunakan logout_callback
            ]

            for text, y_pos, callback_key in user_buttons:
                command = None
                if callback_key:
                    command = self.callbacks.get(callback_key)
                elif text == "Take Quiz" and self.play_quiz_callback:
                    command = self.play_quiz_callback
                elif text == "Logout":
                    command = self.logout_callback

                btn = ctk.CTkButton(
                    sidebar,
                    text=text,
                    font=("Inter", 16),
                    width=211,
                    height=46,
                    corner_radius=10,
                    command=command, # <<< Gunakan command dari callbacks
                    fg_color="#333333" if text != "Logout" else "#E74C3C",
                    hover_color="#444444" if text != "Logout" else "#C0392B"
                )
                btn.place(x=44, y=y_pos)

            # --- Tampilan Awal Dashboard Pengguna --- 
            # Kosongkan content_area atau tampilkan sambutan
            for widget in self.content_area.winfo_children():
                 widget.destroy()

            welcome_label = ctk.CTkLabel(
                self.content_area,
                text=f"Selamat Datang di MakeaQuiz!",
                font=("Inter Bold", 32)
            )
            welcome_label.pack(pady=50, padx=30)

            info_label = ctk.CTkLabel(
                 self.content_area,
                 text="Gunakan menu di samping untuk memulai.",
                 font=("Inter", 18)
            )
            info_label.pack(pady=10, padx=30)

            # Hapus panel-panel contoh lama
            # user_panel = ctk.CTkFrame(...)
            # leaderboard_panel = ctk.CTkFrame(...)
            # recent_panel = ctk.CTkFrame(...)
