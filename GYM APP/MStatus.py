from PyQt5.QtWidgets import QApplication , QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
import cx_Oracle
from subprocess import run
import resources

def import_machines():
    try:
        dsn = cx_Oracle.makedsn("localhost","1521",service_name="XE")
        cnx = cx_Oracle.connect(user="SALLE_DE_SPORT",password="0000", dsn = dsn)
        
        cursor= cnx.cursor()
        cursor.execute("select machineid, machinename,machinestatus,lastcheckup, technicianname from machines order by machineid")
        result = cursor.fetchall()
        
        if result:
            window.tableWidget.setRowCount(len(result))

            for row_indx, row_data in enumerate(result):
                for col_indx, col_data in enumerate(row_data):
                    window.tableWidget.setItem(row_indx, col_indx, QTableWidgetItem(str(col_data)))
            cursor.close()
            cnx.close()
        else:
            QMessageBox.information(window, "No Data", "No Data Found !")
            cursor.close()
            cnx.close
    except cx_Oracle.DatabaseError as e:
        QMessageBox.critical(window,"ConnectionError", str(e))
def Back():
    window.close()
    run(["python", "HomePage.py"])
def planning():
    window.close()
    run(["python","PlanCheck.py"])

app = QApplication([])
window =loadUi("MStatus.ui")
window.show()

import_machines()
window.back.clicked.connect(Back)

window.plan.clicked.connect(planning)

app.exec_()