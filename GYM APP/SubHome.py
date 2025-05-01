from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
from subprocess import run
import resources

def Credential():
    window.close()
    run(["python", "SubCr.py"])

def GymSession():
    window.close()
    run(["python", "GS.py"])

def Back():
    window.close()
    run(["python", "HomePage.py"])

app = QApplication([])
window = loadUi("SubHome.ui")
window.show()

window.cred.clicked.connect(Credential)
window.GS.clicked.connect(GymSession)
window.back.clicked.connect(Back)

app.exec_()
