from sys import argv
from PyQt6.QtWidgets import QApplication
from classes.MainWindow import MainWindow


app = QApplication(argv)
window = MainWindow()
window.show()

app.exec()
