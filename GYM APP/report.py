from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUi
import cx_Oracle
import resources
from subprocess import run

def load_statistics():
    try:
        connection = cx_Oracle.connect("your_username", "your_password", "localhost/XE")
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM members")
        total_members = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM members WHERE gender = 'Male'")
        male_members = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM members WHERE gender = 'Female'")
        female_members = cursor.fetchone()[0]

        cursor.execute("""
            SELECT first_name || ' ' || last_name, TO_CHAR(join_date, 'DD/MM/YYYY')
            FROM members
            ORDER BY join_date ASC
            FETCH FIRST 1 ROWS ONLY
        """)
        oldest_member, oldest_date = cursor.fetchone()

        cursor.execute("""
            SELECT first_name || ' ' || last_name, TO_CHAR(join_date, 'DD/MM/YYYY')
            FROM members
            ORDER BY join_date DESC
            FETCH FIRST 1 ROWS ONLY
        """)
        newest_member, newest_date = cursor.fetchone()

        cursor.execute("SELECT ROUND(AVG(cost)) FROM members")
        avg_revenue = cursor.fetchone()[0]

        cursor.execute("""
            SELECT subscription_type, COUNT(*) AS count
            FROM members
            GROUP BY subscription_type
            ORDER BY count DESC
            FETCH FIRST 1 ROWS ONLY
        """)
        most_popular_sub, sub_count = cursor.fetchone()

        report_text = f"""Total members: {total_members}
            Male members: {male_members}
            Female members: {female_members}
            Oldest member: {oldest_member} (since {oldest_date})
            Newest member: {newest_member} (since {newest_date})
            Average monthly revenue: {avg_revenue}€
            Most popular subscription: {most_popular_sub} ({sub_count} members)"""

        window.report.setText(report_text)

        cursor.close()
        connection.close()

    except cx_Oracle.DatabaseError as e:
        QMessageBox.critical(window, "Database Error", str(e))
def Back():
    window.close()
    run(["python", "BillReport.py"])

app = QApplication([])
window = loadUi("Report.ui")
window.back.clicked.connect(Back)

load_statistics()

window.show()
app.exec_()
