from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from database import db


class Ui_AddNoteWindow(object):
    '''
    Добавление заметок
    '''
    def setupUi(self, addNote, main_window) -> None:
        '''
            Создание меню добавления заметки

            :param addNote: Окно добавления заметки.
            :param main_window: Окно Главного меню.
            :return: None
        '''
        self.main_window = main_window  # Сохраняем экземпляр главного окна

        addNote.setObjectName("addNote")
        addNote.resize(400, 200)
        self.addNote = addNote
        self.addHeader = QtWidgets.QTextEdit(addNote)
        self.addHeader.setGeometry(QtCore.QRect(45, 20, 310, 30))
        self.addHeader.setObjectName("addHeader")
        self.addHeader.setPlaceholderText("Введите заголовок заметки")
        self.addContent = QtWidgets.QTextEdit(addNote)
        self.addContent.setGeometry(QtCore.QRect(45, 60, 310, 90))
        self.addContent.setObjectName("addContent")
        self.addContent.setPlaceholderText("Введите содержание заметки")
        self.saveButton = QtWidgets.QPushButton(addNote)
        self.saveButton.setGeometry(QtCore.QRect(280, 160, 101, 32))
        self.saveButton.setObjectName("saveButton")
        self.cancelButton = QtWidgets.QPushButton(addNote)
        self.cancelButton.setGeometry(QtCore.QRect(180, 160, 101, 32))
        self.cancelButton.setObjectName("cancelButton")

        self.retranslateUi(addNote)
        QtCore.QMetaObject.connectSlotsByName(addNote)

        # Подключение кнопок
        self.saveButton.clicked.connect(self.on_saveButton_clicked)
        self.cancelButton.clicked.connect(self.on_cancelButton_clicked)

    def on_saveButton_clicked(self) -> None:
        '''
            Обработка кнопки "Сохранить"
            Добавление в базу данных значений
            Обновление списка заметок в главном меню

            :return: None
        '''
        header_text = self.addHeader.toPlainText()
        content_text = self.addContent.toPlainText()
        try:
            db.add_note(header_text, content_text)
            QMessageBox.information(
                self.addNote,
                "Успех",
                "Заметка успешно сохранена!",
                QMessageBox.Ok)
            # Вызываем метод обновления списка заметок в главном окне

            self.main_window.populateNoteList()
            self.addNote.close()

        except Exception as e:
            print(e)
            QMessageBox.information(
                self.addNote,
                "Ошибка",
                "Не удалось сохранить заметку!",
                QMessageBox.Ok)

    def on_cancelButton_clicked(self) -> None:
        '''
            Открытие главного меню, обработка кнопки "Отмена"

            :return: None
        '''
        self.addNote.close()

    def retranslateUi(self, addNote):
        _translate = QtCore.QCoreApplication.translate
        addNote.setWindowTitle(_translate("addNote", "Создание заметки"))
        self.saveButton.setText(_translate("addNote", "Сохранить"))
        self.cancelButton.setText(_translate("addNote", "Отмена"))
