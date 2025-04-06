import customtkinter as ctk
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
        self.entry = ctk.CTkEntry(container, width=400)
        self.entry.pack(pady=10)
        return self.entry
    
    def check_answer(self, user_input):
        user_text = user_input.get().strip().lower()
        return user_text == self.correct_answer.lower()

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
        return self.correct_answer == user_input.get()

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
        return user_input.get() == self.correct_answer
