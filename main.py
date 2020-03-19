import configparser
import hashlib
import sqlite3
import sys

import configobj
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem, \
    QListWidgetItem, QFileDialog

from auth_form import Ui_Form as Auth_Form
from child_window import Ui_Form as Child_Window
from question_form import Ui_Form as QuestionForm
from teacher_form import Ui_Form as Teacher_Window
from test_create import Ui_Form as Create_Test_Form
from us_create import Ui_Form as User_Create_Form
from us_delete import Ui_Form as User_Delete_Form
from us_list import Ui_Form as Users_List

'''Импорт необходимых библиотек и QTDesigner форм'''


class DialogGenerator:
    '''Класс генерирующий сообщения различных типов'''

    def __init__(self, text, title, types='critical'):
        self.box = QMessageBox()
        if types == 'critical':  # Условие в зависимости от переанного типа сообщения
            self.box.setIcon(QMessageBox.Critical)  # меняющее отображаемуюю иконку
        elif types == 'information':
            self.box.setIcon(QMessageBox.Information)
        elif types == 'text':
            pass
        self.box.setText(text)
        self.box.setWindowTitle(title)

    def get_class(self):  # функция возвращает класс созданного объекта
        return self.box


class User_Delete(QWidget, User_Delete_Form):
    '''Класс отвечающий за работу формы удаления пользователя'''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('images\\icon.png'))  # Устанавлием иконку окна
        self.pushButton.clicked.connect(self.delete)  # Подключаем саму функцию удаления на кнопку 'Удалить'
        self.con = sqlite3.connect('db.db')  # Подключаем бызу данных

    def delete(self):  # Функции отвечающая непосредственно за удаление пользователя
        if self.lineEdit.text() == '' and self.lineEdit_2.text() == '':  # Проверка на выбранный способ удаления
            a = DialogGenerator('Оба поля пусты', 'Ошибка', 'critical').get_class()
            a.show()
            a.exec_()
        elif self.lineEdit_2.text() == '':  # Если поле для удаления по Login пусто
            cur = self.con.cursor()
            # получаем имена пользователей с заданным id
            result = cur.execute("""SELECT * FROM Users
                                                        WHERE id = ?""", (self.lineEdit.text(),)).fetchall()
            if len(result) == 0:  # Проверка 'Был ли найден хоть один пользователь'
                # Создание соответствующего сообщения
                a = DialogGenerator(f'Пользователи с ID {self.lineEdit.text()} не найдены.', 'Ошибка',
                                    'information').get_class()
                a.show()
                a.exec_()
            elif len(result) > 1:  # Проверка на возможное наличие нескольких пользователей
                # Создание соответствующего сообщения
                a = DialogGenerator(f'База данных некорректна', 'Ошибка',
                                    'critical').get_class()
                a.show()
                a.exec_()
            else:
                # Если пройдена проверка по всем условиям
                result = cur.execute("""DELETE from Users
                                        where id = ?""",
                                     (self.lineEdit.text(),)).fetchall()
                self.con.commit()
                # Генерация сообщения об успехе операции
                a = DialogGenerator(f'Пользователь успешно удален', 'Сообщение',
                                    'information').get_class()
                a.show()
                a.exec_()
        else:  # Если поле для удаления по ID пусто и во всех остальных случаях
            cur = self.con.cursor()
            result = cur.execute("""SELECT * FROM Users
                                                        WHERE login = ?""", (self.lineEdit_2.text(),)).fetchall()
            if len(result) == 0:
                # Проверка на наличие пользователя с таким именем
                a = DialogGenerator(f'Пользователи с Именем Пользователя {self.lineEdit_2.text()} не найдены.',
                                    'Ошибка',
                                    'information').get_class()
                a.show()
                a.exec_()
            elif len(result) > 1:
                # Проверка на наличие нескольких пользователей с таким именем
                a = DialogGenerator(f'База данных некорректна', 'Ошибка',
                                    'critical').get_class()
                a.show()
                a.exec_()
            else:
                # Если пройдена проверка по всем условиям
                result = cur.execute("""DELETE from Users
                                        where login = ?""",
                                     (self.lineEdit_2.text(),)).fetchall()
                self.con.commit()
                # Генерация сообщения об успехе
                a = DialogGenerator(f'Пользователь успешно удален', 'Сообщение',
                                    'information').get_class()
                a.show()
                a.exec_()


