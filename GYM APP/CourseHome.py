from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
from subprocess import run
import resources

def AddCourse():
    window.close()
    run(["python", "AddCourse.py"])

def AddCoach():
    window.close()
    run(["python", "AddCoach.py"])

def SubToCourse():
    window.close()
    run(["python", "SubToCourse.py"])

def SeeSubscribed():
    window.close()
    run(["python", "Subbed.py"])

def Back():
    window.close()
    run(["python", "HomePage.py"])

app = QApplication([])
window = loadUi("CourseHome.ui")
window.show()

window.AddCourse.clicked.connect(AddCourse)
window.AddCoach.clicked.connect(AddCoach)
window.SubToCourse.clicked.connect(SubToCourse)
window.SeeSub.clicked.connect(SeeSubscribed)
window.back.clicked.connect(Back)

app.exec_()