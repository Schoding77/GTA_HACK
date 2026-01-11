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