class User_Create(QWidget, User_Create_Form):
    '''Класс, обеспечивающий работу формы, отвечающей за создание пользователя'''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('images\\icon.png'))  # Устанавлием иконку окна
        # Подключаем функции соответствующим кнопкам
        self.pushButton.clicked.connect(self.creator)
        self.pushButton.clicked.connect(self.deletor)
        # Подключаем бд
        self.con = sqlite3.connect('db.db')

    def deletor(self):  # Функция, отвечающая за запуск формы удаления пользователя
        ex = User_Delete()
        ex.show()

    def creator(self):  # Функция отвечающая за создание пользователя
        if not self.radioButton.isChecked() and not self.radioButton_2.isChecked():
            a = DialogGenerator('Не выбран тип создаваемого пользователя', 'Ошибка', 'critical').get_class()
            a.show()
            a.exec_()
        elif self.lineEdit_3.text() == '':
            a = DialogGenerator('Не введен логин', 'Ошибка', 'critical').get_class()
            a.show()
            a.exec_()
        elif self.lineEdit_4.text() == '':
            a = DialogGenerator('Не введен пароль', 'Ошибка', 'critical').get_class()
            a.show()
            a.exec_()
        else:  # Действия, выполняемые если все условия соблюдены
            cur = self.con.cursor()
            # Получаем кол-во всех пользователей
            length = len(cur.execute("""SELECT * FROM Users""").fetchall())
            teacher = 0
            # Если соответствующая radioButton выбрана, учитель становится равным 1 (Включен)
            if self.radioButton.isChecked():
                teacher = 1
            # Выполняем создание пользователя
            result = cur.execute("""INSERT INTO Users(id, login, password, teacher)
                                    VALUES (?, ?, ?, ?)""",
                                 (length, self.lineEdit_3.text(), hashlib.sha256 \
                                     (self.lineEdit_4.text().encode('utf-8')).hexdigest(),
                                  teacher)).fetchall()
            # Выводим сообщение об успехе операции
            a = DialogGenerator('Пользователь успешно создан', 'Сообщение', 'information').get_class()
            a.show()
            a.exec_()
            # Сохраняем изменения в бд
            self.con.commit()


