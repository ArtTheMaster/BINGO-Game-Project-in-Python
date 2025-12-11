# game_pkg/exit_credits.py
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import pygame
import os
import sys

# --- CASINO PALETTE ---
COLOR_BG = "#0f172a"
COLOR_FRAME = "#fbbf24" # Gold Frame

class ExitCredits:
    def __init__(self, root):
        self.root = root
        
        self.root.title("Thanks for Playing!")
        # Increased window size for better visibility
        self.root.geometry("700x800")
        self.root.configure(bg=COLOR_BG)
        
        # Center the window
        self.center_window(700, 600)
        
        for widget in self.root.winfo_children():
            widget.destroy()

        self.gif_path = os.path.join("assets", "gcash_milocation.gif")
        self.audio_path = os.path.join("assets", "gcash_mylocation.mp3")
        
        self.font_header = tkfont.Font(family="Impact", size=32)
        
        # Header Text
        tk.Label(self.root, text="THANKS FOR PLAYING!", font=self.font_header,
                 bg=COLOR_BG, fg="white").pack(pady=(30, 5))
        
        # --- MODIFIED: CASINO THEMED TEXT ---
        # Changed font to Times New Roman (Classic Casino Serif) 
        # Changed color to Gold (#FFD700) to match the high-roller vibe
        tk.Label(self.root, text="BINGO MASTER", font=("Times New Roman", 28, "bold"),
                 bg=COLOR_BG, fg="#FFD700").pack(pady=(0, 20))

        # --- GIF CONTAINER ---
        self.gif_frame = tk.Frame(self.root, bg=COLOR_FRAME, bd=6, relief=tk.RIDGE)
        self.gif_frame.pack(expand=True, pady=10)
        
        self.lbl_gif = tk.Label(self.gif_frame, bg="black")
        self.lbl_gif.pack(padx=3, pady=3)

        self.frames = []
        self.load_gif_frames()
        
        # Start Sequence
        self.play_audio()
        self.animate_gif(0)
        
        # Sync Exit with Audio
        self.check_audio_status()

    def center_window(self, width, height):
        """Centers the window on the user's screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def load_gif_frames(self):
        try:
            gif_img = Image.open(self.gif_path)
            try:
                while True:
                    # Resized to 550x650 for a BIGGER, clearer view
                    resized = gif_img.resize((650, 600), Image.Resampling.NEAREST)
                    self.frames.append(ImageTk.PhotoImage(resized))
                    gif_img.seek(gif_img.tell() + 1)
            except EOFError:
                pass
        except Exception as e:
            print(f"GIF Error: {e}")
            self.lbl_gif.config(text="[GIF LOADING ERROR]", fg="white")

    def play_audio(self):
        try:
            pygame.mixer.init()
            if os.path.exists(self.audio_path):
                pygame.mixer.music.load(self.audio_path)
                pygame.mixer.music.play()
            else:
                print("Audio file missing.")
                self.root.after(5000, self.close_app)
        except Exception as e:
            print(f"Audio Error: {e}")

    def check_audio_status(self):
        """Checks if music is still playing. If not, close app."""
        if pygame.mixer.music.get_busy():
            self.root.after(100, self.check_audio_status)
        else:
            self.close_app()

    def animate_gif(self, frame_index):
        if not self.frames: return

        frame = self.frames[frame_index]
        self.lbl_gif.config(image=frame)
        
        next_index = (frame_index + 1) % len(self.frames)
        
        # Speed set to 69ms per frame for smoother animation (noice)
        self.root.after(69, lambda: self.animate_gif(next_index))

    def close_app(self):
        try:
            pygame.mixer.music.stop()
            self.root.destroy()
            sys.exit()
        except:
            pass