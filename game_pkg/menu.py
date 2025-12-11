# game_pkg/menu.py
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import os
import pygame

# --- IMPORTS ---
# We use relative imports (indicated by the dot .)
try:
    from .game_ui import BingoGameApp, P1_HIGHLIGHT, P2_HIGHLIGHT
    from .bingo_bomb import BingoBombApp
    from .credits import CreditsScreen
    from .exit_credits import ExitCredits 
    from .notifications import ask_casino_confirm, show_casino_alert 
except ImportError:
    # Fallback prevents crash if run individually (though you should run main.py)
    pass

# --- CASINO PALETTE ---
COLOR_BG = "#0f172a"
COLOR_GOLD = "#FFD700"
COLOR_RED_EXIT = "#be123c"
COLOR_COPPER = "#b45309"

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Bingo Master: Main Menu")
        self.root.geometry("600x650")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)
        
        # Fonts
        self.title_font = tkfont.Font(family="Times New Roman", size=48, weight="bold")
        self.button_font = tkfont.Font(family="Times New Roman", size=18, weight="bold")
        self.sub_font = tkfont.Font(family="Times New Roman", size=14, slant="italic")

        # Audio Setup
        self.snd_click = None
        self.menu_bgm_path = None
        self.setup_audio()
        self.setup_icon()

        self.selected_game_class = None
        self.opponent_mode = None
        self.show_main_screen()

    def setup_audio(self):
        try:
            pygame.mixer.init()
            # Robust path finding for assets
            base_dir = os.path.dirname(os.path.dirname(__file__)) # Go up one level from game_pkg
            assets_dir = os.path.join(base_dir, "assets")
            
            click_path = os.path.join(assets_dir, "mixkit_gameclick.wav")
            if os.path.exists(click_path): 
                self.snd_click = pygame.mixer.Sound(click_path)

            self.menu_bgm_path = os.path.join(assets_dir, "menu_bgm.mp3")
        except: 
            pass

    def setup_icon(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            icon_path = os.path.join(base_dir, "assets", "razzie_icon.jpg")
            if os.path.exists(icon_path):
                icon_image = Image.open(icon_path)
                self.icon_photo = ImageTk.PhotoImage(icon_image)
                self.root.iconphoto(True, self.icon_photo)
        except: 
            pass

    def check_and_play_bgm(self):
        try:
            if not pygame.mixer.music.get_busy() and self.menu_bgm_path:
                if os.path.exists(self.menu_bgm_path):
                    pygame.mixer.music.load(self.menu_bgm_path)
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
        except: pass

    def stop_bgm(self):
        try: pygame.mixer.music.stop() 
        except: pass 

    def clear_screen(self):
        for widget in self.root.winfo_children(): widget.destroy()

    # --- ACTION HANDLERS ---

    def confirm_and_exit(self):
        """Uses the custom notification to ask for exit."""
        should_exit = ask_casino_confirm(self.root, 
                                         title="CASHING OUT?", 
                                         message="Are you sure you want to leave the Casino Floor?")
        if should_exit:
            self.show_exit_credits()

    def show_exit_credits(self):
        self.stop_bgm()
        self.root.geometry("600x700")
        ExitCredits(self.root)

    # --- SCREENS ---

    def show_main_screen(self):
        self.clear_screen()
        self.root.geometry("600x650")
        self.check_and_play_bgm()
        
        center_frame = tk.Frame(self.root, bg=COLOR_BG)
        center_frame.pack(expand=True, fill="both")

        tk.Label(center_frame, text="BINGO", font=self.title_font, bg=COLOR_BG, fg=COLOR_GOLD).pack(pady=(10, 0))
        tk.Label(center_frame, text="MASTER", font=self.title_font, bg=COLOR_BG, fg="white").pack(pady=(0, 10))
        tk.Label(center_frame, text="The Jackpot Edition", font=self.sub_font, bg=COLOR_BG, fg=COLOR_GOLD).pack(pady=(0, 30))
        
        self.create_btn("● PLAY BINGO ●", self.show_game_type_selection, COLOR_GOLD, frame=center_frame).pack(pady=10)
        self.create_btn("CREDITS", self.show_credits_screen, COLOR_COPPER, frame=center_frame).pack(pady=10)
        self.create_btn("CASH OUT/EXIT", self.confirm_and_exit, COLOR_RED_EXIT, frame=center_frame).pack(pady=20)
        
        tk.Label(center_frame, text="Please Play Responsibly", bg=COLOR_BG, fg="#64748b", font=("Times New Roman", 10, "italic")).pack(pady=(10, 0))

    def show_credits_screen(self):
        self.stop_bgm()
        self.root.geometry("1280x850")
        CreditsScreen(self.root, self.show_main_screen)

    def show_game_type_selection(self):
        self.clear_screen()
        center_frame = tk.Frame(self.root, bg=COLOR_BG)
        center_frame.pack(expand=True, fill="both")
        tk.Label(center_frame, text="SELECT GAMEMODE", font=self.button_font, bg=COLOR_BG, fg=COLOR_GOLD).pack(pady=40)
        self.create_btn("CLASSIC BINGO", lambda: self.set_game_type(BingoGameApp), "#3b82f6", width=22, frame=center_frame).pack(pady=10)
        self.create_btn("BINGO BOMB", lambda: self.set_game_type(BingoBombApp), "#f97316", width=22, frame=center_frame).pack(pady=10)
        self.create_btn("BACK", self.show_main_screen, "#64748b", width=10, frame=center_frame).pack(pady=30)

    def set_game_type(self, game_class):
        self.selected_game_class = game_class
        self.show_opponent_selection()

    def show_opponent_selection(self):
        self.clear_screen()
        center_frame = tk.Frame(self.root, bg=COLOR_BG)
        center_frame.pack(expand=True, fill="both")
        mode_name = "Classic" if self.selected_game_class == BingoGameApp else "Bomb"
        tk.Label(center_frame, text=f"{mode_name}: OPPONENT", font=self.button_font, bg=COLOR_BG, fg=COLOR_GOLD).pack(pady=40)
        self.create_btn("Vs CPU", lambda: self.show_name_input("CPU"), "#8b5cf6", width=22, frame=center_frame).pack(pady=10)
        self.create_btn("2 PLAYERS", lambda: self.show_name_input("P2"), "#8b5cf6", width=22, frame=center_frame).pack(pady=10)
        self.create_btn("BACK", self.show_game_type_selection, "#64748b", width=10, frame=center_frame).pack(pady=30)

    def show_name_input(self, opponent_mode):
        self.clear_screen()
        center_frame = tk.Frame(self.root, bg=COLOR_BG)
        center_frame.pack(expand=True, fill="both")
        self.opponent_mode = opponent_mode
        
        tk.Label(center_frame, text="ENTER NAMES", font=self.button_font, bg=COLOR_BG, fg=COLOR_GOLD).pack(pady=30)
        
        entry_conf = {"font": ("Verdana", 14), "justify": "center", "bg": "#e2e8f0", "fg": "black", "relief": tk.FLAT}
        
        tk.Label(center_frame, text="Player 1:", font=("Times New Roman", 12, "bold"), bg=COLOR_BG, fg=P1_HIGHLIGHT).pack(pady=(10, 5))
        self.entry_p1 = tk.Entry(center_frame, **entry_conf)
        self.entry_p1.insert(0, "Player 1")
        self.entry_p1.pack(pady=5, ipadx=10, ipady=3)
        
        self.entry_p2 = None
        if opponent_mode == "P2":
            tk.Label(center_frame, text="Player 2:", font=("Times New Roman", 12, "bold"), bg=COLOR_BG, fg=P2_HIGHLIGHT).pack(pady=(20, 5))
            self.entry_p2 = tk.Entry(center_frame, **entry_conf)
            self.entry_p2.insert(0, "Player 2")
            self.entry_p2.pack(pady=5, ipadx=10, ipady=3)
        
        btn_action_frame = tk.Frame(center_frame, bg=COLOR_BG)
        btn_action_frame.pack(pady=40)
        self.create_btn("START", self.validate_and_start, "#10b981", width=15, frame=btn_action_frame).pack(side="left", padx=10)
        self.create_btn("CANCEL", self.show_opponent_selection, "#ef4444", width=15, frame=btn_action_frame).pack(side="right", padx=10)

    def validate_and_start(self):
        p1 = self.entry_p1.get().strip()
        p2 = "CPU-Bot"
        is_human_p2 = False
        
        # --- NEW NOTIFICATION USAGE ---
        try:
            if not p1: 
                show_casino_alert(self.root, "PIT BOSS ERROR", "Player 1 name is required!")
                return
            if self.opponent_mode == "P2":
                p2_input = self.entry_p2.get().strip()
                if not p2_input: 
                    show_casino_alert(self.root, "PIT BOSS ERROR", "Player 2 name is required!")
                    return
                p2 = p2_input
                is_human_p2 = True
            
            self.root.geometry("1280x850") 
            self.root.resizable(True, True) 
            self.stop_bgm() 
            self.clear_screen()
            self.selected_game_class(self.root, p1, p2, is_human_p2)
        except ValueError as e:
            show_casino_alert(self.root, "INPUT ERROR", str(e))

    def create_btn(self, text, cmd, color, width=22, frame=None):
        parent = frame if frame else self.root
        fg_color = "black" if color == COLOR_GOLD else "white" 
        def on_click():
            if self.snd_click: self.snd_click.play()
            cmd()
        btn = tk.Button(parent, text=text, font=self.button_font, bg=color, fg=fg_color, 
                        width=width, relief=tk.RAISED, bd=5, command=on_click, cursor="hand2")
        def on_enter(e): 
            if color == COLOR_GOLD: e.widget.config(bg="#d4af37") 
            else: e.widget.config(fg=COLOR_GOLD)
        def on_leave(e): e.widget.config(bg=color, fg=fg_color)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn