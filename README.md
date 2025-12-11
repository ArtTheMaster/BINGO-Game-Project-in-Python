# 🎰 BINGO MASTER: Casino Edition & Bingo Bomb
**Student Name:** Art Lorence H. Veridiano
**Course:** BSCS-DS-2A
**Date:** December 2025

## 📝 Project Overview
This is a comprehensive OOP-based Python game featuring a GUI built with Tkinter and audio integration via Pygame. It simulates a high-stakes Casino environment with two distinct game modes:
1.  **Classic Bingo:** Traditional 75-ball bingo against a CPU or a 2nd Player.
2.  **Bingo Bomb:** A survival variation where hidden "Mines" are placed on the board. Hitting a mine reduces HP, adding risk and strategy.

---

## 🔧 How to Run
1.  Ensure you have Python installed.
2.  Install dependencies (if necessary): `pip install pygame pillow`
3.  Run the main file:
    ```bash
    python main.py
    ```

---

## 🏆 Applied OOP Concepts (Rubric Requirements)

*Use this section as your script during the presentation to prove you met the requirements.*

### 1. Class and Object (15 pts)
* **Requirement:** Correct and meaningful class design.
* **Where to show it:**
    * **`player.py`:** The `Player` class encapsulates data (name, board numbers) and logic (`check_match`).
    * **`game_ui.py`:** The `BingoGameApp` class manages the game state and UI.
    * **`notifications.py`:** The `CasinoPopup` class creates reusable custom alert objects.

### 2. Inheritance (10 pts)
* **Requirement:** Proper parent-child class structure.
* **Where to show it:** `game_pkg/bingo_bomb.py`
* **Explanation:**
    * **Parent:** `BingoGameApp` (Classic Game).
    * **Child:** `BingoBombApp` (Survival Game).
    * **Concept:** The child class inherits all drawing/board logic but extends it by adding Health Bars and Explosion logic.

### 3. Polymorphism (10 pts)
* **Requirement:** Method overriding or polymorphic behavior.
* **Where to show it:** `game_pkg/bingo_bomb.py` -> `human_click()`
* **Explanation:** The child class **overrides** the parent's `human_click` method. Instead of just marking the number, it intercepts the click to trigger a "Risk Check" and calculates damage if a mine is hit.

### 4. Module and Package (20 pts)
* **Requirement:** Code separated into multiple files and using a custom package.
* **Where to show it:** The **`game_pkg/`** folder structure.
    * `notifications.py`: Handles UI alerts (Modularization).
    * `player.py`: Handles data logic.
    * `menu.py`: Handles navigation.

### 5. Decorator (10 pts)
* **Requirement:** At least one working decorator applied meaningfully.
* **Where to show it:** `game_pkg/utils.py`
* **Explanation:** The `@log_transaction` decorator is applied to `start_ball_animation` in `game_ui.py`. It automatically logs every ball draw to the console, separating logging logic from game logic.

### 6. Error Handling (10 pts)
* **Requirement:** Use of try-except to prevent crashes.
* **Where to show it:**
    * **`splash_screen.py`:** Wraps asset loading (`razzie_icon.jpg`) in try-except blocks so the game runs even if the image is missing.
    * **`menu.py`:** Catches `ValueError` if the user tries to start a game without entering a name.

### 7. GUI (Tkinter) (25 pts)
* **Requirement:** Functional GUI, smooth experience.
* **Where to show it:**
    * **Custom Design:** "Midnight Blue & Gold" Casino palette.
    * **Interactive Elements:** Hover effects on Bingo cards (`<Enter>`, `<Leave>`) and custom `CasinoPopup` windows.
    * **Animation:** The splash screen loading bar and the confetti effect in `credits.py`.

---

## 🎮 Game Controls
* **Left Click:** Select options, Mark numbers.
* **Draw Ball:** Click the red "ROLL" button.
* **Win Condition:** Complete 5 numbers horizontally, vertically, or diagonally.