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

# ------------------ INTERFACE ------------------
    def build_ui(self):
        if self.layout() is not None:
            while self.layout().count():
                item = self.layout().takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        title = QLabel("Hack-D5G")
        subtitle = QLabel("- NOT A HACKER SINCE 2024 -")
        title.setFont(QFont("Consolas", 24, QFont.Bold))
        subtitle.setFont(QFont("Consolas", 10))
        title.setStyleSheet("color:#00FF66;")
        subtitle.setStyleSheet("color:#00FF66;")
        title.setAlignment(Qt.AlignCenter)
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        top_bar = QHBoxLayout()
        left = QLabel("CLICKING RANDOMLY")
        left.setFont(QFont("Consolas", 10))
        left.setStyleSheet("color:#00BFFF;")

        self.timer_label = QLabel("01:00.000")
        self.timer_label.setFont(QFont("Consolas", 18))
        self.timer_label.setStyleSheet("color:yellow;")
        self.timer_label.setAlignment(Qt.AlignCenter)

        right = QLabel("📶 📶 📶")
        right.setFont(QFont("Consolas", 12))
        right.setStyleSheet("color:#00FF66;")

        top_bar.addWidget(left)
        top_bar.addWidget(self.timer_label, stretch=1)
        top_bar.addWidget(right)
        main_layout.addLayout(top_bar)

        grid_frame = QFrame()
        grid_frame.setStyleSheet("border:2px solid #00BFFF; background:#001020;")
        grid = QGridLayout(grid_frame)
        grid.setSpacing(2)
        grid.setContentsMargins(5, 5, 5, 5)

        self.labels = [[QLabel() for _ in range(COLS)] for _ in range(ROWS)]
        font = QFont("Consolas", 18)

        for r in range(ROWS):
            for c in range(COLS):
                lbl = self.labels[r][c]
                lbl.setFont(font)
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setFixedSize(CELL_SIZE, CELL_SIZE)
                lbl.setStyleSheet("color:white;")
                grid.addWidget(lbl, r, c)

        self.cursor_h = QFrame()
        self.cursor_h.setFixedHeight(CELL_SIZE)
        self.cursor_h.setFrameShape(QFrame.NoFrame)
        self.cursor_h.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.cursor_h.setStyleSheet(
            "background: none; border-top:2px solid #00FF66; border-bottom:2px solid #00FF66;"
        )
        grid.addWidget(self.cursor_h, self.cursor_row, 0, 1, COLS)

        self.cursor_v = QFrame()
        self.cursor_v.setFrameShape(QFrame.NoFrame)
        self.cursor_v.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.cursor_v.setStyleSheet("background: none; border:2px solid yellow;")
        grid.addWidget(self.cursor_v, 0, self.current_col, ROWS, 1)

        self.error_frame = QFrame()
        self.error_frame.setFrameShape(QFrame.NoFrame)
        self.error_frame.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.error_frame.setStyleSheet("background: none; border:3px solid red;")
        self.error_frame.hide()
        grid.addWidget(self.error_frame, 0, 0, ROWS, 1)

        main_layout.addWidget(grid_frame, alignment=Qt.AlignCenter)

        button_layout = QHBoxLayout()
        self.validate_btn = QPushButton("VALIDER")
        self.validate_btn.setFont(QFont("Consolas", 14, QFont.Bold))
        self.validate_btn.setStyleSheet("""
            QPushButton {
                background-color:#002200;
                color:#00FF66;
                border:2px solid #00FF66;
                padding:8px 30px;
            }
            QPushButton:hover { background-color:#004400; }
            QPushButton:pressed { background-color:#006600; }
        """)
        self.validate_btn.clicked.connect(self.select_letter)
        button_layout.addStretch()
        button_layout.addWidget(self.validate_btn)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

    # ------------------ CLAVIER ------------------
    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return

        if event.key() == Qt.Key_Left:
            self.current_col = max(0, self.current_col - 1)
            self.update_cursor()

        elif event.key() == Qt.Key_Right:
            self.current_col = min(COLS - 1, self.current_col + 1)
            self.update_cursor()

        elif event.key() in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter):
            self.select_letter()

    def update_cursor(self):
        parent_layout = self.cursor_v.parent().layout()
        parent_layout.addWidget(self.cursor_v, 0, self.current_col, ROWS, 1)

            self.columns.append(letters)
            self.target_indices.append(target_index)
