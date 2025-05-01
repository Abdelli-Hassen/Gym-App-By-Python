from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUi
import cx_Oracle
import resources

def get_db_connection():
    try:
        dsn = cx_Oracle.makedsn("localhost", "1521", service_name="XE")
        return cx_Oracle.connect(user="SALLE_DE_SPORT", password="root", dsn=dsn)
    except Exception as e:
        QMessageBox.critical(window, "Error", f"Database connection failed: {e}")
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
                SETS_REPS,
                REST_TIME,
                WORKOUT_DAYS
            ) VALUES (
                :1, 'GSThree Alternating', SYSDATE,
                'Barbell Curl, Seated Dumbbell Press, Pec Deck Fly, ' ||
                'Single Arm Dumbbell Row, Seated Cable Row, ' ||
                'Flat Dumbbell Press, Dumbbell Lateral Raise, Barbell Wrist Curl',
                'Upper: 1 set × 10-12 reps, Lower: 2 sets × 10-12 reps',
                '60-90 seconds',
                '3 non-consecutive days'
            )
        """, (cin,))
        conn.commit()
        return True
    except Exception as e:
        QMessageBox.critical(window, "Error", f"Failed to save plan: {e}")
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
            "          GSThree Workout Bought!\n\n" +
            "Alternating Workouts on 3 non-consecutive days\n\n" +
            "Upper Body: 1 set × 10-12 reps\n" +
            "Lower Body: 2 sets × 10-12 reps\n" +
            "Rest: 60-90 seconds\n\n" +
            "View Coach For Demonstration!"
        )
        window.cin.clear()
    else:
        QMessageBox.warning(window, "Error", "Purchase failed")

app = QApplication([])
window = loadUi("GSThree.ui")
window.show()
window.confirm.clicked.connect(Buy)
app.exec_()