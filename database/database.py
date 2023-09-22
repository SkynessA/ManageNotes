import sqlite3


class Database:
    '''
        Класс для работы с базой данных
    '''
    def __init__(self, db_file):
        '''
            Подключение к базе данных.

            :param db_file: Путь до файла базы данных.
        '''
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_note(self, header: str, content: str) -> None:
        '''
            Добавление заметки

            :param header: Заголовок заметки.
            :type header: str
            :param content: Содержание заметки.
            :type content: str
            :return: None
        '''
        self.cursor.execute(
            '''INSERT INTO notes (header, content) VALUES (?, ?)''',
            (header, content,))
        self.connection.commit()

    def get_all_notes(self) -> list:
        '''
            Получение всех заметок

            :return: Возвращает список всех заметок
            :rtype: list
        '''
        self.cursor.execute('''SELECT * FROM notes''')
        result = self.cursor.fetchall()
        return result

    def get_note_by_id(self, note_id) -> list:
        '''
            Получение заметки по айди

            :param note_id: Айди заметки.
            :return: Возвращает список всех заметок
            :rtype: list
        '''
        self.cursor.execute('''SELECT * FROM notes WHERE id = ?''', (note_id,))
        result = self.cursor.fetchall()
        return result[0]

    def delete_note(self, note_id) -> None:
        '''
            Удаление заметки

            :param note_id: Айди заметки.
            :return: None
        '''
        self.cursor.execute(
            'DELETE FROM notes WHERE id = ?',
            (int(note_id),))
        self.connection.commit()
