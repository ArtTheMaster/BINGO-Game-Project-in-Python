# game_pkg/notifications.py
import tkinter as tk

# --- CASINO PALETTE ---
COLOR_BG = "#0f172a"      # Midnight Blue
COLOR_GOLD = "#FFD700"    # Casino Gold
COLOR_RED = "#be123c"     # Velvet Red
COLOR_GREEN = "#10b981"   # Success Green
COLOR_TEXT = "#e2e8f0"    # Off-white

class CasinoPopup:
    def __init__(self, parent, title, message, buttons, width=450, height=250):
        self.result = None
        
        # 1. Setup the Popup Window
        self.popup = tk.Toplevel(parent)
        self.popup.configure(bg=COLOR_BG)
        self.popup.overrideredirect(True) # Removes Title Bar (No X button)
        
        # 2. Force parent to update so we get accurate coordinates
        parent.update_idletasks()
        
        # 3. Smart Centering Calculation
        try:
            x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (width // 2)
            y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (height // 2)
        except:
            # Fallback if parent isn't ready
            x = (parent.winfo_screenwidth() // 2) - (width // 2)
            y = (parent.winfo_screenheight() // 2) - (height // 2)
            
        self.popup.geometry(f"{width}x{height}+{x}+{y}")
        
        # 4. Casino Style Frame (The Gold Border)
        self.frame = tk.Frame(self.popup, bg=COLOR_BG, bd=3, relief=tk.RAISED)
        # highlightbackground creates the border color effect
        self.frame.config(highlightbackground=COLOR_GOLD, highlightcolor=COLOR_GOLD, highlightthickness=3)
        self.frame.pack(expand=True, fill="both")

        # Fonts
        f_title = ("Times New Roman", 16, "bold")
        f_msg = ("Verdana", 11)
        f_btn = ("Times New Roman", 12, "bold")

        # 5. UI Elements
        # Title
        tk.Label(self.frame, text=title.upper(), font=f_title, bg=COLOR_BG, fg=COLOR_GOLD).pack(pady=(20, 10))
        
        # Message (Wraps text automatically)
        tk.Label(self.frame, text=message, font=f_msg, bg=COLOR_BG, fg=COLOR_TEXT, 
                 wraplength=width-40, justify="center").pack(pady=10, expand=True)

        # Buttons
        btn_frame = tk.Frame(self.frame, bg=COLOR_BG)
        btn_frame.pack(pady=20)

        for btn_text, btn_color, btn_val in buttons:
            # Black text for Gold buttons, White text for Red/Green/Blue
            fg_color = "black" if btn_color == COLOR_GOLD else "white"
            
            # Note: We use v=btn_val to capture the specific value for this button
            btn = tk.Button(btn_frame, text=btn_text, font=f_btn, 
                            bg=btn_color, fg=fg_color,
                            activebackground="white", activeforeground="black",
                            width=14, bd=3, relief=tk.RAISED,
                            command=lambda v=btn_val: self.on_click(v))
            btn.pack(side="left", padx=10)

        # 6. Make it Modal (Blocks other windows)
        self.popup.transient(parent) # Tells window manager this belongs to parent
        self.popup.grab_set()        # Forces all mouse interaction to this window
        parent.wait_window(self.popup) # Pauses code execution here until popup closes

    def on_click(self, value):
        self.result = value
        self.popup.destroy()

# --- CALLABLE FUNCTIONS ---

def ask_casino_confirm(parent, title="SECURITY CHECK", message="Are you sure you want to proceed?"):
    """
    Returns True if user clicks CONFIRM, False if CANCEL.
    """
    dialog = CasinoPopup(parent, title, message, 
                         buttons=[("CONFIRM", COLOR_GREEN, True), 
                                  ("CANCEL", COLOR_RED, False)])
    return dialog.result

def show_casino_alert(parent, title="PIT BOSS SAYS", message="Action Completed."):
    """
    Just shows a message with an ACKNOWLEDGE button. Returns nothing.
    """
    CasinoPopup(parent, title, message, 
                buttons=[("ACKNOWLEDGE", COLOR_GOLD, True)], height=220)

def ask_risk_check(parent):
    """
    Special popup for Bingo Bomb mode.
    """
    msg = "A BOMB is hidden here!\n\nDo you want to RISK defusing it?\n(50% Chance to Clear, 50% Explosion)"
    dialog = CasinoPopup(parent, "⚠ HIGH STAKES ⚠", msg, 
                         buttons=[("CUT WIRE", "#d97706", True), 
                                  ("FOLD", "#64748b", False)],
                         width=500, height=300)
    return dialog.result