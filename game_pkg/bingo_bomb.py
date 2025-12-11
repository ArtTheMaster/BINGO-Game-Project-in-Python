# game_pkg/bingo_bomb.py
import tkinter as tk
from tkinter import messagebox
import random
import pygame
import os
# --- NEW IMPORTS ---
from .notifications import ask_risk_check, show_casino_alert
from .game_ui import BingoGameApp, COLOR_BG, COLOR_GOLD, COLOR_RED

class BingoBombApp(BingoGameApp):
    def __init__(self, root, p1_name, p2_name, is_p2_human):
        super().__init__(root, p1_name, p2_name, is_p2_human)
        self.root.title("BINGO BOMB: Survival Mode")
        
        self.p1_health = 2
        self.p2_health = 2

        # --- 💣 BOMB MODE AUDIO ---
        self.snd_explode = None
        
        try:
            # 1. Background Music
            bgm_path = os.path.join("assets", "uptown_jazzbomb.mp3")
            if os.path.exists(bgm_path):
                pygame.mixer.music.load(bgm_path)
                pygame.mixer.music.play(loops=-1)
                pygame.mixer.music.set_volume(0.5)
            
            # 2. Explosion Sound Effect
            explode_path = os.path.join("assets", "bomb_explode.mp3")
            if os.path.exists(explode_path):
                self.snd_explode = pygame.mixer.Sound(explode_path)
                self.snd_explode.set_volume(0.6) 
            else:
                print(f"[WARNING] Missing SFX: {explode_path}")

        except Exception as e:
            print(f"[ERROR] Bomb Audio Failed: {e}")

        candidates = [i for i in range(25) if i != 12]
        self.p1_mines = random.sample(candidates, random.randint(3, 4))
        self.p2_mines = random.sample(candidates, random.randint(3, 4))
        
        self.draw_health_bars()

    def draw_health_bars(self):
        self.lbl_p1_health = tk.Label(self.human_frame, text=f"HP: {'❤️'*self.p1_health}", 
                                      font=("Impact", 14), bg=COLOR_BG, fg=COLOR_RED)
        self.lbl_p1_health.pack(pady=5)

        self.lbl_p2_health = tk.Label(self.cpu_frame, text=f"HP: {'❤️'*self.p2_health}", 
                                      font=("Impact", 14), bg=COLOR_BG, fg=COLOR_RED)
        self.lbl_p2_health.pack(pady=5)

    def update_health_display(self):
        self.lbl_p1_health.config(text=f"HP: {'❤️'*self.p1_health}")
        self.lbl_p2_health.config(text=f"HP: {'❤️'*self.p2_health}")

    def human_click(self, player_obj, btn_list, value, index):
        if self.game_over: return
        
        if self.is_drawing:
            if self.snd_notify: self.snd_notify.play()
            self.show_toast("WAIT FOR THE BALL!")
            return

        if self.snd_click: self.snd_click.play()

        if value == self.current_draw:
            if self.snd_notify: self.snd_notify.play()

            # --- NEW: CUSTOM RISK CHECK ---
            # Instead of standard Yes/No, we use the specific Risk Popup
            risk_it = ask_risk_check(self.root)
            if not risk_it: 
                self.show_toast("PLAYED IT SAFE!")
                return

            # Proceed if they risked it (call Parent logic logic to mark cell)
            # NOTE: We can't call super().human_click easily because it duplicates logic.
            # So we manually mark it here similar to parent class:
            
            player_obj.marked[index] = True
            # Visual update handles in parent usually, but we need to do it here
            from .game_ui import P1_HIGHLIGHT, P2_HIGHLIGHT
            mark_color = P1_HIGHLIGHT if player_obj == self.human else P2_HIGHLIGHT
            btn_list[index].config(bg=mark_color, fg="black", state="disabled", relief=tk.SUNKEN)
            self.update_log(f"{player_obj.name} marked {value}!")
            self.check_winners()

            # Now Check for Bomb
            current_mines = self.p1_mines if player_obj == self.human else self.p2_mines
            if index in current_mines:
                self.take_damage(player_obj, btn_list[index])
        else:
            # Wrong number click
            self.show_toast("WRONG NUMBER!")

    def cpu_turn(self, number):
        idx = self.cpu.check_match(number)
        
        # Manually do parent logic to avoid super() issues with custom flow
        if idx != -1:
            # CPU Logic: In a real game, CPU might "know" or randomly guess.
            # Here we just assume CPU always takes the risk.
            from .game_ui import P2_HIGHLIGHT
            self.p2_btns[idx].config(bg=P2_HIGHLIGHT, fg="black", relief=tk.SUNKEN)
            self.update_log(f"CPU marked {number}")
            self.check_winners()

        if idx != -1 and idx in self.p2_mines:
            target_widget = self.p2_btns[idx]
            self.take_damage(self.cpu, target_widget)

    def take_damage(self, player_obj, widget):
        try: widget.config(text="💣", bg=COLOR_RED, fg="white") 
        except: pass

        self.animate_explosion(widget)
        
        if player_obj == self.human:
            self.p1_health -= 1
        else:
            self.p2_health -= 1 
            
        self.update_health_display()
        
        if self.snd_explode:
            self.snd_explode.play()

        # --- NEW: CASINO ALERT FOR BOMB ---
        show_casino_alert(self.root, "EXPLOSION!", f"{player_obj.name} hit a BOMB! (-1 Heart)")

        if self.p1_health <= 0:
            self.game_over_sequence(winner=self.cpu, reason="Elimination")
        elif self.p2_health <= 0:
            self.game_over_sequence(winner=self.human, reason="Elimination")

    def animate_explosion(self, widget):
        final_bg = widget.cget("bg")
        colors = [COLOR_RED, COLOR_GOLD, "#000000", COLOR_RED, COLOR_GOLD]
        def step(i):
            if i < len(colors):
                try:
                    widget.config(bg=colors[i])
                    self.root.after(100, lambda: step(i+1))
                except: pass
            else:
                try: widget.config(bg=final_bg)
                except: pass
        step(0)

    def reveal_mines(self):
        for idx in self.p1_mines:
            try: self.human_btns[idx].config(bg="#94a3b8", text="💣")
            except: pass
        for idx in self.p2_mines:
            try: self.p2_btns[idx].config(bg="#94a3b8", text="💣")
            except: pass

    def check_winners(self):
        p1_win_indices = self.human.get_winning_indices()
        p2_win_indices = self.cpu.get_winning_indices()

        p1_win = len(p1_win_indices) > 0
        p2_win = len(p2_win_indices) > 0

        if p1_win: self.highlight_win(p1_win_indices, self.human_btns)
        if p2_win: self.highlight_win(p2_win_indices, self.p2_btns)

        if p1_win or p2_win:
            self.game_over_sequence(winner=None, reason="Draw" if (p1_win and p2_win) else "Bingo")

    def game_over_sequence(self, winner, reason):
        try: pygame.mixer.music.stop()
        except: pass

        self.reveal_mines()
        self.game_over = True
        
        self.play_game_over_sound(winner)

        msg = ""
        if reason == "Bingo" or reason == "Draw":
            if winner is None: msg = "It's a DRAW!"
            elif winner == self.human: msg = f"{self.human.name} WINS via BINGO!"
            else: msg = f"{self.cpu.name} WINS via BINGO!"
        elif reason == "Elimination":
            if winner == self.human: msg = f"{self.cpu.name} exploded! YOU WIN!"
            else: msg = f"{self.human.name} exploded! {self.cpu.name} WINS!"

        # --- NEW: CASINO ALERT FOR GAME OVER ---
        show_casino_alert(self.root, "SURVIVAL RESULT", msg)
        
        # After acknowledging, ask what to do next
        self.ask_post_game_action()