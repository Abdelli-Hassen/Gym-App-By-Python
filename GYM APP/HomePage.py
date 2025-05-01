from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
from subprocess import run
import resources

def Subscriber():
    window.close()
    run(["python", "SubHome.py"])

def Subscription():
    window.close()
    run(["python", "subinfo.py"])

def Course():
    window.close()
    run(["python", "CourseHome.py"])

def Machines():
    window.close()
    run(["python", "MStatus.py"])

def Bill():
    window.close()
    run(["python", "BillReport.py"])

def Deal():
    window.close()
    run(["python", "Buy.py"])

def Logout():
    window.close()
    run(["python", "login.py"])
app = QApplication([])
window = loadUi("Home.ui")
window.show()

window.subr.clicked.connect(Subscriber)
window.subp.clicked.connect(Subscription)
window.course.clicked.connect(Course)
window.machines.clicked.connect(Machines)
window.bills.clicked.connect(Bill)
window.deal.clicked.connect(Deal)
window.logout.clicked.connect(Logout)

app.exec_()
