from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUi
import cx_Oracle
from subprocess import run
import resources

def connect_to_database():
    try:
        return cx_Oracle.connect(user="SALLE_DE_SPORT", password="root", dsn="localhost/XE")
    except cx_Oracle.DatabaseError as e:
        QMessageBox.critical(None, "Error", f"Database connection failed: {str(e)}")
        return None

def load_coaches():
    connection = connect_to_database()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT coach_id, first_name || ' ' || last_name 
            FROM coaches 
            ORDER BY last_name
        """)
        window.coach_combo.clear()
        for coach_id, full_name in cursor:
            window.coach_combo.addItem(full_name, coach_id)
    except cx_Oracle.DatabaseError as e:
        QMessageBox.critical(window, "Error", f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

def add_course():
    course_name = window.course_input.text().strip()
    coach_id = window.coach_combo.currentData()
    day = window.day_combo.currentText()
    time = window.time_edit.time().toString("HH:mm")
    duration = window.duration_spin.value()
    max_participants = window.places_spin.value()
    
    if not course_name or not coach_id:
        QMessageBox.warning(window, "Warning", "Please fill all required fields!")
        return
    
    connection = connect_to_database()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO courses (
                course_name, 
                coach_id, 
                day_of_week, 
                start_time, 
                duration_minutes, 
                max_participants
            ) VALUES (
                :1, :2, :3, TO_TIMESTAMP(:4, 'HH24:MI'), :5, :6
            )
        """, (course_name, coach_id, day, time, duration, max_participants))
        
        connection.commit()
        QMessageBox.information(window, "Success", "Course added successfully!")
        window.course_input.clear()
    except cx_Oracle.DatabaseError as e:
        QMessageBox.critical(window, "Error", f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()
def Back():
    window.close()
    run(["python", "CourseHome.py"])
app = QApplication([])
window = loadUi("AddCourse.ui")
window.Add.clicked.connect(add_course)
load_coaches()
window.back.clicked.connect(Back)
window.show()
app.exec_()