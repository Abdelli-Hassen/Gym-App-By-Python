from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
import cx_Oracle
from subprocess import run
import resources

def connect_db():
    try:
        return cx_Oracle.connect(user="SALLE_DE_SPORT", password="root", dsn="localhost/XE")
    except cx_Oracle.DatabaseError as e:
        QMessageBox.critical(None, "Error", f"Connection failed: {str(e)}")
        return None

def load_courses():
    conn = connect_db()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM registrations WHERE course_id = c.course_id),
                c.course_name,
                i.first_name || ' ' || i.last_name,
                c.max_participants,
                c.day_of_week,
                TO_CHAR(c.start_time, 'HH24:MI')
            FROM courses c
            JOIN coaches i ON c.coach_id = i.coach_id
            ORDER BY c.day_of_week, c.start_time
        """)
        
        window.tab.setRowCount(0)
        headers = ["Subbed", "Courses", "Coaches", "Places", "Days", "Times"]
        window.tab.setColumnCount(len(headers))
        window.tab.setHorizontalHeaderLabels(headers)
        
        for row_num, row_data in enumerate(cursor):
            window.tab.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                window.tab.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        
        window.tab.resizeColumnsToContents()
        
    except cx_Oracle.DatabaseError as e:
        QMessageBox.critical(window, "Error", f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()
def Back():
    window.close()
    run(["python", "CourseHome.py"])
app = QApplication([])
window = loadUi("Subbed.ui")
load_courses()
window.back.clicked.connect(Back)
window.show()
app.exec_()