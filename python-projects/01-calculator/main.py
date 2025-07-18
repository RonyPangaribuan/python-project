"""
Kalkulator GUI dengan Tkinter
Proyek pemula untuk belajar GUI programming dan operasi matematika
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Canggih")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Variables
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.total = 0
        self.history = []
        
        self.create_widgets()
        
    def create_widgets(self):
        # Display frame
        display_frame = ttk.Frame(self.root, padding="10")
        display_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Entry widget for display
        self.display_var = tk.StringVar(value="0")
        self.display = ttk.Entry(
            display_frame, 
            textvariable=self.display_var,
            font=("Arial", 16),
            justify="right",
            state="readonly"
        )
        self.display.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Button frame
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons layout
        buttons = [
            ('C', 0, 0), ('CE', 0, 1), ('⌫', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('±', 4, 0), ('0', 4, 1), ('.', 4, 2), ('=', 4, 3),
            ('√', 5, 0), ('x²', 5, 1), ('1/x', 5, 2), ('%', 5, 3),
        ]
        
        for (text, row, col) in buttons:
            btn = ttk.Button(
                button_frame,
                text=text,
                width=8,
                command=lambda t=text: self.button_click(t)
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
        # Configure grid weights
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
            
        # History frame
        history_frame = ttk.LabelFrame(self.root, text="Riwayat", padding="5")
        history_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        self.history_text = tk.Text(history_frame, height=6, width=50, state="disabled")
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=scrollbar.set)
        
        self.history_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def button_click(self, char):
        if char.isdigit() or char == '.':
            self.number_click(char)
        elif char in ['+', '-', '×', '÷']:
            self.operator_click(char)
        elif char == '=':
            self.equals_click()
        elif char == 'C':
            self.clear_all()
        elif char == 'CE':
            self.clear_entry()
        elif char == '⌫':
            self.backspace()
        elif char == '±':
            self.negate()
        elif char == '√':
            self.square_root()
        elif char == 'x²':
            self.square()
        elif char == '1/x':
            self.reciprocal()
        elif char == '%':
            self.percentage()
    
    def number_click(self, char):
        if self.current == "0" or self.current == "Error":
            self.current = char
        else:
            self.current += char
        self.update_display()
    
    def operator_click(self, op):
        if self.operator and self.previous:
            self.equals_click()
        
        self.previous = self.current
        self.operator = op
        self.current = "0"
    
    def equals_click(self):
        if self.operator and self.previous:
            try:
                prev = float(self.previous)
                curr = float(self.current)
                
                if self.operator == '+':
                    result = prev + curr
                elif self.operator == '-':
                    result = prev - curr
                elif self.operator == '×':
                    result = prev * curr
                elif self.operator == '÷':
                    if curr != 0:
                        result = prev / curr
                    else:
                        raise ZeroDivisionError
                
                # Add to history
                calculation = f"{self.previous} {self.operator} {self.current} = {result}"
                self.add_to_history(calculation)
                
                self.current = str(result)
                self.previous = ""
                self.operator = ""
                self.update_display()
                
            except (ValueError, ZeroDivisionError):
                self.current = "Error"
                self.update_display()
    
    def clear_all(self):
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.update_display()
    
    def clear_entry(self):
        self.current = "0"
        self.update_display()
    
    def backspace(self):
        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = "0"
        self.update_display()
    
    def negate(self):
        if self.current != "0" and self.current != "Error":
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
        self.update_display()
    
    def square_root(self):
        try:
            value = float(self.current)
            if value >= 0:
                result = math.sqrt(value)
                self.add_to_history(f"√{self.current} = {result}")
                self.current = str(result)
            else:
                self.current = "Error"
        except ValueError:
            self.current = "Error"
        self.update_display()
    
    def square(self):
        try:
            value = float(self.current)
            result = value ** 2
            self.add_to_history(f"{self.current}² = {result}")
            self.current = str(result)
        except ValueError:
            self.current = "Error"
        self.update_display()
    
    def reciprocal(self):
        try:
            value = float(self.current)
            if value != 0:
                result = 1 / value
                self.add_to_history(f"1/{self.current} = {result}")
                self.current = str(result)
            else:
                self.current = "Error"
        except ValueError:
            self.current = "Error"
        self.update_display()
    
    def percentage(self):
        try:
            value = float(self.current)
            result = value / 100
            self.add_to_history(f"{self.current}% = {result}")
            self.current = str(result)
        except ValueError:
            self.current = "Error"
        self.update_display()
    
    def update_display(self):
        # Format number display
        if self.current != "Error":
            try:
                # Remove trailing zeros and decimal point if not needed
                num = float(self.current)
                if num.is_integer():
                    self.display_var.set(str(int(num)))
                else:
                    self.display_var.set(str(num))
            except ValueError:
                self.display_var.set(self.current)
        else:
            self.display_var.set(self.current)
    
    def add_to_history(self, calculation):
        self.history.append(calculation)
        self.history_text.config(state="normal")
        self.history_text.insert(tk.END, calculation + "\n")
        self.history_text.config(state="disabled")
        self.history_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
