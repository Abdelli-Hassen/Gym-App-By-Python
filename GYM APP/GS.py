from PyQt5.QtWidgets import QApplication , QMessageBox
from PyQt5.uic import loadUi
from subprocess import run
import resources

def isfloat(s):
    try:
        float(s)
        return True
    except:
        return False


def Calculate():
    MW = window.mw.text().strip()
    CW = window.cw.text().strip()
    
    if MW == "" or isfloat(MW) == False or int(MW) <= 0:
        QMessageBox.warning(window,"Value Error", " Maximum weight is not valid ! ")
    elif CW == "" or isfloat(CW) == False or int(CW) <= 0:
        QMessageBox.warning(window,"Value Error", " Current weight is not valid ! ")
    else:
        if float(MW)/float(CW) < 0.2:
            QMessageBox.information(window, "Result", "Weak !")
            run(["python", "GSOne.py"])
        elif 0.2<= float(MW)/float(CW) <0.6:
            QMessageBox.information(window, "Result", "Intermediate !")
            run(["python", "GSTwo.py"])
        elif 0.6<= float(MW)/float(CW) <1:
            QMessageBox.information(window, "Result", "Advanced !")
            run(["python", "GSThree.py"])
        else:
            QMessageBox.information(window, "Result", "Athlete !")
            run(["python", "Buy.py"])
def Back():
    window.close()
    run(["python", "SubHome.py"])
app = QApplication([])
window =loadUi("GSLink.ui")
window.show()
window.back.clicked.connect(Back)

window.confirme.clicked.connect(Calculate)

app.exec_()