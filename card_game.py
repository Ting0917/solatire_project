import random
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
import platform

# ---------------------------
# Casino-style theme colors
# ---------------------------
FELT = "#0b3d0b"
FELT_DARK = "#072607"
GOLD = "#d4af37"
GOLD_DARK = "#8c6a00"
CARD_BG = "#0e2d0e"
CARD_HL = "#174d17"
TEXT = "#000000"
FADE_COLORS = [
    "#000000", "#222222", "#444444", "#666666",
    "#888888", "#aaaaaa", "#cccccc", "#eeeeee", "#ffffff"
]
FADE_DELAY_MS = 40


# ---------------------------
# Unicode mapping
# ---------------------------
def create_unicode_map():
    mapping = {}
    for cd in range(13):
        mapping[cd] = 127153 + cd       # Hearts
        mapping[cd + 13] = 127169 + cd  # Diamonds
        mapping[cd + 26] = 127185 + cd  # Clubs
        mapping[cd + 39] = 127137 + cd  # Spades
    return mapping


CARDS_CHR = create_unicode_map()


def is_jqk(card_index: int) -> bool:
    rank = card_index % 13
    return rank in (10, 11, 12)


class SolitaireGUI:
    def __init__(self, parent):
        self.root = parent
        self.root.configure(bg=FELT)

        # ---------------------------
        # Font setup
        # ---------------------------
        self.card_font_families = [
            "Segoe UI Symbol", "Arial Unicode MS", "Noto Sans Symbols", "Sans Serif", "Arial"
        ]
        available = set(tkfont.families())
        picked = next((fam for fam in self.card_font_families if fam in available), None)

        scale = 48
        if platform.system() == "Windows":
            scale = 42  # Windows 字型較大，略微縮小
        self.card_font = (picked or "TkDefaultFont", scale, "bold")

        # ---------------------------
        # Game state
        # ---------------------------
        self.reset_game_state()

        # --- Layout ---
        self.build_header()
        self.build_grid()
        self.build_controls()
        self.deal_round(initial=True)

    # ---------------------------
    # Game state
    # ---------------------------
    def reset_game_state(self):
        self.round_num = 1
        self.total_removed = 0
        self.deck = list(range(52))
        random.shuffle(self.deck)
        self.grid_cards = [None] * 16
        self.draw_ptr = 16
        self.round_active = True

    # ---------------------------
    # UI builders
    # ---------------------------
    def build_header(self):
        self.header = tk.Frame(self.root, bg=FELT)
        self.header.pack(padx=16, pady=(16, 10), fill="x")

        self.title_label = tk.Label(
            self.header, text="🃏 Unicode Solitaire — Remove J/Q/K",
            fg=GOLD, bg=FELT, font=("Georgia", 18, "bold")
        )
        self.title_label.pack()

        self.status_label = tk.Label(
            self.header, text="", fg=TEXT, bg=FELT, font=("Arial", 12, "bold")
        )
        self.status_label.pack(pady=(8, 0))

    def build_grid(self):
        self.grid_frame = tk.Frame(self.root, bg=FELT_DARK, bd=3, relief="ridge")
        self.grid_frame.pack(padx=20, pady=10)

        self.buttons = []
        for r in range(4):
            for c in range(4):
                idx = r * 4 + c
                btn = tk.Button(
                    self.grid_frame,
                    text="",
                    font=self.card_font,
                    fg=TEXT,
                    bg=CARD_BG,
                    activebackground=CARD_HL,
                    activeforeground=TEXT,
                    relief="raised",
                    bd=2,
                    width=3,
                    command=lambda i=idx: self.on_card_click(i)
                )
                btn.grid(row=r, column=c, padx=8, pady=8, ipadx=6, ipady=6)
                self.buttons.append(btn)

    def build_controls(self):
        self.controls = tk.Frame(self.root, bg=FELT)
        self.controls.pack(padx=16, pady=(6, 16), fill="x")

        self.next_btn = tk.Button(
            self.controls, text="Next Round ♻️", font=("Arial", 12, "bold"),
            fg="#332700", bg=GOLD, activebackground=GOLD_DARK, activeforeground="#000",
            bd=2, relief="raised", command=self.next_round
        )
        self.next_btn.pack(side="left", padx=(0, 10))

        self.reset_btn = tk.Button(
            self.controls, text="Reset 🔁", font=("Arial", 12, "bold"),
            fg="#332700", bg=GOLD, activebackground=GOLD_DARK, activeforeground="#000",
            bd=2, relief="raised", command=self.reset_game
        )
        self.reset_btn.pack(side="left", padx=10)

        self.quit_btn = tk.Button(
            self.controls, text="Quit 🚪", font=("Arial", 12, "bold"),
            fg="#332700", bg=GOLD, activebackground=GOLD_DARK, activeforeground="#000",
            bd=2, relief="raised", command=self.root.winfo_toplevel().destroy
        )
        self.quit_btn.pack(side="right")

    # ---------------------------
    # Round / dealing
    # ---------------------------
    def deal_round(self, initial=False):
        if initial:
            for i in range(16):
                self.grid_cards[i] = self.deck[i]
        else:
            for i in range(16):
                self.grid_cards[i] = self.deck[i]
        self.draw_ptr = 16
        self.round_active = True
        self.refresh_grid()
        self.update_status()

    def refresh_grid(self):
        for i, btn in enumerate(self.buttons):
            card = self.grid_cards[i]
            if card is None:
                btn.config(text=" ", state="disabled", fg=TEXT, bg=CARD_BG, relief="sunken")
            else:
                btn.config(text=chr(CARDS_CHR[card]), state="normal", fg=TEXT, bg=CARD_BG, relief="raised")

    def update_status(self, extra=""):
        msg = f"Round {self.round_num}/4 — Pictures removed: {self.total_removed}"
        if extra:
            msg += f" — {extra}"
        self.status_label.config(text=msg)

    # ---------------------------
    # Interactions
    # ---------------------------
    def on_card_click(self, grid_index: int):
        if not self.round_active:
            return
        card = self.grid_cards[grid_index]
        if card is None:
            return

        if is_jqk(card):
            self.buttons[grid_index].config(state="disabled")
            self.fade_out_card(grid_index, 0)

    def fade_out_card(self, grid_index: int, step: int):
        btn = self.buttons[grid_index]
        if step < len(FADE_COLORS):
            btn.config(fg=FADE_COLORS[step])
            self.root.after(FADE_DELAY_MS, lambda: self.fade_out_card(grid_index, step + 1))
        else:
            self.grid_cards[grid_index] = None
            btn.config(text=" ", fg=TEXT, bg=CARD_BG)
            self.total_removed += 1
            self.refresh_grid()
            self.update_status()
            if not self.any_jqk_in_grid():
                self.update_status("No more J/Q/K on table")

    def any_jqk_in_grid(self) -> bool:
        return any((c is not None and is_jqk(c)) for c in self.grid_cards)

    # ---------------------------
    # Controls
    # ---------------------------
    def next_round(self):
        if not self.round_active:
            return
        if self.any_jqk_in_grid():
            messagebox.showwarning("J/Q/K Remaining", "You must remove all J, Q, and K cards before moving to the next round.")
            return

        table_cards = [c for c in self.grid_cards if c is not None]
        not_drawn_cards = self.deck[self.draw_ptr:]
        pool = table_cards + not_drawn_cards
        random.shuffle(pool)
        self.deck = pool

        self.round_num += 1
        if self.round_num > 4:
            self.round_active = False
            if self.total_removed >= 12:
                messagebox.showinfo("Result", "🎉 You uncovered all pictures, you won!")
            else:
                messagebox.showinfo("Result", f"🃏 You uncovered {self.total_removed} pictures. Try again!")
            for b in self.buttons:
                b.config(state="disabled")
            self.next_btn.config(state="disabled")
            self.update_status("Game over")
            return

        if len(self.deck) < 16:
            for i in range(16):
                self.grid_cards[i] = None
            self.refresh_grid()
            self.round_active = False
            messagebox.showwarning("Deck Exhausted", "Not enough cards to start a new round.")
            self.update_status("Deck exhausted")
            return

        self.draw_ptr = 16
        for i in range(16):
            self.grid_cards[i] = self.deck[i]

        self.round_active = True
        self.refresh_grid()
        self.update_status("New round started")

        if self.round_num == 4:
            self.status_label.config(fg="#ffdd66")
            self.next_btn.config(bg="#ffcc44", activebackground="#d9a933")
        else:
            self.status_label.config(fg=TEXT)
            self.next_btn.config(bg=GOLD, activebackground=GOLD_DARK)

    def reset_game(self):
        self.reset_game_state()
        self.next_btn.config(state="normal")
        for b in self.buttons:
            b.config(state="normal")
        self.deal_round(initial=True)


# ---------------------------
# Run with Scrollable Frame
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Unicode Solitaire — J/Q/K Removal")

    # 固定視窗大小，但內容可滾動
    root.geometry("750x600")

    # 建立 Canvas + Scrollbar 結構
    canvas = tk.Canvas(root, bg=FELT, highlightthickness=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # 內部 Frame (實際放 UI)
    scrollable_frame = tk.Frame(canvas, bg=FELT)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_configure)

    # 啟用滑鼠滾輪捲動
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # 啟動遊戲
    app = SolitaireGUI(scrollable_frame)
    root.mainloop()
