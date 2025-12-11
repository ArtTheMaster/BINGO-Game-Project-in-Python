import tkinter as tk

COLOR_BG = "#0f172a"
COLOR_GOLD = "#FFD700"
COLOR_RED = "#be123c"
COLOR_GREEN = "#10b981"
COLOR_TEXT = "#e2e8f0"

class CasinoPopup:
    def __init__(self, parent, title, message, buttons, width=450, height=250):
        self.result = None
        
        self.popup = tk.Toplevel(parent)
        self.popup.configure(bg=COLOR_BG)
        self.popup.overrideredirect(True)
        
        parent.update_idletasks()
        
        try:
            x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (width // 2)
            y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (height // 2)
        except:
            x = (parent.winfo_screenwidth() // 2) - (width // 2)
            y = (parent.winfo_screenheight() // 2) - (height // 2)
            
        self.popup.geometry(f"{width}x{height}+{x}+{y}")
        
        self.frame = tk.Frame(self.popup, bg=COLOR_BG, bd=3, relief=tk.RAISED)
        self.frame.config(highlightbackground=COLOR_GOLD, highlightcolor=COLOR_GOLD, highlightthickness=3)
        self.frame.pack(expand=True, fill="both")

        f_title = ("Times New Roman", 16, "bold")
        f_msg = ("Verdana", 11)
        f_btn = ("Times New Roman", 12, "bold")

        tk.Label(self.frame, text=title.upper(), font=f_title, bg=COLOR_BG, fg=COLOR_GOLD).pack(pady=(20, 10))
        
        tk.Label(self.frame, text=message, font=f_msg, bg=COLOR_BG, fg=COLOR_TEXT, 
                 wraplength=width-40, justify="center").pack(pady=10, expand=True)

        btn_frame = tk.Frame(self.frame, bg=COLOR_BG)
        btn_frame.pack(pady=20)

        for btn_text, btn_color, btn_val in buttons:
            fg_color = "black" if btn_color == COLOR_GOLD else "white"
            
            btn = tk.Button(btn_frame, text=btn_text, font=f_btn, 
                            bg=btn_color, fg=fg_color,
                            activebackground="white", activeforeground="black",
                            width=14, bd=3, relief=tk.RAISED,
                            command=lambda v=btn_val: self.on_click(v))
            btn.pack(side="left", padx=10)

        self.popup.transient(parent)
        self.popup.grab_set()
        parent.wait_window(self.popup)

    def on_click(self, value):
        self.result = value
        self.popup.destroy()

def ask_casino_confirm(parent, title="SECURITY CHECK", message="Are you sure you want to proceed?"):
    dialog = CasinoPopup(parent, title, message, 
                         buttons=[("CONFIRM", COLOR_GREEN, True), 
                                  ("CANCEL", COLOR_RED, False)])
    return dialog.result

def show_casino_alert(parent, title="PIT BOSS SAYS", message="Action Completed."):
    CasinoPopup(parent, title, message, 
                buttons=[("ACKNOWLEDGE", COLOR_GOLD, True)], height=220)

def ask_risk_check(parent):
    msg = "A BOMB is hidden here!\n\nDo you want to RISK defusing it?\n(50% Chance to Clear, 50% Explosion)"
    dialog = CasinoPopup(parent, "⚠ HIGH STAKES ⚠", msg, 
                         buttons=[("RISK IT", "#d97706", True), 
                                  ("AVOID", "#64748b", False)],
                         width=500, height=300)
    return dialog.result