class CreateForm(QWidget, Create_Test_Form):
    '''Класс, обеспечивающий работу формы
    создания тестов'''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('images\\icon.png'))  # Устанавлием иконку окна
        # Подключаем функцию обновления типа текущего вопроса
        self.listWidget.currentItemChanged.connect(self.update)
        # Подключаем функции соответствующим кнопкам и radioButton
        self.radioButton.clicked.connect(self.oneResultMode)
        self.pushButton_2.clicked.connect(self.save_test)
        self.radioButton_2.clicked.connect(self.moreResultsMode)
        self.pushButton_3.clicked.connect(self.save_ask)
        self.pushButton.clicked.connect(self.delete_ask)
        self.pushButton.setEnabled(False)
        # Создаем общий словарь, для хранения созданных вопросов
        self.asks = {}
        self.radioButton.click()  # Включаем стандартный режим 'Один вариант ответа'

    def delete_ask(self):  # Функция, удаляющая вопрос
        m = self.listWidget.currentItem().text()
        self.listWidget.takeItem([i for i in self.asks.keys()].index(self.listWidget.currentItem().text()) + 1)
        del self.asks[m]

    def save_ask(self):  # Функция, отвечающая за сохранение текущего вопроса в self.asks
        if self.plainTextEdit.document().toRawText() == '':
            # Ошибка, если не введен текст вопроса
            a = DialogGenerator('Не введён текст вопроса', 'Ошибка', 'critical').get_class()
            a.show()
            a.exec_()
        elif self.plainTextEdit.document().toRawText() in [self.asks[i] for i in self.asks]:
            # Ошибка, если данный вопрос уже существует
            a = DialogGenerator('Данный вопрос уже существует', 'Ошибка', 'critical').get_class()
            a.show()
            a.exec_()
        else:  # Действия, выполняемые если все условия соблюдены
            errors = 0
            if self.listWidget.currentItem().text() == 'Новый вопрос':  # Если выбран новый вопрос
                if self.radioButton.isChecked():  # Если выбран первый тип вопроса 'Один вариант ответа'
                    if self.lineEdit_6.text() == '':
                        # Если не введен ответ
                        errors += 1
                        a = DialogGenerator('Не введён ответ', 'Ошибка', 'critical').get_class()
                        a.show()
                        a.exec_()
                    else:
                        # Если соответствует условиям
                        # Сохраняем вопрос в self.asks определенным методом
                        # Для последующего обращения по тексту вопроса
                        self.asks[self.plainTextEdit.document().toRawText()] = {}
                        self.asks[self.plainTextEdit.document().toRawText()][
                            'Ask'] = self.plainTextEdit.document().toRawText()
                        self.asks[self.plainTextEdit.document().toRawText()]['Answer'] = self.lineEdit_6.text()
                        self.asks[self.plainTextEdit.document().toRawText()]['Type'] = 'One'
                elif self.radioButton_2.isChecked():  # Если выбран режим 'Выбор' (Между RadioButton-ами)
                    # Сохраняем вопрос в self.asks определенным способом
                    self.asks[self.plainTextEdit.document().toRawText()] = {}
                    self.asks[self.plainTextEdit.document().toRawText()][
                        'Ask'] = self.plainTextEdit.document().toRawText()
                    self.asks[self.plainTextEdit.document().toRawText()]['Answer'] = []
                    self.asks[self.plainTextEdit.document().toRawText()]['Type'] = 'Two'
                    # Проверяем поля ввода, и сохраняем
                    # Если поле не является пустым
                    if self.lineEdit.text() != '':
                        self.asks[self.plainTextEdit.document().toRawText()]['Answer'].append(
                            [self.lineEdit.text(), self.checkBox.isChecked(), 1])
                    if self.lineEdit_2.text() != '':
                        self.asks[self.plainTextEdit.document().toRawText()]['Answer'].append(
                            [self.lineEdit_2.text(), self.checkBox_5.isChecked(), 5])
                    if self.lineEdit_3.text() != '':
                        self.asks[self.plainTextEdit.document().toRawText()]['Answer'].append(
                            [self.lineEdit_3.text(), self.checkBox_4.isChecked(), 4])
                    if self.lineEdit_4.text() != '':
                        self.asks[self.plainTextEdit.document().toRawText()]['Answer'].append(
                            [self.lineEdit_4.text(), self.checkBox_3.isChecked(), 3])
                    if self.lineEdit_5.text() != '':
                        self.asks[self.plainTextEdit.document().toRawText()]['Answer'].append(
                            [self.lineEdit_5.text(), self.checkBox_2.isChecked(), 2])
                    # Проверяем, был ли введен хоть один ответ
                    if len(self.asks[self.plainTextEdit.document().toRawText()]['Answer']) == 0:
                        a = DialogGenerator('Не добавлен ни один вариант ответа', 'Ошибка', 'critical').get_class()
                        a.show()
                        a.exec_()
                        errors += 1
                        del self.asks[self.plainTextEdit.document().toRawText()]
                    elif True not in [i[1] for i in self.asks[self.plainTextEdit.document().toRawText()]['Answer']]:
                        # Если не добавлен ни один ответ, отмеченный верным
                        a = DialogGenerator('Не добавлен ни один верный вариант ответа', 'Ошибка',
                                            'critical').get_class()
                        a.show()
                        a.exec_()
                        errors += 1
                        del self.asks[self.plainTextEdit.document().toRawText()]
                if errors == 0:  # Если в процессе не возникло ошибок
                    # Добавляем элемент в ListWidget
                    self.listWidget.addItem(QListWidgetItem(self.plainTextEdit.document().toRawText()))
            else:  # Если выбран определенный вопрос для редактирования
                # Выполняем необходимые проверки
                if self.plainTextEdit.document().toRawText() == '':
                    a = DialogGenerator('Не введён текст вопроса', 'Ошибка', 'critical').get_class()
                    a.show()
                    a.exec_()
                elif self.plainTextEdit.document().toRawText() in [self.asks[i] for i in self.asks]:
                    a = DialogGenerator('Данный вопрос уже существует', 'Ошибка', 'critical').get_class()
                    a.show()
                    a.exec_()
                else:
                    # Если проверки пройдены
                    # Задаешь текущему элементу в listWidget новое значение
                    errorser = 0
                    if self.radioButton.isChecked():  # Если выбран режим 'Один ответ'
                        if self.lineEdit_6.text() == '':  # Проверяем, введен ли ответ
                            errorser += 1
                            a = DialogGenerator('Не введён ответ', 'Ошибка', 'critical').get_class()
                            a.show()
                            a.exec_()
                        else:
                            # Сохраняем вопрос в self.asks определенным образом
                            del self.asks[self.listWidget.currentItem().text()]  # Удаляем предыдущюю версию элемента
                            self.asks[self.plainTextEdit.document().toRawText()] = {}
                            self.asks[self.plainTextEdit.document().toRawText()][
                                'Ask'] = self.plainTextEdit.document().toRawText()
                            self.asks[self.plainTextEdit.document().toRawText()]['Answer'] = self.lineEdit_6.text()
                            self.asks[self.plainTextEdit.document().toRawText()]['Type'] = 'One'
                    elif self.radioButton_2.isChecked():  # Если выбран режим 'Выбор'
                        if self.lineEdit.text() == '' and self.lineEdit_2.text() == '' and \
                                self.lineEdit_3.text() == '' and self.lineEdit_4.text() == '' and \
                                self.lineEdit_5.text() == '' and self.lineEdit_6.text() == '':
                            a = DialogGenerator('Не введен ни один ответ', 'Ошибка', 'critical').get_class()
                            a.show()
                            a.exec_()
                            errorser += 1
                        elif not (
                                self.checkBox.isChecked() or self.checkBox_2.isChecked() or self.checkBox_3.isChecked()
                                or self.checkBox_4.isChecked() or self.checkBox_5):
                            a = DialogGenerator('Не введен ни один верный ответ', 'Ошибка', 'critical').get_class()
                            a.show()
                            a.exec_()
                        else:
                            del self.asks[self.listWidget.currentItem().text()]  # Удаляем предыдущюю версию элемента
                            # Сохраняем вопрос в self.asks
                            self.asks[self.plainTextEdit.document().toRawText()] = {}
                            self.asks[self.plainTextEdit.document().toRawText()][
                                'Ask'] = self.plainTextEdit.document().toRawText()
                            self.asks[self.plainTextEdit.document().toRawText()]['Answer'] = []
                            self.asks[self.plainTextEdit.document().toRawText()]['Type'] = 'Two'
                            # Добавляем ответы из непустых полей
                            if self.lineEdit.text() != '':
                                self.asks[self.plainTextEdit.document().toRawText()]['Answer'].append(
                                    [self.lineEdit.text(), self.checkBox.isChecked(), 1])
                            if self.lineEdit_2.text() != '':
                                self.asks[self.plainTextEdit.document().toRawText()]['Answer'].append(
                                    [self.lineEdit_2.text(), self.checkBox_5.isChecked(), 5])
                            if self.lineEdit_3.text() != '':
                                self.asks[self.plainTextEdit.document().toRawText()]['Answer'].append(
                                    [self.lineEdit_3.text(), self.checkBox_4.isChecked(), 4])
                            if self.lineEdit_4.text() != '':
                                self.asks[self.plainTextEdit.document().toRawText()]['Answer'].append(
                                    [self.lineEdit_4.text(), self.checkBox_3.isChecked(), 3])
                            if self.lineEdit_5.text() != '':
                                self.asks[self.plainTextEdit.document().toRawText()]['Answer'].append(
                                    [self.lineEdit_5.text(), self.checkBox_2.isChecked(), 2])
                    if errorser == 0:  # Проверяем на наличие ошибок
                        self.listWidget.currentItem().setText(self.plainTextEdit.document().toRawText())

    def save_test(self):  # Функция, отвечающая за сохранение теста в файл
        # Инициализируем ConfigObj
        config = configobj.ConfigObj(encoding='utf8')
        try:  # Пробуем получить путь сохранения файла.
            # Используем try для избежания возможной ошибки при задании путя
            if len(self.asks) == 0:  # Если не был добавлен ни один вопрос
                a = DialogGenerator('Не добавлен ни один вопррос', 'Ошибка', 'critical').get_class()
                a.show()
                a.exec_()
            else:
                filename = QFileDialog.getSaveFileName()  # Получаем путь для сохранения файла
                config.filename = str(filename[0])  # Задаем путь сохранения
                config['Allуs'] = self.asks
                config.write()
        except:
            # При ошибке выводим соответствующее сообщение
            a = DialogGenerator('Не выбран файл', 'Ошибка', 'critical').get_class()
            a.show()
            a.exec_()

    def update(self):  # Объявляем функцию, выполняемую при изменении текущего типа вопроса
        # Обнуляем поля
        self.plainTextEdit.setPlainText('')
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_6.setText('')
        if self.listWidget.currentItem().text() == 'Новый вопрос':
            # Включаем возможность выбора любого режима
            self.radioButton.setEnabled(True)
            self.radioButton_2.setEnabled(True)
            self.pushButton.setEnabled(False)  # Выключаем возможность удаления вопроса
        else:
            # Если выбран не новый вопрос
            self.pushButton.setEnabled(True)  # Включаем возможность удаления вопроса
            currentItem = self.asks.get(self.listWidget.currentItem().text())
            self.plainTextEdit.setPlainText(currentItem['Ask'])
            if currentItem['Type'] == 'One':
                # Если тип вопроса 'Один ответ'
                self.radioButton_2.setEnabled(False)  # Отключаем возможность включить другой режим
                self.radioButton.setEnabled(True)
                self.lineEdit_6.setText(currentItem['Answer'])  # Задаем полю ответа сохраненное значение
                self.radioButton.click()  # Включаем режим 'Один верный ответ'
            elif currentItem['Type'] == 'Two':
                # Если тип вопроса 'Выбор'
                self.radioButton.setEnabled(False)  # Отключаем возможность включить другой режим
                self.radioButton_2.setEnabled(True)
                self.radioButton_2.click()  # Включаем режим 'Выбор'
                for i in currentItem['Answer']:
                    # Восстанавляем и задаем переменным сохраненные значения
                    if i[2] == 1:
                        self.checkBox.setChecked(i[1])
                        self.lineEdit.setText(i[0])
                    if i[2] == 2:
                        self.checkBox_2.setChecked(i[1])
                        self.lineEdit_5.setText(i[0])
                    if i[2] == 3:
                        self.checkBox_3.setChecked(i[1])
                        self.lineEdit_4.setText(i[0])
                    if i[2] == 4:
                        self.checkBox_4.setChecked(i[1])
                        self.lineEdit_3.setText(i[0])
                    if i[2] == 5:
                        self.checkBox_5.setChecked(i[1])
                        self.lineEdit_2.setText(i[0])

    def oneResultMode(self):  # Функция, настраивающая форму под тип вопроса 'Один вариант ответа'
        self.lineEdit.hide()
        self.lineEdit_2.hide()
        self.lineEdit_3.hide()
        self.lineEdit_4.hide()
        self.lineEdit_5.hide()
        self.checkBox.hide()
        self.checkBox_2.hide()
        self.checkBox_3.hide()
        self.checkBox_4.hide()
        self.checkBox_5.hide()
        self.lineEdit_6.show()

        self.label.hide()
        self.label_2.hide()
        self.label_3.hide()
        self.label_4.hide()
        self.label_5.hide()
        self.label_6.show()

    def moreResultsMode(self):  # Функция, настраивающая форму под тип вопроса 'Выбор'
        self.lineEdit.show()
        self.lineEdit_2.show()
        self.lineEdit_3.show()
        self.lineEdit_4.show()
        self.lineEdit_5.show()
        self.checkBox.show()
        self.checkBox_2.show()
        self.checkBox_3.show()
        self.checkBox_4.show()
        self.checkBox_5.show()
        self.lineEdit_6.hide()
        self.label.show()
        self.label_2.show()
        self.label_3.show()
        self.label_4.show()
        self.label_5.show()
        self.label_6.hide()


