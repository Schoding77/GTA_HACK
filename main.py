import sys
import random
import string
import time

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QGridLayout,
    QVBoxLayout, QHBoxLayout, QFrame, QPushButton
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer


ROWS = 6
COLS = 8
CELL_SIZE = 40
TIME_LIMIT = 60
WORD = "PASSWORD"


# ===================== POPUP =====================
class Popup(QWidget):
    def __init__(self, message, restart_callback):
        super().__init__()
        self.setWindowTitle("Hack-D5G - MESSAGE")
        self.setStyleSheet("background-color:black;")
        self.resize(400, 200)

        layout = QVBoxLayout(self)

        label = QLabel(message)
        label.setFont(QFont("Consolas", 20, QFont.Bold))
        label.setStyleSheet("color:#00FF66;")
        label.setAlignment(Qt.AlignCenter)

        btn = QPushButton("RECOMMENCER")
        btn.setFont(QFont("Consolas", 16, QFont.Bold))
        btn.setStyleSheet(
            "color:#00FF66; background:black; border:2px solid #00FF66; padding:10px;"
        )
        btn.clicked.connect(restart_callback)

        layout.addWidget(label)
        layout.addWidget(btn)

# ===================== JEU =====================
class Hack(QWidget):
    def __init__(self):
        super().__init__()
        self.start_game()

    # ------------------ LANCEMENT ------------------
    def start_game(self):
        self.setWindowTitle("Hack-D5G")
        self.setStyleSheet("background-color:black;")
        self.resize(600, 520)
        self.setFocusPolicy(Qt.StrongFocus)

        self.current_col = 0
        self.cursor_row = ROWS // 2
        self.mistakes = 0
        self.start_time = time.time()
        self.game_over_triggered = False  

        self.offsets = [0.0] * COLS
        self.frozen = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.column_locked = [False] * COLS

        self.generate_columns()
        self.build_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_grid)
        self.timer.start(50)

        self.show()

    # ------------------ GÉNÉRATION ------------------
    def generate_columns(self):
        self.columns = []
        self.target_indices = []

        for c in range(COLS):
            letters = [random.choice(string.ascii_uppercase) for _ in range(ROWS)]
            target_index = random.randint(0, ROWS - 1)

            if c < len(WORD):
                letters[target_index] = WORD[c]

            self.columns.append(letters)
            self.target_indices.append(target_index)
