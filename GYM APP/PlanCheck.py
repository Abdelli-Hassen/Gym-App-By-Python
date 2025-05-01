from PyQt5.QtWidgets import QApplication , QMessageBox
from PyQt5.uic import loadUi
from cx_Oracle import DatabaseError, makedsn, connect
import resources

def plan():
    MID = window.MID.text().strip()
    MName = window.MName.text().strip()
    MStatus = window.MStatus
    
    dateui = window.NextCheck.date()
    datee = dateui.toString("MM/dd/yyyy")
    
    TechName = window.TechName.text().strip()
    
    if MID == "" or MID.isdigit() == False :
        QMessageBox.warning(window, "ValueError", "Please verify your machine's ID !")
    elif MName == "" or MName.isalpha() == False :
        QMessageBox.warning(window, "ValueError", "Please verify your machine's Name !")
    elif MStatus.currentIndex() == 0 :
        QMessageBox.warning(window, "ValueError", "Please verify your machine's Status !")
    elif TechName == "" or not(TechName.isalpha() or TechName.find('_') or TechName.find(' ') ) :
        QMessageBox.warning(window, "ValueError", "Please verify your Technician Name !")
    else:
        try:
            dsn = makedsn("localhost", "1521", service_name="XE")
            cnx = connect(user="SALLE_DE_SPORT", password="0000", dsn=dsn)
            
            cursor = cnx.cursor()
            query = "insert into MACHINES (machineid, machinename, machinestatus, nextcheckup, technicianname) values(:1,:2,:3,:4,:5)"
            cursor.execute(query,(MID, MName, MStatus.currentText(), datee, TechName))
            
            cnx.commit()
            cursor.close()
            cnx.close()
            
            QMessageBox.information(window, "Success", "Planing successful !")
        except DatabaseError as e:
            QMessageBox.critical(window, "Database Error", str(e))
app = QApplication([])
window =loadUi("CheckUp.ui")
window.show()

window.confirm.clicked.connect(plan)

app.exec_()