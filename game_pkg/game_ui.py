import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import pygame
import tkinter.font as tkfont
import os
from .player import Player, ComputerPlayer
from .utils import log_transaction
from .notifications import ask_casino_confirm, show_casino_alert

COLOR_BG = "#0f172a"         
COLOR_PANEL = "#1e293b"      
COLOR_TEXT_MAIN = "#f1f5f9"  

CARD_BG_COLOR = "#064e3b"    
TILE_BG = "#f8fafc"          
TILE_FG = "#0f172a"          
TILE_HOVER = "#e2e8f0"       

COLOR_GOLD = "#fbbf24"       
COLOR_RED = "#dc2626"        
COLOR_DRAW_BTN = "#b91c1c"   
COLOR_DRAW_TEXT = "#ffffff"

P1_HIGHLIGHT = "#38bdf8"     
P2_HIGHLIGHT = "#ec4899"     

class BingoGameApp:
    def __init__(self, root, p1_name, p2_name, is_p2_human):
        self.root = root
        self.root.title("Bingo Master: Casino Edition")
        self.root.configure(bg=COLOR_BG)
        
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.is_p2_human = is_p2_human

        self.font_header = tkfont.Font(family="Impact", size=18)
        self.font_ball_main = tkfont.Font(family="Arial Black", size=65, weight="bold")
        self.font_ball_sub = tkfont.Font(family="Arial Narrow", size=16, weight="bold")
        self.font_tile = tkfont.Font(family="Verdana", size=13, weight="bold")
        self.font_log = tkfont.Font(family="Consolas", size=10)

        try:
            icon_path = os.path.join("assets", "razzie_icon.jpg")
            icon_image = Image.open(icon_path)
            self.icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(True, self.icon_photo) 
        except Exception:
            pass

        self.drawn_numbers = []
        self.current_draw = None
        self.game_over = False
        self.is_drawing = False

        self.snd_click = None
        self.snd_roll = None
        self.snd_draw = None
        self.snd_victory = None
        self.snd_defeat = None
        self.snd_notify = None
        self.bgm_classic = None
        
        try:
            pygame.mixer.init()
            
            def load_sound(filename):
                path = os.path.join("assets", filename)
                if os.path.exists(path): return pygame.mixer.Sound(path)
                return None

            self.snd_click = load_sound("mixkit_gameclick.wav")
            
            self.snd_roll = load_sound("rolling.mp3")
            if self.snd_roll: self.snd_roll.set_volume(0.5)

            self.snd_draw = load_sound("pop.wav")
            self.snd_victory = load_sound("BingWin.mp3") 
            self.snd_defeat = load_sound("BingLose.mp3")
            self.snd_notify = load_sound("mixkit_notifieraudio.wav")
            
            if self.__class__.__name__ == "BingoGameApp":
                bgm_path = os.path.join("assets", "jazzloop_classic.mp3")
                if os.path.exists(bgm_path):
                    pygame.mixer.music.load(bgm_path)
                    pygame.mixer.music.play(loops=-1)
                    pygame.mixer.music.set_volume(0.5)
                    self.bgm_classic = True
                    
        except Exception as e:
            print(f"Audio Error: {e}")

        self.human = Player(self.p1_name)
        self.cpu = Player(self.p2_name) if self.is_p2_human else ComputerPlayer(self.p2_name)

        self.setup_menu()
        self.create_layout()

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Main Menu", command=self.confirm_return_to_menu)
        filemenu.add_command(label="Exit", command=self.root.quit)
        self.root.config(menu=menubar)

    def create_layout(self):
        sidebar = tk.Frame(self.root, bg=COLOR_PANEL, width=300, padx=20, pady=20, relief=tk.RAISED, bd=2)
        sidebar.pack(side="left", fill="y")
        
        self.ball_canvas = tk.Canvas(sidebar, width=220, height=220, 
                                     bg=COLOR_PANEL, highlightthickness=0)
        self.ball_canvas.pack(pady=(10, 25))
        
        self.ball_canvas.create_oval(10, 10, 210, 210, fill=COLOR_GOLD, outline="#78350f", width=2)
        self.ball_canvas.create_oval(15, 15, 205, 205, fill="#b45309", outline="")
        self.ball_oval = self.ball_canvas.create_oval(20, 20, 200, 200, fill="white", outline="")
        
        self.ball_text_letter = self.ball_canvas.create_text(110, 90, text="?", font=self.font_ball_main, fill=COLOR_BG)
        self.ball_text_num = self.ball_canvas.create_text(110, 160, text="ROLL", font=self.font_ball_sub, fill="#64748b")

        self.btn_draw = tk.Button(sidebar, text="🎰 DRAW BALL", font=("Arial Black", 14),
                             bg=COLOR_DRAW_BTN, fg="white", 
                             activebackground="#b91c1c", activeforeground="white",
                             command=self.start_ball_animation, relief=tk.RAISED, bd=5, cursor="hand2")
        self.btn_draw.pack(fill="x", pady=15)

        tk.Label(sidebar, text="HISTORY LOG", bg=COLOR_PANEL, fg=COLOR_GOLD, font=("Verdana", 10, "bold")).pack(anchor="w")
        self.log_box = tk.Text(sidebar, height=12, width=30, font=self.font_log, 
                               bg="#0f172a", fg="#38bdf8", bd=2, relief=tk.SUNKEN, padx=5, pady=5)
        self.log_box.pack(fill="x", pady=5)

        self.btn_back = tk.Button(sidebar, text="🏠 MAIN MENU", font=("Arial", 10, "bold"),
                             bg="#475569", fg="white", command=self.confirm_return_to_menu, relief=tk.RAISED, bd=3)
        self.btn_back.pack(side="bottom", fill="x", pady=10)

        board_area = tk.Frame(self.root, bg=COLOR_BG)
        board_area.pack(side="right", expand=True, fill="both", padx=30, pady=20)
        board_area.columnconfigure(0, weight=1)
        board_area.columnconfigure(1, weight=1)

        self.human_frame = tk.Frame(board_area, bg=COLOR_BG)
        self.human_frame.grid(row=0, column=0)
        tk.Label(self.human_frame, text=f" {self.human.name} ", font=self.font_header,
                 bg=COLOR_BG, fg=P1_HIGHLIGHT).pack(pady=(0, 5))
        self.p1_grid = tk.Frame(self.human_frame, bg=CARD_BG_COLOR, bd=6, relief=tk.RIDGE)
        self.p1_grid.pack()

        self.cpu_frame = tk.Frame(board_area, bg=COLOR_BG)
        self.cpu_frame.grid(row=0, column=1)
        tk.Label(self.cpu_frame, text=f" {self.cpu.name} ", font=self.font_header,
                 bg=COLOR_BG, fg=P2_HIGHLIGHT).pack(pady=(0, 5))
        self.p2_grid = tk.Frame(self.cpu_frame, bg=CARD_BG_COLOR, bd=6, relief=tk.RIDGE)
        self.p2_grid.pack()

        self.create_grids()

    def create_grids(self):
        self.human_btns = []
        self.p2_btns = []
        bingo_letters = ["B", "I", "N", "G", "O"]
        header_colors = ["#ef4444", "#f97316", "#f59e0b", "#10b981", "#3b82f6"]

        for col, letter in enumerate(bingo_letters):
            c = header_colors[col]
            lbl1 = tk.Label(self.p1_grid, text=letter, font=("Arial Black", 16), 
                     bg=c, fg="white", width=4, relief=tk.RAISED, bd=2)
            lbl1.grid(row=0, column=col, padx=2, pady=5)
            lbl2 = tk.Label(self.p2_grid, text=letter, font=("Arial Black", 16), 
                     bg=c, fg="white", width=4, relief=tk.RAISED, bd=2)
            lbl2.grid(row=0, column=col, padx=2, pady=5)

        for i in range(25):
            val = self.human.card_numbers[i]
            txt = "★" if val == "FREE" else str(val)
            
            btn = tk.Button(self.p1_grid, text=txt, width=4, height=2, font=self.font_tile,
                            bg=TILE_BG, fg=TILE_FG, relief=tk.RAISED, bd=3, cursor="hand2",
                            command=lambda v=val, idx=i: self.human_click(self.human, self.human_btns, v, idx))
            if val == "FREE":
                btn.config(bg=COLOR_GOLD, fg="black", state="disabled", relief=tk.SUNKEN)
            else:
                btn.bind("<Enter>", lambda e: self.on_hover(e, True))
                btn.bind("<Leave>", lambda e: self.on_hover(e, False))
            btn.grid(row=(i//5)+1, column=i%5, padx=2, pady=2)
            self.human_btns.append(btn)

            val2 = self.cpu.card_numbers[i]
            txt2 = "★" if val2 == "FREE" else str(val2)
            if self.is_p2_human:
                btn2 = tk.Button(self.p2_grid, text=txt2, width=4, height=2, font=self.font_tile,
                                 bg=TILE_BG, fg=TILE_FG, relief=tk.RAISED, bd=3, cursor="hand2",
                                 command=lambda v=val2, idx=i: self.human_click(self.cpu, self.p2_btns, v, idx))
                if val2 == "FREE":
                    btn2.config(bg=COLOR_GOLD, fg="black", state="disabled", relief=tk.SUNKEN)
                else:
                    btn2.bind("<Enter>", lambda e: self.on_hover(e, True))
                    btn2.bind("<Leave>", lambda e: self.on_hover(e, False))
                btn2.grid(row=(i//5)+1, column=i%5, padx=2, pady=2)
                self.p2_btns.append(btn2)
            else:
                lbl = tk.Label(self.p2_grid, text=txt2, width=4, height=2, font=self.font_tile,
                               bg="#e2e8f0", fg="#475569", relief=tk.GROOVE, bd=2)
                if val2 == "FREE": lbl.config(bg=COLOR_GOLD, fg="black")
                lbl.grid(row=(i//5)+1, column=i%5, padx=2, pady=2, ipady=5)
                self.p2_btns.append(lbl)

    def on_hover(self, event, is_hovering):
        if event.widget['state'] == 'normal':
            color = TILE_HOVER if is_hovering else TILE_BG
            event.widget.config(bg=color)

    def get_bingo_info(self, pick):
        if 1 <= pick <= 15: return "B", "#ef4444", "white"
        if 16 <= pick <= 30: return "I", "#f97316", "white"
        if 31 <= pick <= 45: return "N", "#f59e0b", "black"
        if 46 <= pick <= 60: return "G", "#10b981", "white"
        if 61 <= pick <= 75: return "O", "#3b82f6", "white"
        return "?", "white", "black"

    @log_transaction
    def start_ball_animation(self):
        if self.snd_click: self.snd_click.play()
        if self.game_over or self.is_drawing: return

        self.is_drawing = True
        self.btn_draw.config(state="disabled")

        available = [n for n in range(1, 76) if n not in self.drawn_numbers]
        if not available:
            self.update_log("All numbers drawn!")
            self.is_drawing = False
            return

        if self.snd_roll:
            self.snd_roll.play(loops=-1) 

        final_pick = random.choice(available)
        self.animate_ball_spin(final_pick, 0)

    def animate_ball_spin(self, final_pick, step):
        if step < 60: 
            temp_pick = random.randint(1, 75)
            letter, color, t_color = self.get_bingo_info(temp_pick)
            self.ball_canvas.itemconfig(self.ball_oval, fill=color)
            self.ball_canvas.itemconfig(self.ball_text_letter, text=letter, fill=t_color)
            self.ball_canvas.itemconfig(self.ball_text_num, text=str(temp_pick), fill=t_color)
            self.root.after(50, lambda: self.animate_ball_spin(final_pick, step + 1))
        else:
            self.current_draw = final_pick
            self.drawn_numbers.append(final_pick)
            self.finish_draw(final_pick)

    def finish_draw(self, pick):
        if self.snd_roll:
            self.snd_roll.stop()

        try:
            letter, color, t_color = self.get_bingo_info(pick)
            self.ball_canvas.itemconfig(self.ball_oval, fill=color)
            self.ball_canvas.itemconfig(self.ball_text_letter, text=letter, fill=t_color)
            self.ball_canvas.itemconfig(self.ball_text_num, text=str(pick), fill=t_color)

            self.update_log(f"DRAWN: {letter}-{pick}")
            
            if self.snd_draw: self.snd_draw.play()

            if not self.is_p2_human:
                self.cpu_turn(pick)
        finally:
            self.btn_draw.config(state="normal")
            self.is_drawing = False

    def show_toast(self, message):
        show_casino_alert(self.root, "PIT BOSS SAYS", message)

    def human_click(self, player_obj, btn_list, value, index):
        if self.game_over: return
        
        if self.is_drawing:
            if self.snd_notify: self.snd_notify.play()
            self.show_toast("WAIT FOR THE BALL!")
            return

        if self.snd_click: self.snd_click.play()

        if value == self.current_draw:
            player_obj.marked[index] = True
            mark_color = P1_HIGHLIGHT if player_obj == self.human else P2_HIGHLIGHT
            btn_list[index].config(bg=mark_color, fg="black", state="disabled", relief=tk.SUNKEN)
            self.update_log(f"{player_obj.name} marked {value}!")
            self.check_winners()
        elif value != "FREE":
            if self.snd_notify: self.snd_notify.play()
            self.show_toast("WRONG NUMBER!")

    def cpu_turn(self, number):
        idx = self.cpu.check_match(number)
        if idx != -1:
            self.p2_btns[idx].config(bg=P2_HIGHLIGHT, fg="black", relief=tk.SUNKEN)
            self.update_log(f"CPU marked {number}")
        self.check_winners()

    def highlight_win(self, indices, btn_list):
        for idx in indices:
            try:
                btn_list[idx].config(bg=COLOR_GOLD, fg="black", relief=tk.RAISED, bd=4)
            except: pass

    def check_winners(self):
        p1_win_indices = self.human.get_winning_indices()
        p2_win_indices = self.cpu.get_winning_indices()
        p1_win = len(p1_win_indices) > 0
        p2_win = len(p2_win_indices) > 0

        if p1_win: self.highlight_win(p1_win_indices, self.human_btns)
        if p2_win: self.highlight_win(p2_win_indices, self.p2_btns)

        if p1_win or p2_win:
            winner = None
            if p1_win and p2_win: winner = None
            elif p1_win: winner = self.human
            else: winner = self.cpu
            self.game_over_sequence(winner, "Bingo")

    def play_game_over_sound(self, winner):
        try:
            if winner == self.human:
                if self.snd_victory: self.snd_victory.play()
            elif winner == self.cpu:
                if self.snd_defeat: self.snd_defeat.play()
            elif winner is None:
                if self.snd_defeat: self.snd_defeat.play()
        except:
            pass

    def game_over_sequence(self, winner, reason):
        if self.bgm_classic:
            try: pygame.mixer.music.stop()
            except: pass

        self.game_over = True
        self.play_game_over_sound(winner)
        
        msg = ""
        if reason == "Bingo" or reason == "Draw":
            if winner is None: msg = "It's a DRAW!"
            elif winner == self.human: msg = f"{self.human.name} WINS via BINGO!"
            else: msg = f"{self.cpu.name} WINS via BINGO!"

        show_casino_alert(self.root, "JACKPOT RESULT", msg)
        
        self.ask_post_game_action()

    def ask_post_game_action(self):
        play_again = ask_casino_confirm(self.root, "PLAY AGAIN?", "Do you want to play another round?")
        
        if play_again:
            self.restart_game()
        else:
            self.return_to_main_menu()

    def restart_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__class__(self.root, self.p1_name, self.p2_name, self.is_p2_human)

    def confirm_return_to_menu(self):
        if self.snd_click: self.snd_click.play()

        if self.game_over:
            self.return_to_main_menu()
            return
            
        leave = ask_casino_confirm(self.root, "LEAVE THE TABLE?", "Forfeit current game and return to Main Menu?")
        if leave:
            self.return_to_main_menu()

    def return_to_main_menu(self):
        try: pygame.mixer.music.stop()
        except: pass

        for widget in self.root.winfo_children():
            widget.destroy()
        from .menu import MainMenu
        self.root.geometry("600x650")
        MainMenu(self.root)

    def update_log(self, message):
        self.log_box.insert(tk.END, f"» {message}\n")
        self.log_box.see(tk.END)