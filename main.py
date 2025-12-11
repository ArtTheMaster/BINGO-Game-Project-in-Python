#Making Game using Python, Tkinter and Pygame

import tkinter as tk
import os
import sys

# This to ensure Python can find the game_pkg folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from game_pkg.splash_screen import SplashScreen
except ImportError as e:
    print(f"Error importing game package: {e}")
    sys.exit(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = SplashScreen(root)
    root.mainloop()