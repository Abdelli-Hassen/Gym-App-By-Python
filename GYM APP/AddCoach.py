from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUi
import cx_Oracle
import resources
from subprocess import run
def Back():
    window.close()
    run(["python", "CourseHome.py"])
def connect_db():
    try:
        return cx_Oracle.connect(user="GYM", password="root", dsn="localhost/XE")
    except cx_Oracle.DatabaseError as e:
        QMessageBox.critical(None, "Error", f"Database connection failed: {str(e)}")
        return None

def add_coach():
    last_name = window.Lname.text().strip()
    first_name = window.Frame.text().strip()
    id_number = window.CIN.text().strip()
    email = window.Mail.text().strip()
    phone = window.Num.text().strip()

    if not all([id_number, last_name, first_name]):
        QMessageBox.warning(window, "Error", "⚠️ ID Number, Last Name, and First Name are required.")
        return

    try:
        id_num = int(id_number)
        if len(id_number) != 8:
            raise ValueError
    except ValueError:
        QMessageBox.warning(window, "Error", "⚠️ ID Number must be an 8-digit number.")
        return

    if email and '@' not in email:
        QMessageBox.warning(window, "Error", "⚠️ Invalid email format.")
        return

    try:
        with connect_db() as cnx:
            with cnx.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO COACHES (ID_NUMBER, LAST_NAME, FIRST_NAME, EMAIL, PHONE)
                    VALUES (:id_num, :last_name, :first_name, :email, :phone)
                """, {
                    'id_num': id_number,
                    'last_name': last_name,
                    'first_name': first_name,
                    'email': email if email else None,
                    'phone': phone if phone else None
                })
                cnx.commit()

        QMessageBox.information(window, "Success", "Coach added successfully!")
        window.Lname.clear()
        window.Frame.clear()
        window.CIN.clear()
        window.Mail.clear()
        window.Num.clear()

    except cx_Oracle.DatabaseError as e:
        error_obj, = e.args
        if error_obj.code == 1:
            QMessageBox.warning(window, "Error", "⚠️ This coach already exists.")
        elif error_obj.code == 1400:
            QMessageBox.warning(window, "Error", "⚠️ Required fields cannot be empty.")
        else:
            QMessageBox.critical(window, "Error", f"❌ Database error: {error_obj.message}")
    except Exception as e:
        QMessageBox.critical(window, "Error", f"❌ Unexpected error: {str(e)}")

app = QApplication([])
window = loadUi("AddCoach.ui")
window.confirm.clicked.connect(add_coach)
window.back.clicked.connect(Back)
window.show()
app.exec_()