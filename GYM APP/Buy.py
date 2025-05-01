from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUi
import cx_Oracle
from datetime import datetime, timedelta
import sys
import resources
from subprocess import run

def get_db_connection():
    try:
        dsn = cx_Oracle.makedsn("localhost", "1521", service_name="XE")
        conn = cx_Oracle.connect(user="SALLE_DE_SPORT", password="0000", dsn=dsn)
        return conn
    except Exception as e:
        QMessageBox.critical(window, "Error", f"Could not connect to database: {e}")
        return None

def save_purchase(member_id, membership_type, price):
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        start_date = datetime.now()
        if membership_type == "MONTH":
            end_date = start_date + timedelta(days=30)
            months = 1
        else:
            end_date = start_date + timedelta(days=365)
            months = 12
        
        cursor.execute("""
            INSERT INTO ABONNEMENTS (
                ID_MEMBRE, 
                TYPE, 
                DATE_DEBUT, 
                DATE_EXPIRATION, 
                STATUT,
                MONTANT
            ) VALUES (
                :1, :2, :3, :4, 'Active', :5
            )
        """, (member_id, f"{months} Month", start_date, end_date, price))
        
        conn.commit()
        return True
        
    except Exception as e:
        QMessageBox.critical(window, "Error", f"Failed to save purchase: {e}")
        return False
    finally:
        conn.close()

def BuyMonth():
    member_id = window.ID.text().strip()
    if not member_id:
        QMessageBox.warning(window, "Missing Info", "Please enter your member ID")
        return
    
    if save_purchase(member_id, "MONTH", 100):
        QMessageBox.information(window, "Success", 
            "1 Month Membership Bought!\n\n" +
            "Price: $100\n" +
            "See your coach for more details!")
    else:
        QMessageBox.warning(window, "Error", "Purchase could not be completed")

def BuyYear():
    member_id = window.ID.text().strip()
    
    if not member_id:
        QMessageBox.warning(window, "Missing Info", "Please enter your member ID")
        return
    
    if save_purchase(member_id, "YEAR", 1000):
        QMessageBox.information(window, "Success", 
            "1 Year Membership Bought!\n\n" +
            "Price: $1000 (Save $200!)\n" +
            "See your coach for more details!")
    else:
        QMessageBox.warning(window, "Error", "Purchase could not be completed")
def Back():
    window.close()
    run(["python", "HomePage.py"])
    
app = QApplication(sys.argv)
window = loadUi("BuyCourse.ui")
window.show()
window.back.clicked.connect(Back)
window.confirm1.clicked.connect(BuyMonth)
window.confirm2.clicked.connect(BuyYear)

sys.exit(app.exec_())