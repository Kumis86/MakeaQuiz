# src/gui/dashboard.py
import customtkinter as ctk

class Dashboard(ctk.CTkFrame):
    """Dashboard screen for the application"""
    def __init__(self, parent, logout_callback, play_quiz_callback=None):
        super().__init__(parent, corner_radius=0, width=1260, height=716)
        self.parent = parent
        self.logout_callback = logout_callback
        self.play_quiz_callback = play_quiz_callback
        
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
        
        # Navigation buttons
        buttons = [
            ("Dashboard", 89, None),
            ("Create Quiz", 158, None),
            ("My Quizzes", 227, None),
            ("Take Quiz", 296, self.play_quiz_callback),
            ("Results", 365, None),
            ("Settings", 434, None),
            ("Logout", 641, self.logout_callback)
        ]
        
        for text, y_pos, callback in buttons:
            # Set default callback
            if text == "Logout":
                command = self.logout_callback
            elif text == "Take Quiz" and self.play_quiz_callback:
                command = self.play_quiz_callback
            else:
                command = None
                
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=("Inter", 16),
                width=211,
                height=46,
                corner_radius=10,
                command=command,
                fg_color="#333333" if text != "Logout" else "#E74C3C",
                hover_color="#444444" if text != "Logout" else "#C0392B"
            )
            btn.place(x=44, y=y_pos)
        
        # User activity panel
        user_panel = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=10, width=391, height=309)
        user_panel.place(x=327, y=46)
        
        user_title = ctk.CTkLabel(
            user_panel, 
            text="User Aktif", 
            font=("Inter", 16), 
            text_color="#FFFFFF"
        )
        user_title.place(x=158, y=20)
        
        # Leaderboard panel
        leaderboard_panel = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=10, width=391, height=309)
        leaderboard_panel.place(x=774, y=46)
        
        leaderboard_title = ctk.CTkLabel(
            leaderboard_panel, 
            text="Leaderboard", 
            font=("Inter", 16), 
            text_color="#FFFFFF"
        )
        leaderboard_title.place(x=150, y=20)
        
        # Recent activity panel
        recent_panel = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=10, width=838, height=309)
        recent_panel.place(x=327, y=379)
        
        recent_title = ctk.CTkLabel(
            recent_panel, 
            text="Recent Activity", 
            font=("Inter", 16), 
            text_color="#FFFFFF"
        )
        recent_title.place(x=369, y=20)
