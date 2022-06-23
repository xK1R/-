import sys
from PyQt5.QtCore import QFile
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from Final_cipher import *
from check_db import *
import sqlite3


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('WindowQT.ui', self)

        self.pushButton.clicked.connect(self.reg)
        self.pushButton_2.clicked.connect(self.auth)

        self.check_db = CheckThread()
        self.check_db.mysignal.connect(self.signal_handler)

        self.cipher_window = Cipher_window()

    def signal_handler(self, value):
        QtWidgets.QMessageBox.about(self, "Оповещение", value)
        if value == 'Успешная авторизация!':
            self.cipher_window.show()

    def auth(self):
        name = self.lineEdit.text()
        passw = self.lineEdit_2.text()
        self.check_db.thr_login(name, passw)

    def reg(self):
        name = self.lineEdit.text()
        passw = self.lineEdit_2.text()
        self.check_db.thr_register(name, passw)


class Cipher_window(QDialog):
    def __init__(self):
        super(Cipher_window, self).__init__()
        loadUi('Cipher_form.ui', self)

        self.pushButton.clicked.connect(lambda: self.enc_dec_process())
        self.pushButton_3.clicked.connect(lambda: self.save_to_file())
        self.pushButton_2.clicked.connect(lambda: self.database_entry())
        self.pushButton_4.clicked.connect(lambda: self.select_from_database())
        self.pushButton_5.clicked.connect(lambda: self.read_from_file())

    def signal_handler(self, value):
        QtWidgets.QMessageBox.about(self, "Оповещение", value)

    def enc_dec_process(self):
        # selected radiobutton Шифрование
        if self.radioButton.isChecked():
            text = self.lineEdit.text().upper()
            encrypted_text = Playfair_cipher().encryptDecrypt(mode='E', message=text)
            self.lineEdit_2.setText(f'{encrypted_text}')
        # selected radiobutton Дешифрование
        if self.radioButton_2.isChecked():
            text = self.lineEdit.text().upper()
            encrypted_text = Playfair_cipher().encryptDecrypt(mode='D', message=text)
            self.lineEdit_2.setText(f'{encrypted_text}')

    def database_entry(self):
        con = sqlite3.connect(f'handler/encrypted_text.db')
        cur = con.cursor()

        name = self.lineEdit_name.text()
        text = self.lineEdit_3.text()

        cur.execute(f"INSERT INTO encrypted_text (name, text) VALUES ('{name}', '{text}');")
        self.signal_handler('Зашифрованный текст успешно записан в базу данных!')
        con.commit()

        cur.close()
        con.close()

    def select_from_database(self):
        name = self.lineEdit_name.text()
        connection = sqlite3.connect(f'handler/encrypted_text.db')
        cur = connection.cursor()
        sqlquery = f'SELECT * FROM encrypted_text WHERE name="{name}"'

        list_of_rows = list(cur.execute(sqlquery))

        self.tableWidget.setRowCount(len(list_of_rows))
        tablerow = 0
        for row in list_of_rows:
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            tablerow += 1

        connection.close()

    def read_from_file(self):
        some_file = QFileDialog.getOpenFileName(self)[0]
        try:
            f = open(some_file, 'r')
            with f:
                data = f.read()
                self.textEdit.setText(data)

            f.close()
        except FileNotFoundError:
            self.signal_handler('Файл не выбран!')

    def save_to_file(self):
        some_file = QFileDialog.getSaveFileName(self)[0]

        try:
            f = open(some_file, 'w')
            text = self.lineEdit_4.text()
            f.write(text)
            f.close()
        except FileNotFoundError:
            self.signal_handler('Файл не выбран!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.show()
    sys.exit(app.exec_())
