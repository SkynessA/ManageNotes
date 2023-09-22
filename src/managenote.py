from PyQt5 import QtCore, QtWidgets
from database import db


class Ui_ViewNoteWindow(object):
    '''
        Класс для отображения полной заметки
    '''
    def setupUi(self, ViewNoteWindow, main_window, note_id) -> None:
        '''
            Создание меню управления заметкой

            :param ViewNoteWindow: Окно управления заметкой.
            :param main_window: Окно Главного меню.
            :param note_id: Айди заметки.
            :return: None
        '''
        self.textBrowser = QtWidgets.QTextBrowser()
        self.noteId = note_id
        note = db.get_note_by_id(note_id)

        title = note[1]
        text = note[2]

        self.textBrowser.setHtml(f"""
<!-- Увеличенным размер и жирный текст -->
<b style="font-size: 20px;">{title}</b>

<!-- Увеличенный размер и перенос строк -->
<p style="font-size: 16px; white-space: pre-line;">
    {text}
</p>
""")
        self.ViewNoteWindow = ViewNoteWindow
        self.main_window = main_window

        ViewNoteWindow.setObjectName("ViewNoteWindow")
        ViewNoteWindow.resize(400, 300)

        layout = QtWidgets.QVBoxLayout(ViewNoteWindow)
        layout.addWidget(self.textBrowser)

        # Кнопка "Удалить заметку"
        deleteButton = QtWidgets.QPushButton("Удалить заметку")
        deleteButton.clicked.connect(self.deleteNote)
        layout.addWidget(deleteButton)

        # Кнопка "Закрыть"
        closeButton = QtWidgets.QPushButton("Закрыть")
        closeButton.clicked.connect(ViewNoteWindow.close)
        layout.addWidget(closeButton)

        self.retranslateUi(ViewNoteWindow)
        QtCore.QMetaObject.connectSlotsByName(ViewNoteWindow)

    def deleteNote(self) -> None:
        '''
            Удаление заметки
            Показ окна, подтверждающий удаление заметки

            :return: None
        '''
        db.delete_note(self.noteId)
        self.showSuccessMessage()

    def showSuccessMessage(self) -> None:
        '''
            Настройка окна удаления заметки

            :return: None
        '''
        QtWidgets.QMessageBox.information(
            self.ViewNoteWindow,
            "Успешно",
            "Заметка успешно удалена!",
            QtWidgets.QMessageBox.Ok
        )

        self.main_window.populateNoteList()
        self.ViewNoteWindow.close()

    def acceptSuccessMessage(self) -> None:
        '''
            Обработка закрытия окна после удаления заметки

            :return: None
        '''
        self.ViewNoteWindow.close()

    def retranslateUi(self, ViewNoteWindow):
        _translate = QtCore.QCoreApplication.translate
        ViewNoteWindow.setWindowTitle(_translate(
            "ViewNoteWindow",
            f"Заметка {self.noteId}"))
