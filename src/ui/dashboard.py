# src/gui/dashboard.py
import customtkinter as ctk
from tkinter import messagebox

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
        self.content_area = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0)
        self.content_area.place(x=299, y=0, relwidth=(1 - 299/1260), relheight=1)
        
        # === Tombol Navigasi Admin ===
        admin_buttons = [
            ("Leaderboard", 89, "show_leaderboard"),
            ("User Aktif", 140, "show_active_users"),
            ("Upload Soal", 191, "show_upload_question"),
            ("Tambah Pertanyaan", 242, "show_add_question"),
            ("Lihat Pertanyaan", 293, "show_questions"),
            ("Edit Pertanyaan", 344, "show_edit_question"),
            ("Cari Pertanyaan", 395, "show_search_question"),
            ("Cari User", 599, "show_search_user"),
            ("Hapus Pertanyaan", 446, "show_delete_question"),
            ("Manajemen User", 497, "show_user_management"),
            ("Set Timer", 548, "show_set_timer"),
            ("Kembali", 650, "logout")
        ]
        
        for text, y_pos, callback_key in admin_buttons:
            command = self.callbacks.get(callback_key, None)
            if callback_key == "logout":
                command = self.logout_callback
            
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

        # --- Tampilan Awal Dashboard --- 
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