class Users_Ls(QWidget, Users_List):
    '''Класс, отвечающий за работу списка пользователей,\
    формы их добавления и удаления'''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('images\\icon.png'))  # Устанавлием иконку окна
        # Подключаемся к бд
        self.con = sqlite3.connect('db.db')
        # Подключаем функцию выполняемую при изменении текущего выбранного элемента, и прочие
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton.clicked.connect(self.save_results)
        self.pushButton_2.clicked.connect(self.user_create)
        self.pushButton_3.clicked.connect(self.user_delete)
        # Объявляем массив, в который будем записывать изменения
        self.modified = {}
        # Объявляем список заголовков, и задаем ему значение None
        self.titles = None
        # Выполняем функцию обновления списка
        self.update_result()

    def user_create(self):  # Функция, отвечающая за запуск формы создания пользователя
        self.ex = User_Create()
        self.ex.show()

    def user_delete(self):  # Функция, отвечающая за запуск формы удаления пользователя
        self.ex = User_Delete()
        self.ex.show()

    def update_result(self):  # Функция, отвечающая за обновление текущей таблицы в TableWidget
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("Select * from Users").fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):  # Функция, вызываемая при изменении элемента в таблице
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, номер строки,  новое значение
        try:
            self.modified[self.titles[item.column()]][item.row()] = item.text()
        except:
            self.modified[self.titles[item.column()]] = {}
            self.modified[self.titles[item.column()]][item.row()] = item.text()

    def save_results(self):  # Функция отвечающая за сохранение изменений в бд
        self.count_errors = 0  # Объявляем счетчик ошиюок
        if self.modified:  # Если есть изменения, выполняются следующие действия
            cur = self.con.cursor()
            # Начинаем перебор измененных значений
            for key in self.modified.keys():  # Key = имя столбца
                for row in self.modified[key]:  # Row = номер строки
                    # Начинаем формирование запроса
                    que = "UPDATE Users SET\n"
                    # В зависимости от изменяемого столбца добавляем в запрос определенным отбразом
                    # отформатированную строку
                    if key == 'password':
                        # Если изменяется пароль то введенное значение шифруется
                        que += "{}='{}'\n".format(key, hashlib.sha256(
                            self.modified[key].get(row).encode('utf-8')).hexdigest())
                    elif key == 'login':
                        # Если вводится логин то проверяется, нет ли в таблица такого же логина на данный момент
                        result = cur.execute("""SELECT * FROM Users
                                                WHERE login = ?""",
                                             (self.modified[key].get(row),)).fetchall()
                        if len(result) == 1:
                            self.count_errors += 1
                            a = DialogGenerator('Пользователь с таким логином уже существует', 'Ошибка',
                                                'critical').get_class()
                            a.show()
                            a.exec_()
                            continue
                        else:
                            que += "{}='{}'\n".format(key, self.modified[key].get(row))
                    elif key == 'id':
                        # Если вводится id то проверяется, нет ли в таблица такого же id на данный момент
                        result = cur.execute("""SELECT * FROM Users
                                                WHERE id = ?""",
                                             (self.modified[key].get(row),)).fetchall()
                        if len(result) == 1:
                            self.count_errors += 1
                            a = DialogGenerator('Пользователь с таким id уже существует', 'Ошибка',
                                                'critical').get_class()
                            a.show()
                            a.exec_()
                            continue
                        else:
                            que += "{}='{}'\n".format(key, self.modified[key].get(row))
                    else:
                        # В остальных стлучаях добавляется строка по типу 'teacher'='1'
                        que += "{}='{}'\n".format(key, self.modified[key].get(row))
                    # Добавляем параметр, выбирающий только определенную строку
                    que += "WHERE ROWID={}\n".format(row)
                    # Выполняем сформированный запрос
                    cur.execute(que)
            # Сохраняем изменения в бд
            self.con.commit()
            # Проверяем были ли найдены ошибки
            # И если да: генерируем сообщение об их количестве
            if self.count_errors == 0:
                a = DialogGenerator('Все изменения применены', 'Сообщение', 'information').get_class()
            else:
                a = DialogGenerator(f'{self.count_errors} изменений не применены', 'Сообщение',
                                    'information').get_class()
            a.show()
            a.exec_()
            # Обновляем таблицу
            self.update_result()


