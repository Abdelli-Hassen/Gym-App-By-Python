from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
from subprocess import run
import resources
def report():
    window.close()
    run(["python", "report.py"])
    
def bill():
    window.close()
    run(["python", "bill.py"])

def Back():
    window.close()
    run(["python", "HomePage.py"])

app = QApplication([])
window = loadUi("BillReport.ui")
window.show()

window.report.clicked.connect(report)
window.bill.clicked.connect(bill)
window.back.clicked.connect(Back)

app.exec_()