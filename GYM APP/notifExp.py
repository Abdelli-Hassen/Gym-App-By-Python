from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
import resources

def close():
    window.close()

app = QApplication([])
window =loadUi("NotifExp.ui")
window.show()
window.ok.clicked.connect(close)
app.exec_()