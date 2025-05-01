from PyQt5.QtWidgets import QApplication , QMessageBox
from PyQt5.uic import loadUi
import resources
from subprocess import run
import cx_Oracle


def check_validation():
    LastName = window.LName.text().strip()
    FirstName = window.FName.text().strip()
    Username = window.username.text().strip()
    Password = window.password.text().strip()
    PC = window.CPassword.text().strip()
    mail = window.mail.text().strip()
    male = window.Male.isChecked()
    female = window.Female.isChecked()
    Number = window.PN.text().strip()
    Cin = window.CIN.text().strip()

    if not (LastName and FirstName and Username and Password and PC and mail and Number and Cin):
        QMessageBox.warning(window, "Error", "Fields Required !")
    else:
        if not LastName.isalpha():
            QMessageBox.warning(window, "Error", "Invalid last name address !")
            window.LName.setFocus()
        elif not FirstName.isalpha():
            QMessageBox.warning(window, "Error", "Invalid first name address !")
            window.FName.setFocus()        
        elif len(Number) != 8 or not Number.isdigit()  :
            QMessageBox.warning(window, "Error", "Incorrect Phone number !")
            window.PN.setFocus()
        elif not Cin.isdigit() or len(Cin) != 8:
            QMessageBox.warning(window, "Error", "Incorrect cin number !")
            window.CIN.setFocus()
        elif "@" not in mail or "." not in mail :
            QMessageBox.warning(window, "Error", "Invalid email address ! \nMissing @ or .")
            window.mail.setFocus()
        elif Password != PC:
            QMessageBox.warning(window, "Error", "Password and confirmation do not match!")
            window.password.clear()
            window.CPassword.clear()
            window.password.setFocus()
        elif not male and not female:
            QMessageBox.warning(window, "Error", "Please select a gender!")
        else:
            gender = ""
            if not(female):
                gender = "Male"
            else :
                gender = "Female"            
            try:
                dsn = cx_Oracle.makedsn("localhost", "1521", service_name="XE")
                cnx = cx_Oracle.connect(user="SALLE_DE_SPORT", password="0000", dsn=dsn)
                cursor = cnx.cursor()
                query = "INSERT INTO users (lastname, firstname, username, password, email, gender,cin, phone_number) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)"
                cursor.execute(query, (LastName, FirstName, Username, Password, mail, gender, Cin, Number))
                cnx.commit()
                cursor.close()
                cnx.close()
                QMessageBox.information(window, "Success", "Registration successful !")
            except cx_Oracle.DatabaseError as e:
                QMessageBox.critical(window, "Database Error", str(e))
def login():
    window.close()
    run(["python", "login.py"])

app = QApplication([])
window =loadUi("Signup.ui")
window.show()

window.Signbtn.clicked.connect(check_validation)
window.logbtn.clicked.connect(login)

app.exec_()