class Child(QWidget, Child_Window):
    '''Класс, отвечающий за отображение и работоспособность всех форм
    связанных с интерфейсом ребенка'''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('images\\icon.png'))  # Устанавлием иконку окна
        # Подключаем соответствующие кнопкам функции
        self.pushButton.clicked.connect(self.run_test)
        self.pushButton_2.clicked.connect(self.exits)

    def run_test(self):  # Функция, отвечающая за запуск формы теста
        self.ex = Formater()

    def exits(self):  # Функция отвечающая за закрытие программы
        sys.exit()


class Test_Result:
    '''Класс, отвечающий за формирование сообщения о результате теста'''

    def __init__(self, answer_user, answer_true):
        # При инициализации принимает два массива: массив с ответами пользователя и правильными ответами
        self.answer_user = answer_user
        self.answer_true = answer_true
        # Начинаем формирование текста результата
        text = 'Результаты теста:\n'
        for i in range(len(answer_user)):
            text += f'Вопрос №{i + 1}\n'
            if self.answer_user[i] == self.answer_true[i]:
                text += f'\t Правильно\n'
            else:
                text += f'\t Неправильно\n'
        # Создаем соответствующее сообщение с текстом результата
        a = DialogGenerator(text, 'Результаты', 'text').get_class()
        a.show()
        a.exec_()


