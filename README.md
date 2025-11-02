# 🃏 Unicode Solitaire — J/Q/K Removal Game

A small interactive card game built with **Python (Tkinter)**.  
Your objective is to **remove all Jacks, Queens, and Kings** (picture cards) from the table across **4 rounds**, using simple strategy and memory.

This game displays real playing cards using Unicode suit characters — **no images required**.

---

## 🎮 Game Rules

- The game deals **16 cards** (4×4 grid) each round.
- Click on **J, Q, or K** to remove them.
- When **all** picture cards are removed from the grid, click **Next Round** to continue.
- The deck reshuffles between rounds.
- After **Round 4**, the game ends:
  - ✅ Remove all **12** picture cards → **You win!**
  - ❌ Fail to remove all → **Try again!**

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🎴 Unicode Playing Cards | Cards displayed entirely using Unicode characters. |
| 🕹 Simple Controls | Click to remove cards, continue rounds with a button. |
| ♻️ 4-Round Progression | Each round reshuffles remaining cards. |
| 🌟 Fade-Out Animation | Visual feedback when removing picture cards. |
| 🔁 Reset Anytime | Restart from Round 1 instantly. |

---

## 🛠 Requirements

- **Python 3.8+**
- **Tkinter** (included with most Python installations)

No external libraries required.

---

## ▶️ How to Run

```bash
python3 card_game.py
