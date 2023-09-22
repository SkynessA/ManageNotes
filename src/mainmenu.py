from PyQt5 import QtCore, QtGui, QtWidgets
from .addnote import Ui_AddNoteWindow
from .managenote import Ui_ViewNoteWindow
from database import db
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QFontMetrics


class Ui_MainWindow(object):
    '''
        Основной класс управления программой
    '''

    def setupUi(self, MainWindow) -> None:
        '''
            Создание дизайна главного меню

            :return: None
        '''
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.noteListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.noteListWidget.setGeometry(QtCore.QRect(40, 80, 320, 360))
        self.noteListWidget.setObjectName("noteListWidget")

        self.addNote = QtWidgets.QPushButton(self.centralwidget)
        self.addNote.setGeometry(QtCore.QRect(40, 33, 50, 42))
        self.addNote.setObjectName("addNote")
        self.addNote.setText("+")

        self.fieldNote = QtWidgets.QLineEdit(self.centralwidget)
        self.fieldNote.setGeometry(QtCore.QRect(90, 38, 200, 34))
        self.fieldNote.setObjectName("fieldNote")
        self.fieldNote.setPlaceholderText("Введите ключевое слово")

        self.findNote = QtWidgets.QPushButton(self.centralwidget)
        self.findNote.setGeometry(QtCore.QRect(290, 33, 70, 42))
        self.findNote.setObjectName("findNote")
        self.findNote.setText("Найти")

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.addNote.clicked.connect(self.openAddNoteWindow)
        self.noteListWidget.itemClicked.connect(self.openViewNoteWindow)
        self.findNote.clicked.connect(self.searchNotes)

        self.populateNoteList()

    def openAddNoteWindow(self) -> None:
        '''
            Обработка нажатия на кнопку добавить заметку

            :return: None
        '''
        addNoteDialog = QtWidgets.QDialog()
        ui = Ui_AddNoteWindow()
        ui.setupUi(addNoteDialog, self)
        result = addNoteDialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            # Если нажата кнопка сохранить
            self.populateNoteList()

    def populateNoteList(self, search_text=None) -> None:
        '''
            Обновление списка заметок

            :param search_text: Текст поиска заметки.
            :return: None
        '''
        self.noteListWidget.clear()
        notes = db.get_all_notes()

        self.noteListWidget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff
            )

        for note in reversed(notes):
            note_id, title, text = note

            if search_text is not None:
                textnote = f'{title} {text}'
                # Если есть слово для поиска
                if str(search_text).lower() not in str(textnote).lower():
                    # Пропускаем, если совпадения не найдены
                    continue

            item = QListWidgetItem(f"{note_id} - {title}: {text}")
            item.setTextAlignment(QtCore.Qt.AlignLeft)

            font = QtGui.QFont()
            font.setPointSize(14)
            item.setFont(font)

            title_font = QtGui.QFont(font)
            title_font.setBold(True)

            # Делаем максимум 1 строку
            text_lines_content = text.split('\n')[:1]
            text_content = '\n'.join(text_lines_content)

            metrics = QFontMetrics(font)
            text_width_content = metrics.width(text_content)
            list_width_content = self.noteListWidget.width()
            if text_width_content > list_width_content:
                # Добавляем многоточение если текст не вмещается
                text_content = metrics.elidedText(
                    text_content,
                    QtCore.Qt.ElideRight,
                    list_width_content)
            else:
                if len(text.split('\n')) > 1:
                    text_content = str(text_content)+'...'

            # Делаем, чтобы текст показывался максимум в 1 строку для заголовка

            text_lines_header = title.split('\n')[:1]
            text_header = '\n'.join(text_lines_header)

            metrics = QFontMetrics(font)
            text_width_header = metrics.width(text_header)
            list_width_header = self.noteListWidget.width()
            if text_width_header > list_width_header:
                # Если текст не вмещается, добавляем многоточие, обрезаем текст

                text_header = metrics.elidedText(
                    text_header,
                    QtCore.Qt.ElideRight,
                    list_width_header)
            else:
                if len(text.split('\n')) > 1:
                    text_header = str(text_header) + '...'
            item.setText(
                f"{note_id} - {text_header}\n\n{text_content}")

            # Добавляем линию разделения заметок
            line_widget = QtWidgets.QFrame()
            line_widget.setFrameShape(QtWidgets.QFrame.HLine)
            line_widget.setFrameShadow(QtWidgets.QFrame.Sunken)
            line_widget.setFixedHeight(2)
            self.noteListWidget.addItem(item)
            self.noteListWidget.setItemWidget(item, line_widget)

    def openViewNoteWindow(self, item) -> None:
        '''
            Обработка нажатия на элемент списка для просмотра полной заметки

            :return: None
        '''
        note_id = item.text().split(' ')[0].strip()

        # Создаем окно для отображения полной заметки
        viewNoteDialog = QtWidgets.QDialog()
        ui = Ui_ViewNoteWindow()
        ui.setupUi(viewNoteDialog, self, note_id)
        viewNoteDialog.exec_()

    def searchNotes(self) -> None:
        '''
            Поиск заметок по ключевым словам

            :return: None
        '''
        search_text = self.fieldNote.text().strip()
        self.populateNoteList(search_text)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Заметки"))
