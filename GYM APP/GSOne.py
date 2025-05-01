from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUi
import cx_Oracle
import resources

def get_db_connection():
    try:
        dsn = cx_Oracle.makedsn("localhost", "1521", service_name="XE")
        return cx_Oracle.connect(user="SALLE_DE_SPORT", password="root", dsn=dsn)
    except Exception as e:
        QMessageBox.critical(window, "Error", f"Could not connect to database: {e}")
        return None

def save_workout_plan(cin):
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO WORKOUT_PLANS (
                MEMBER_CIN,
                PLAN_NAME,
                PURCHASE_DATE,
                EXERCISES,
                SETS,
                REPS,
                REST_TIME
            ) VALUES (
                :1, 'GSOne Beginner', SYSDATE,
                'Leg Press, Seated Cable Curl, Flat Bench Press, Dumbbell Press, ' ||
                'Tricep Pushdown, Barbell Curl, Barbell Wrist Curl, Back Extension',
                '1 set',
                '15 reps',
                '60-90 seconds'
            )
        """, (cin,))
        conn.commit()
        return True
    except Exception as e:
        QMessageBox.critical(window, "Error", f"Failed to save workout: {e}")
        return False
    finally:
        conn.close()

def Buy():
    cin = window.cin.text().strip()
    if not cin:
        QMessageBox.warning(window, "Missing Info", "Please enter your CIN number")
        return
    
    if save_workout_plan(cin):
        QMessageBox.information(
            window, 
            "Success", 
            "          GSOne Workout Plan Bought! \n\nView Coach For Demonstration!"
        )
        window.cin.clear()
    else:
        QMessageBox.warning(window, "Error", "Couldn't complete purchase")

app = QApplication([])
window = loadUi("GSOne.ui")
window.show()
window.confirm.clicked.connect(Buy)
app.exec_()