class Formater(QWidget, QuestionForm):
    '''Класс, отвечающий за работу формы вывода вопроса, ивариантов ответа на него'''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('images\\icon.png'))  # Устанавлием иконку окна
        # Побуем открыть файл, в случае ошибки - выводим сообщение
        try:
            path = QFileDialog.getOpenFileName()  # Получаем путь к файлу
            self.path = path  # Сохраняем путь
            self.config = configparser.ConfigParser()  # Инициализируем config
            self.config.read(self.path)
            self.true_answer = []  # Объявляем массив для сохранения верных ответов
            cas = {}  # Объявляем массив для сохранения распарсеных данных
            # Начинаем парсинг и сохранение данных
            count = 0
            for i in self.config.sections():
                count += 1
                if count == 1:
                    pass
                else:
                    if i.encode('cp1251').decode("utf") != 'Alls':  # Указываем расшифровку из cp1251 в utf
                        cas[i.encode('cp1251').decode("utf")] = {}  # Во всех строчках
                        for j in self.config[i].keys():
                            cas[i.encode('cp1251').decode("utf")][j] \
                                = self.config[i][j].encode('cp1251').decode("utf")
            for i in cas:
                if '"' in cas[i]['answer']:
                    answers = []
                    for i in ''.join(cas[i]['answer'].split('"'))[1:-1].split('], ['):
                        answers.append('True' in i)
                    self.true_answer.append(answers)
                else:
                    self.true_answer.append(cas[i]['answer'])
            # Запускаем функцию начала и работы теста
            self.start(cas)
        except:
            # В случае ошибки выводим сообщение и завершаем исполнение программы
            a = DialogGenerator('Не выбран файл').get_class()
            a.show()
            a.exec_()
            self.close()

    def start(self, asker):  # ункция начала и выполнения теста
        # Объявляем необходимые переменные
        self.asker = asker  # Массив переданных данных
        self.count = 0  # Номер текущего вопроса
        self.config = configparser.ConfigParser()  # Сохраняем инициализованный экземпляр конфига
        self.pushButton.clicked.connect(self.continues)  # Подключаем фунцию записи результатов
        self.asks = [i for i in asker]  # Сохраняем заголовки вопросов
        self.answer = []  # Массив для записи ответов пользователя
        # Выполняем первичное задание элементам их значений из дапнных
        self.label.setText(self.asker[self.asks[self.count]]['ask'])  # Задаем текст вопроса
        if self.asker[self.asks[self.count]]['type'] == 'One':  # Если тип вопроса 'Один вариант ответа'
            self.oneResultMode()  # Запускаем функцию настройки формы под наш тип вопроса
        else:
            checkboxes = []  # Массив с номерами существующих чекбоксов
            for i in ''.join(self.asker[self.asks[self.count]]['answer'].split('"'))[1:-1].split('], ['):
                # Перебираем значения правильно разделенного ответа
                if int(i[-1]) == 1:
                    self.checkBox.setText(i.split('\'')[1])
                    checkboxes.append(1)
                elif int(i[-1]) == 2:
                    self.checkBox_2.setText(i.split('\'')[1])
                    checkboxes.append(2)
                elif int(i[-1]) == 3:
                    self.checkBox_3.setText(i.split('\'')[1])
                    checkboxes.append(3)
                elif int(i[-1]) == 4:
                    self.checkBox_4.setText(i.split('\'')[1])
                    checkboxes.append(4)
                elif int(i[-1]) == 5:
                    self.checkBox_5.setText(i.split('\'')[1])
                    checkboxes.append(5)
            self.moreResultMode(checkboxes)  # Настаиваем форму под наш тип вопроса, передаем
            # список существующих чекбоксов
        # Отображаем настроенную форму
        self.show()

    def setter(self):  # Функция, задающая чекбоксам и лэйблу нужные значения
        # Функция работает также, как и первичная
        self.label.setText(self.asker[self.asks[self.count]]['ask'])
        if self.asker[self.asks[self.count]]['type'] == 'One':
            self.oneResultMode()
        else:
            checkboxes = []
            for i in ''.join(self.asker[self.asks[self.count]]['answer'].split('"'))[1:-1].split('], ['):
                if int(i[-1]) == 1:
                    self.checkBox.setText(i.split('\'')[1])
                    checkboxes.append(1)
                elif int(i[-1]) == 2:
                    self.checkBox_2.setText(i.split('\'')[1])
                    checkboxes.append(2)
                elif int(i[-1]) == 3:
                    self.checkBox_3.setText(i.split('\'')[1])
                    checkboxes.append(3)
                elif int(i[-1]) == 4:
                    self.checkBox_4.setText(i.split('\'')[1])
                    checkboxes.append(4)
                elif int(i[-1]) == 5:
                    self.checkBox_5.setText(i.split('\'')[1])
                    checkboxes.append(5)
            self.moreResultMode(checkboxes)

    def continues(self):  # Функция, считывающая и сохраняющая значения
        if not self.count > len(self.asks) - 1:  # Если номер вопроса не превысил максимальный существующий
            if self.asker[self.asks[self.count]]['type'] == 'One':  # Если тип вопроса 'Один правильный ответ'
                self.answer.append(self.lineEdit.text())  # Добавляем считанный ответ в список ответов пользователя
            else:
                tek_result = []  # Массив данных, считанных с чекбоксов
                for i in ''.join(self.asker[self.asks[self.count]]['answer'].split('"'))[1:-1].split('], ['):
                    if int(i[-1]) == 1:  # Если в i упомянут 1-й чекбокс
                        tek_result.append(self.checkBox.isChecked())
                    elif int(i[-1]) == 2:
                        tek_result.append(self.checkBox_2.isChecked())
                    elif int(i[-1]) == 3:
                        tek_result.append(self.checkBox_3.isChecked())
                    elif int(i[-1]) == 4:
                        tek_result.append(self.checkBox_4.isChecked())
                    elif int(i[-1]) == 5:
                        tek_result.append(self.checkBox_5.isChecked())
                self.answer.append(tek_result)  # В список ответов пользователя сохраняем список ответов с чекбоксов
        self.count += 1  # Увеличиваем номер вопроса на 1
        if self.count > len(self.asks) - 1:  # Если номер вопроса превысил максимально возможный
            self.stop()  # Программа вызывает функцию завершения
        else:
            self.setter()  # Иначе снова вызываем функцию задания значений чекбоксам

    def stop(self):  # Функция, завершающая работу программы
        self.hide()  # Скрываем форму с тестом
        ex = Test_Result(self.answer, self.true_answer)  # Инициализируем класс, генерирующий результат, передавая
        # массив с ответами пользователя и истинные ответы

    def oneResultMode(self):  # Функция, настраивающая форму на режим 'Один вариант ответа'
        self.checkBox.hide()
        self.checkBox_2.hide()
        self.checkBox_3.hide()
        self.checkBox_4.hide()
        self.checkBox_5.hide()
        self.lineEdit.show()

    def moreResultMode(self, checkboxes):  # Функция, настраивающая форму на режим 'Выбор'
        self.oneResultMode()
        if 1 in checkboxes:
            self.checkBox.show()
        if 2 in checkboxes:
            self.checkBox_2.show()
        if 3 in checkboxes:
            self.checkBox_3.show()
        if 4 in checkboxes:
            self.checkBox_4.show()
        if 5 in checkboxes:
            self.checkBox_5.show()

        self.lineEdit.hide()


