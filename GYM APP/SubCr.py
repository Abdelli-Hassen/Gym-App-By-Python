from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUi
import cx_Oracle
import resources
from datetime import datetime
from subprocess import run

def connect_db():
    try:
        return cx_Oracle.connect("SALLE_DE_SPORT/root@localhost:1521/XE")
    except Exception as e:
        QMessageBox.critical(window, "Error", f"Cannot connect to database: {e}")
        return None

def clear_add_fields():
    window.cin.clear()
    window.FName.clear()
    window.LName.clear()
    window.mail.clear()
    window.num.clear()
    window.Female.setChecked(False)
    window.Male.setChecked(False)
    window.birthday.setDate(datetime.now())

def add_member():
    cin = window.cin.text().strip()
    fname = window.FName.text().strip()
    lname = window.LName.text().strip()
    email = window.mail.text().strip()
    phone = window.num.text().strip()
    
    if not cin:
        QMessageBox.warning(window, "Error", "CIN is required")
        window.cin.setFocus()
        return
    if not fname:
        QMessageBox.warning(window, "Error", "First name is required")
        window.FName.setFocus()
        return
    if not lname:
        QMessageBox.warning(window, "Error", "Last name is required")
        window.LName.setFocus()
        return
    if not email or '@' not in email:
        QMessageBox.warning(window, "Error", "Valid email is required")
        window.mail.setFocus()
        return
    if not phone or len(phone) < 8 or not phone.isdigit():
        QMessageBox.warning(window, "Error", "Phone needs 8+ digits")
        window.num.setFocus()
        return
    if not window.Female.isChecked() and not window.Male.isChecked():
        QMessageBox.warning(window, "Error", "Select gender")
        return
    
    gender = "Female" if window.Female.isChecked() else "Male"
    birthdate = window.birthday.date().toString("yyyy-MM-dd")
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO MEMBERS VALUES (
                    :1, :2, :3, :4, :5, :6, TO_DATE(:7, 'YYYY-MM-DD'), SYSDATE
                )
            """, (cin, fname, lname, email, phone, gender, birthdate))
            conn.commit()
            QMessageBox.information(window, "Success", "Member added!")
            clear_add_fields()
        except cx_Oracle.DatabaseError as e:
            if "CIN" in str(e):
                QMessageBox.warning(window, "Error", "CIN already exists")
                window.cin.setFocus()
            elif "EMAIL" in str(e):
                QMessageBox.warning(window, "Error", "Email already exists")
                window.mail.setFocus()
            else:
                QMessageBox.critical(window, "Error", f"Database error: {e}")
        finally:
            conn.close()

def search_member():
    cin = window.modifyCIN.text().strip()
    if not cin:
        QMessageBox.warning(window, "Error", "Enter CIN to search")
        return
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM MEMBERS WHERE CIN = :1", (cin,))
            result = cursor.fetchone()
            
            if result:
                window.modifyName.setText(result[1])
                window.modifyLast.setText(result[2])
                window.modifyMail.setText(result[3])
                window.modifyNum.setText(result[4])
                
                if result[5] == "Female":
                    window.modifyFe.setChecked(True)
                else:
                    window.modifyMale.setChecked(True)
                    
                window.modifyBirthday.setDate(datetime.strptime(result[6], "%Y-%m-%d"))
            else:
                QMessageBox.warning(window, "Error", "Member not found")
        except Exception as e:
            QMessageBox.critical(window, "Error", f"Search failed: {e}")
        finally:
            conn.close()

def modify_member():
    cin = window.modifyCIN.text().strip()
    fname = window.modifyName.text().strip()
    lname = window.modifyLast.text().strip()
    email = window.modifyMail.text().strip()
    phone = window.modifyNum.text().strip()
    
    if not cin:
        QMessageBox.warning(window, "Error", "CIN is required")
        return
    
    if not fname:
        QMessageBox.warning(window, "Error", "First name is required")
        window.modifyName.setFocus()
        return
    if not lname:
        QMessageBox.warning(window, "Error", "Last name is required")
        window.modifyLast.setFocus()
        return
    if not email or '@' not in email:
        QMessageBox.warning(window, "Error", "Valid email is required")
        window.modifyMail.setFocus()
        return
    if not phone or len(phone) < 8 or not phone.isdigit():
        QMessageBox.warning(window, "Error", "Phone needs 8+ digits")
        window.modifyNum.setFocus()
        return
    if not window.modifyFe.isChecked() and not window.modifyMale.isChecked():
        QMessageBox.warning(window, "Error", "Select gender")
        return
    
    gender = "Female" if window.modifyFe.isChecked() else "Male"
    birthdate = window.modifyBirthday.date().toString("yyyy-MM-dd")
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE MEMBERS SET
                    FIRST_NAME = :1,
                    LAST_NAME = :2,
                    EMAIL = :3,
                    PHONE = :4,
                    GENDER = :5,
                    BIRTHDATE = TO_DATE(:6, 'YYYY-MM-DD')
                WHERE CIN = :7
            """, (fname, lname, email, phone, gender, birthdate, cin))
            conn.commit()
            QMessageBox.information(window, "Success", "Member updated!")
        except Exception as e:
            QMessageBox.critical(window, "Error", f"Update failed: {e}")
        finally:
            conn.close()

def delete_member():
    cin = window.deleteCIN.text().strip()
    if not cin:
        QMessageBox.warning(window, "Error", "Enter CIN to delete")
        return
    
    if QMessageBox.question(window, "Confirm", "Delete this member?", 
                          QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM MEMBERS WHERE CIN = :1", (cin,))
                conn.commit()
                QMessageBox.information(window, "Success", "Member deleted!")
                window.deleteCIN.clear()
            except Exception as e:
                QMessageBox.critical(window, "Error", f"Delete failed: {e}")
            finally:
                conn.close()

def show_member():
    cin = window.showCIN.text().strip()
    if not cin:
        QMessageBox.warning(window, "Error", "Enter CIN to view")
        return
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM MEMBERS WHERE CIN = :1", (cin,))
            result = cursor.fetchone()
            
            if result:
                window.showName.setText(f"{result[1]} {result[2]}")
                window.showmail.setText(result[3])
                window.showNum.setText(result[4])
                window.showGender.setText(result[5])
                window.showbirthday.setText(result[6])
            else:
                QMessageBox.warning(window, "Error", "Member not found")
        except Exception as e:
            QMessageBox.critical(window, "Error", f"Search failed: {e}")
        finally:
            conn.close()
def Back():
    window.close()
    run(["python", "SubHome.py"])
app = QApplication([])
window = loadUi("SubCr.ui")
window.back.clicked.connect(Back)
window.add.clicked.connect(add_member)
window.search.clicked.connect(search_member)
window.modify.clicked.connect(modify_member)
window.DELETE.clicked.connect(delete_member)
window.print.clicked.connect(show_member)

window.show()
app.exec_()