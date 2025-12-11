import tkinter as tk
from tkinter import font as tkfont
import random
import string

COLOR_BG = "#0f172a"
COLOR_GOLD = "#fbbf24"
COLOR_WHITE = "#f1f5f9"
COLOR_RED = "#ef4444"
COLOR_SHADOW = "#475569"

class CreditsScreen:
    def __init__(self, root, return_callback):
        self.root = root
        self.return_callback = return_callback
        self.root.title("Bingo Master: Credits")
        self.root.configure(bg=COLOR_BG)
        
        self.is_running = True 

        for widget in self.root.winfo_children():
            widget.destroy()

        self.width = 1280
        self.height = 850
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, 
                                bg=COLOR_BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.font_header = tkfont.Font(family="Impact", size=40)
        self.font_main = tkfont.Font(family="Arial Black", size=50, weight="bold")
        self.font_detail = tkfont.Font(family="Verdana", size=24, weight="bold")

        self.confetti = []
        self.create_confetti()
        self.animate_confetti()

        btn_back = tk.Button(self.root, text="⬅ MAIN MENU", font=("Arial", 12, "bold"),
                             bg="#334155", fg="white", activebackground=COLOR_GOLD, activeforeground="black",
                             relief=tk.RAISED, bd=3, cursor="hand2",
                             command=self.go_back)
        btn_back.place(x=40, y=40)

        self.root.after(500, lambda: self.show_section(200, "DEVELOPED BY", "ART LORENCE H. VERIDIANO", COLOR_GOLD))
        self.root.after(3500, lambda: self.show_section(450, "COURSE & YEAR", "BSCS-DS-2A", COLOR_WHITE))
        self.root.after(6000, lambda: self.show_section(650, "PROJECT DATE", "DECEMBER 2025", COLOR_RED))

    def go_back(self):
        self.is_running = False
        self.return_callback()

    def create_confetti(self):
        for _ in range(50):
            x = random.randint(0, self.width)
            y = random.randint(-500, 0)
            size = random.randint(5, 10)
            color = random.choice([COLOR_GOLD, COLOR_RED, "#ffffff", "#3b82f6"])
            item = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            speed = random.randint(2, 7)
            self.confetti.append([item, speed])

    def animate_confetti(self):
        if not self.is_running: return 

        for particle in self.confetti:
            item, speed = particle
            self.canvas.move(item, 0, speed)
            coords = self.canvas.coords(item)
            
            if coords:
                if coords[1] > self.root.winfo_height():
                    new_x = random.randint(0, self.root.winfo_width())
                    self.canvas.coords(item, new_x, -10, new_x+8, -2)

        self.root.after(30, self.animate_confetti)

    def show_section(self, y_pos, label_text, value_text, value_color):
        if not self.is_running: return

        cx = self.root.winfo_width() // 2
        self.canvas.create_text(cx, y_pos, text=label_text, font=self.font_header, fill=COLOR_SHADOW)
        text_id = self.canvas.create_text(cx, y_pos + 70, text="", font=self.font_main, fill=value_color)
        
        self.roll_text(text_id, value_text, 0)

    def roll_text(self, text_id, target_text, step):
        if not self.is_running: return

        if step > len(target_text) + 20: 
            self.canvas.itemconfig(text_id, text=target_text)
            return

        locked_len = max(0, step - 10)
        current_str = target_text[:locked_len]
        remaining_len = len(target_text) - locked_len
        
        if remaining_len > 0:
            chaos = ''.join(random.choices(string.ascii_uppercase + "0123456789", k=remaining_len))
            current_str += chaos

        self.canvas.itemconfig(text_id, text=current_str)
        self.root.after(60, lambda: self.roll_text(text_id, target_text, step + 1))