class Teacher(QWidget, Teacher_Window):
    '''Класс, отвечающий за работу всех функций и форм,
    связанных с интерфейсом учителя'''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('images\\icon.png'))  # Устанавлием иконку окна
        # Подключаем кнопкам соответствующие функции
        self.pushButton.clicked.connect(self.users)
        self.pushButton_2.clicked.connect(self.create_test)
        self.pushButton_4.clicked.connect(self.exits)

    def create_test(self):  # Функция, запускающая форму создания теста
        self.ex2 = CreateForm()
        self.ex2.show()

    def users(self):  # Функция, запускающая форму списка пользователей
        self.ex = Users_Ls()
        self.ex.show()

    def exits(self):  # Функция, отвечающая за завершение программы
        sys.exit()


class LoginForm(QWidget, Auth_Form):
    '''Класс, отвечающий за работу формы авторизации'''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('images\\icon.png'))  # Устанавлием иконку окна
        # Подключаем кнопке функцию login
        self.pushButton.clicked.connect(self.login)

    def login(self):  # Функция, отвечающая за авторизацию
        self.con = sqlite3.connect('db.db')  # Подключаем бд
        cur = self.con.cursor()
        result = cur.execute("""SELECT * FROM Users
                                            WHERE login = ?""", (self.lineEdit.text(),)).fetchall()
        if len(result) == 0:  # Если не был найден пользователь
            a = DialogGenerator('Пользователь не найден', 'Ошибка', 'critical').get_class()
            a.show()
            a.exec_()
        elif result[0][2] != hashlib.sha256(self.lineEdit_2.text().encode('utf-8')).hexdigest():
            # Если пароль не верен
            a = DialogGenerator('Не верный пароль', 'Ошибка', 'critical').get_class()
            a.show()
            a.exec_()
        else:
            # Если пройдены все условия
            self.hide()  # Скрываем форму входа
            if result[0][-1] == 1 or result[0][-1] == '1':  # Если включен режим 'учитель'
                self.ex = Teacher()  # Инициализируем класс Teacher
                self.ex.show()
            else:
                self.ex = Child()  # Инициализируем класс Child
                self.ex.show()


app = QApplication(sys.argv)
ex = LoginForm()
ex.show()
sys.exit(app.exec_())
