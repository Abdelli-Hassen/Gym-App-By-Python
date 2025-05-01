from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
import cx_Oracle
import resources
from subprocess import run

def search_data():
    cin = window.CIN.text().strip()

    if not cin:
        QMessageBox.warning(window, "Warning", "Please enter a CIN.")
        return

    try:
        connection = cx_Oracle.connect("your_username", "your_password", "localhost/XE")
        cursor = connection.cursor()

        query = """
        SELECT first_name, last_name, email, cin, phone_number, gender, birthday, cost 
        FROM members 
        WHERE cin = :cin
        """
        cursor.execute(query, {'cin': cin})
        result = cursor.fetchall()

        window.memberTable.setRowCount(0)

        for row_num, row_data in enumerate(result):
            window.memberTable.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                window.memberTable.setItem(row_num, col_num, QTableWidgetItem(str(data)))

        cursor.close()
        connection.close()
    except cx_Oracle.DatabaseError as e:
        QMessageBox.critical(window, "Database Error", str(e))
def Back():
    window.close()
    run(["python", "BillReport.py"])
app = QApplication([])
window = loadUi("bill.ui")
window.back.clicked.connect(Back)

window.search.clicked.connect(search_data)

window.show()
app.exec_()
