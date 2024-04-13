from PyQt5.QtWidgets import QMessageBox


class ErrorMessageBox(QMessageBox):
    def __init__(self, text):
        self.setText(text)
        self.critical()

