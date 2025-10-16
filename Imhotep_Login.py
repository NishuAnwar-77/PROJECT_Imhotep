import sys
import mysql.connector
from mysql.connector import errors as db_errors
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QMessageBox, QVBoxLayout, QHBoxLayout, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QCursor

class LoginUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Imhotep Login")
        self.setFixedSize(380, 460)
        self.setStyleSheet("background-color: #f4f5f7;")

        self.card = QFrame(self)
        self.card.setGeometry(60, 60, 260, 330)
        self.card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 18px;
            }
        """)

        # Drop shadow for card
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.card.setGraphicsEffect(shadow)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(14)

        # Title
        title = QLabel("Imhotep")
        title.setFont(QFont("Arial Black", 18))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Subtitle (no box)
        subtitle = QLabel("Log in to your account")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setStyleSheet("color: #555;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Unique Code input
        self.unique_code = QLineEdit()
        self.unique_code.setPlaceholderText("Unique Code")
        self.unique_code.setFixedHeight(38)
        self.unique_code.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding-left: 10px;
                font-size: 11pt;
                background-color: #fff;
            }
            QLineEdit:hover {
                border: 2px solid #1EBE64;
            }
        """)
        layout.addWidget(self.unique_code)

        # Password input
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedHeight(38)
        self.password.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding-left: 10px;
                font-size: 11pt;
                background-color: #fff;
            }
            QLineEdit:hover {
                border: 2px solid #1EBE64;
            }
        """)
        layout.addWidget(self.password)

        # Forgot Password (no box)
        forgot = QLabel("<a href='#' style='color:#007BFF;text-decoration:none;'>Forgot Password?</a>")
        forgot.setFont(QFont("Arial", 9))
        forgot.setAlignment(Qt.AlignLeft)
        forgot.setTextInteractionFlags(Qt.TextBrowserInteraction)
        forgot.setOpenExternalLinks(True)
        layout.addWidget(forgot)

        # Login button (#2475FF)
        self.login_btn = QPushButton("Log In")
        self.login_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_btn.setFixedHeight(40)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #2475FF;
                color: white;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #3C8CFF;
            }
        """)
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)

        # Register + Cancel buttons row
        row = QHBoxLayout()
        row.setSpacing(12)

        self.register_btn = QPushButton("Register")
        self.register_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.register_btn.setFixedHeight(36)
        self.register_btn.setStyleSheet("""
            QPushButton {
                background-color: #1EBE64;
                color: white;
                border-radius: 8px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #2ED97A;
            }
        """)
        row.addWidget(self.register_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancel_btn.setFixedHeight(36)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                border-radius: 8px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #E94B5A;
            }
        """)
        self.cancel_btn.clicked.connect(self.close)
        row.addWidget(self.cancel_btn)

        layout.addLayout(row)

    def show_message(self, title, text, icon=QMessageBox.Information):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.exec_()

    def handle_login(self):
        user = self.unique_code.text().strip()
        pwd = self.password.text().strip()

        if not user or not pwd:
            self.show_message("Input Error", "Please enter both Unique Code and Password.", QMessageBox.Warning)
            return

        config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "imhotep_db",
            "connect_timeout": 5
        }

        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE unique_code=%s AND password=%s LIMIT 1", (user, pwd))
            result = cursor.fetchone()

            if result:
                self.show_message("Success", "Welcome! You’re logged in.", QMessageBox.Information)
            else:
                self.show_message("Error", "Incorrect password or unique code.", QMessageBox.Critical)

            cursor.close()
            conn.close()

        except db_errors.InterfaceError as e:
            self.show_message("Connection Error", f"MySQL connection failed.\n{e}", QMessageBox.Critical)
        except db_errors.ProgrammingError as e:
            self.show_message("Database Error", f"Database/table issue.\n{e}", QMessageBox.Critical)
        except Exception as e:
            self.show_message("Error", f"Unexpected error:\n{e}", QMessageBox.Critical)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginUI()
    win.show()
    sys.exit(app.exec_())
