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

def load_available_courses():
    """Load courses that still have available spots"""
    connection = connect_to_database()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT c.course_id, c.course_name
            FROM courses c
            WHERE (SELECT COUNT(*) FROM registrations 
                  WHERE course_id = c.course_id) < c.max_participants
            ORDER BY c.course_name
        """)
        window.course_combo.clear()
        for course_id, course_name in cursor:
            window.course_combo.addItem(course_name, course_id)
    except cx_Oracle.DatabaseError as e:
        QMessageBox.critical(window, "Error", f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

def register_member():
    """Register a member for the selected course"""
    member_id = window.member_id_input.text().strip()
    course_name = window.course_combo.currentText()
    
    if not member_id or not course_name:
        QMessageBox.warning(window, "Warning", "Please fill all required fields!")
        return
    
    connection = connect_to_database()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM members WHERE member_id = :1", (member_id,))
        if cursor.fetchone()[0] == 0:
            QMessageBox.warning(window, "Error", "Member not found!")
            return
        
        cursor.execute("""
            SELECT course_id, max_participants 
            FROM courses 
            WHERE course_name = :1
        """, (course_name,))
        course_data = cursor.fetchone()
        
        if not course_data:
            QMessageBox.warning(window, "Error", f"Course '{course_name}' not found!")
            return
            
        course_id, max_participants = course_data
        
        cursor.execute("""
            SELECT COUNT(*) FROM registrations 
            WHERE member_id = :1 AND course_id = :2
        """, (member_id, course_id))
        if cursor.fetchone()[0] > 0:
            QMessageBox.warning(window, "Error", "Already registered for this course!")
            return
        
        cursor.execute("""
            SELECT COUNT(*) FROM registrations WHERE course_id = :1
        """, (course_id,))
        if cursor.fetchone()[0] >= max_participants:
            QMessageBox.warning(window, "Error", "No more available spots!")
            return
        
        cursor.execute("""
            INSERT INTO registrations (member_id, course_id, registration_date)
            VALUES (:1, :2, SYSDATE)
        """, (member_id, course_id))
        
        connection.commit()
        QMessageBox.information(window, "Success", "Registration successful!")
        window.member_id_input.clear()
        
    except cx_Oracle.DatabaseError as e:
        QMessageBox.critical(window, "Error", f"Database error: {str(e)}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
def Back():
    window.close()
    run(["python", "CourseHome.py"])
app = QApplication([])
window = loadUi("SubToCourse.ui")

window.sub.clicked.connect(register_member)
load_available_courses()
window.back.clicked.connect(Back)

window.show()
app.exec_()