import customtkinter as ctk
from tkinter import messagebox

# Set the theme and color mode
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ModernCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Modern Calculator")
        self.geometry("350x500")
        self.resizable(False, False)

        # Variables
        self.current_expression = ""
        self.equation = ctk.StringVar(value="0")

        # Layout Configuration
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((1, 2, 3, 4, 5), weight=1)

        # --- Display Screen ---
        self.display = ctk.CTkEntry(
            self,
            textvariable=self.equation,
            font=("Roboto", 40),
            width=300,
            height=80,
            corner_radius=10,
            fg_color="#1e1e1e", # Dark background for display
            text_color="white",
            border_width=0,
            justify="right"
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=(20, 10), sticky="nsew")
        self.display.configure(state="readonly") # Prevent typing with keyboard to enforce button use

        # --- Buttons Configuration ---
        # (Text, Row, Column, Color Type)
        buttons_config = [
            ('C', 1, 0, 'danger'), ('/', 1, 3, 'op'),
            ('7', 2, 0, 'num'), ('8', 2, 1, 'num'), ('9', 2, 2, 'num'), ('*', 2, 3, 'op'),
            ('4', 3, 0, 'num'), ('5', 3, 1, 'num'), ('6', 3, 2, 'num'), ('-', 3, 3, 'op'),
            ('1', 4, 0, 'num'), ('2', 4, 1, 'num'), ('3', 4, 2, 'num'), ('+', 4, 3, 'op'),
            ('.', 5, 0, 'num'), ('0', 5, 1, 'num'), ('=', 5, 2, 'accent')
        ]

        # Colors
        color_num = "#3a3a3a"      # Dark Gray
        color_op = "#FF9500"       # Orange
        color_accent = "#007AFF"   # Blue
        color_danger = "#FF3B30"   # Red
        hover_num = "#4a4a4a"

        for text, r, c, type_ in buttons_config:
            
            # Determine logic based on type
            if type_ == 'num':
                col = color_num
                hov = hover_num
                cmd = lambda x=text: self.click(x)
                cspan = 1
                width = 50
            elif type_ == 'op':
                col = color_op
                hov = "#FFAC33"
                cmd = lambda x=text: self.click(x)
                cspan = 1
                width = 50
            elif type_ == 'danger':
                col = color_danger
                hov = "#FF665E"
                cmd = self.clear_display
                cspan = 3 # Span C across 3 columns
                width = 150
            elif type_ == 'accent':
                col = color_accent
                hov = "#3395FF"
                cmd = self.equals
                cspan = 2 # Span = across 2 columns
                width = 100

            # Determine grid placement for standard buttons vs wide buttons
            # Note: I adjusted the grid logic slightly for a cleaner layout
            
            btn = ctk.CTkButton(
                self,
                text=text,
                font=("Roboto", 24, "bold"),
                width=width,
                height=60,
                corner_radius=15,
                fg_color=col,
                hover_color=hov,
                command=cmd
            )
            
            # Grid placement logic
            if text == 'C':
                btn.grid(row=r, column=c, columnspan=3, padx=5, pady=5, sticky="nsew")
            elif text == '=':
                btn.grid(row=r, column=c, columnspan=2, padx=5, pady=5, sticky="nsew")
            else:
                btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")


    def click(self, key):
        if self.equation.get() == "Error" or self.equation.get() == "0":
            self.current_expression = ""
        
        self.current_expression += str(key)
        self.equation.set(self.current_expression)

    def clear_display(self):
        self.current_expression = ""
        self.equation.set("0")

    def equals(self):
        try:
            # Note: In a real production app, don't use eval() for security, 
            # but for a simple calculator it is fine.
            result = str(eval(self.current_expression))
            if result.endswith('.0'):
                result = result[:-2]
            
            self.equation.set(result)
            self.current_expression = result 
        except ZeroDivisionError:
            self.equation.set("Error")
            self.current_expression = ""
        except Exception:
            self.equation.set("Error")
            self.current_expression = ""

if __name__ == "__main__":
    app = ModernCalculator()
    app.mainloop()