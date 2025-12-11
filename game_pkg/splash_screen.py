# game_pkg/splash_screen.py
import tkinter as tk
import tkinter.font as tkfont
import os
import pygame
import itertools
from PIL import Image, ImageTk 

try:
    from .menu import MainMenu
except ImportError:
    from menu import MainMenu 

COLOR_BG = "#0f172a"
COLOR_GOLD = "#FFD700"
COLOR_BAR_BG = "#1e293b"

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Bingo Master - Loading")
        self.root.geometry("600x650")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)
        self.center_window(600, 650)
        
        for widget in self.root.winfo_children(): widget.destroy()

        # --- FIX: UPDATED FILENAME TO 'razzie_icon.jpg' ---
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__)) 
            # Changed from logo_bingo.jpg to razzie_icon.jpg to match your file
            icon_path = os.path.join(base_dir, "assets", "razzie_icon.jpg")
            
            if os.path.exists(icon_path):
                icon_image = Image.open(icon_path)
                self.icon_photo = ImageTk.PhotoImage(icon_image)
                self.root.iconphoto(True, self.icon_photo)
            else:
                print(f"[WARNING] Splash icon missing at: {icon_path}")
        except Exception as e:
            print(f"[ERROR] Could not load splash icon: {e}")
        # ------------------------------

        self.loading_phrases = itertools.cycle([
            "Entering Casino Floor...", "Polishing Bingo Balls...",
            "Shuffling Deck...", "Counting Chips...", "Checking Luck..."
        ])
        
        self.progress_val = 0
        self.max_duration = 4000 
        self.step_interval = 50
        self.total_steps = self.max_duration // self.step_interval
        self.step_increment = 100 / self.total_steps

        self.create_casino_design()
        self.start_system()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_casino_design(self):
        self.canvas = tk.Canvas(self.root, width=600, height=650, bg=COLOR_BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Border
        self.canvas.create_rectangle(10, 10, 590, 640, outline=COLOR_GOLD, width=4)
        self.canvas.create_rectangle(15, 15, 585, 635, outline="#b45309", width=2)

        # Suits
        font_suits = ("Times New Roman", 32)
        self.canvas.create_text(50, 60, text="♠", fill=COLOR_GOLD, font=font_suits)
        self.canvas.create_text(550, 60, text="♥", fill=COLOR_GOLD, font=font_suits)
        self.canvas.create_text(50, 600, text="♣", fill=COLOR_GOLD, font=font_suits)
        self.canvas.create_text(550, 600, text="♦", fill=COLOR_GOLD, font=font_suits)

        # Text
        self.canvas.create_text(304, 204, text="BINGO", font=("Impact", 72), fill="black")
        self.canvas.create_text(300, 200, text="BINGO", font=("Impact", 72), fill=COLOR_GOLD)
        self.canvas.create_text(300, 280, text="MASTER", font=("Times New Roman", 36, "bold"), fill="white")
        self.canvas.create_text(300, 320, text="The Jackpot Edition", font=("Times New Roman", 16, "italic"), fill="#fbbf24")

        # Loading Bar
        bar_x, bar_y = 100, 450
        self.canvas.create_rectangle(bar_x, bar_y, bar_x + 400, bar_y + 30, fill=COLOR_BAR_BG, outline=COLOR_GOLD, width=2)
        self.bar_fill = self.canvas.create_rectangle(bar_x+2, bar_y+2, bar_x+2, bar_y+28, fill=COLOR_GOLD, outline="")
        self.lbl_loading = self.canvas.create_text(300, 420, text="Initializing...", font=("Verdana", 12), fill="white")

    def start_system(self):
        self.play_music()
        self.update_progress()
        self.cycle_text()

    def play_music(self):
        try:
            pygame.mixer.init()
            base_path = os.path.dirname(__file__)
            bgm_path = os.path.abspath(os.path.join(base_path, "..", "assets", "menu_bgm.mp3"))
            
            if os.path.exists(bgm_path):
                pygame.mixer.music.load(bgm_path)
                pygame.mixer.music.set_volume(0.5) 
                pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Audio Error: {e}")

    def update_progress(self):
        if self.progress_val < 100:
            self.progress_val += self.step_increment
            current_width = (self.progress_val / 100) * 396
            self.canvas.coords(self.bar_fill, 102, 452, 102 + current_width, 478)
            self.root.after(self.step_interval, self.update_progress)
        else:
            self.transition_to_menu()

    def cycle_text(self):
        if self.progress_val < 100:
            self.canvas.itemconfig(self.lbl_loading, text=next(self.loading_phrases))
            self.root.after(800, self.cycle_text)

    def transition_to_menu(self):
        self.canvas.destroy()
        MainMenu(self.root)