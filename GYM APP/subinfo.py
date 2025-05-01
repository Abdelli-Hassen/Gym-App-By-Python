from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
import cx_Oracle
import resources
from datetime import datetime
from subprocess import run

def connect_db():
    try:
        return cx_Oracle.connect("SALLE_DE_SPORT/root@localhost:1521/XE")
    except:
        return None

def show_expired():
    run(["python", "NotifExp.py"])

def load_member_data():
    cin = window.cin.text().strip()
    
    if not cin:
        return
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT expiration_date, payment_status, duration
                FROM members 
                WHERE cin = :cin
            """, {'cin': cin})
            
            data = cursor.fetchone()
            
            if data:
                window.exp.setText(data[0].strftime("%Y-%m-%d"))
                window.duration.setText(str(data[2]))
                window.status.setText(data[1])
                
                if data[0] < datetime.now().date():
                    show_expired()
            else:
                window.label.setText("Member not found")
        except:
            pass
        finally:
            conn.close()
def Back():
    window.close()
    run(["python", "HomePage.py"])
app = QApplication([])
window = loadUi("SubInfo.ui")
window.back.clicked.connect(Back)
window.confirm.clicked.connect(load_member_data)
window.show()
app.exec_()