from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUi
import cx_Oracle
from datetime import datetime
import resources

def get_db_connection():
    try:
        dsn = cx_Oracle.makedsn("localhost", "1521", service_name="XE")
        conn = cx_Oracle.connect(user="SALLE_DE_SPORT", password="0000", dsn=dsn)
        return conn
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
            INSERT INTO MEMBER_WORKOUTS (
                CIN,
                PLAN_NAME,
                PURCHASE_DATE,
                EXERCISES,
                SETS,
                REPS,
                REST_TIME
            ) VALUES (
                :1, 'GSTwo Advanced', SYSDATE,
                'Leg Press, Lying Leg Curl, Seated Cable Curl, Flat Bench Press, ' ||
                'Tricep Pushdown, Barbell Curl, Barbell Wrist Curl, Back Extension',
                '2 sets',
                '12 reps',
                '60-90 seconds'
            )
        """, (cin,))
        
        conn.commit()
        return True
        
    except Exception as e:
        QMessageBox.critical(window, "Error", f"Failed to save workout plan: {e}")
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
            "          GSTwo Workout Plan Bought! \n\n" +
            "View Coach For Demonstration!\n\n" +
            "Exercises:\n" +
            "- Leg Press\n- Lying Leg Curl\n- Seated Cable Curl\n" +
            "- Flat Bench Press\n- Tricep Pushdown\n- Barbell Curl\n" +
            "- Barbell Wrist Curl\n- Back Extension\n\n" +
            "2 sets × 12 reps\nRest: 60-90s"
        )
        window.cin.clear()
    else:
        QMessageBox.warning(window, "Error", "Purchase could not be completed")


def test(CIN):
    try:
        dsn = cx_Oracle.makedsn("localhost", "1521", service_name="XE")
        with cx_Oracle.connect(user="GESTION_DE_SALLE", password="0000", dsn=dsn) as cnx:
            with cnx.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM MEMBRE WHERE CIN = :1", (CIN,))
                return cursor.fetchone()[0] > 0
    except cx_Oracle.DatabaseError as e:
        QMessageBox.critical(window, "Erreur", f"Erreur de base de données: {e}")
        return False


app = QApplication([])
window = loadUi("GSTwo.ui") 
window.show()
window.confirm.clicked.connect(Buy)  

app.exec_()