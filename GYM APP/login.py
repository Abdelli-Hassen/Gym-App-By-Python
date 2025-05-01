from PyQt5.QtWidgets import QApplication , QMessageBox
from PyQt5.uic import loadUi
from subprocess import run

import cx_Oracle

import resources

def check_login():
    username = window.username.text()
    password = window.password.text()
    
    if username == "" or not(username.isalpha()):
        QMessageBox.warning(window, "Login Failed", "Invalid Username.")
    elif password == "":
        QMessageBox.warning(window, "Login Failed", "Invalid Password.")
    else:
        try:
            dsn = cx_Oracle.makedsn("localhost", "1521", service_name="XE")
            cnx = cx_Oracle.connect(user="SALLE_DE_SPORT", password="0000", dsn=dsn)
            
            cursor = cnx.cursor()
            cursor.execute("SELECT * FROM users WHERE username = :1 AND password = :2", (username, password))
            result = cursor.fetchone() 

            if result:
                QMessageBox.information(window, "Login Successful", "Welcome, " + username + " !")
                run(["python"],"HomePage.py")
                cursor.close()
                cnx.close()
            else:
                QMessageBox.warning(window, "Login Failed", "Invalid Credentials.")
                cursor.close()
                cnx.close()
                
        except cx_Oracle.DatabaseError as e:
            QMessageBox.critical(window, "Database Error", str(e))

def signup():
    window.close()
    run(["python", "Signup.py"])
    
app = QApplication([])
window =loadUi("login.ui")
window.show()

window.createAcc.setText('<a href="#" style="text-decoration:none; color: black;">Don\'t Have An Account ?</a>')
window.createAcc.linkActivated.connect(signup)

window.password.setEchoMode(window.password.Password)
window.log.clicked.connect(check_login)

app.exec_()