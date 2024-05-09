import sys
import random
import sqlite3

from PyQt5 import uic, Qt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QHBoxLayout, QSizePolicy, QVBoxLayout, \
    QLabel, QMainWindow, QAction, QDialog


class Window(QWidget):
    def __init__(self, record_id):
        super(Window, self).__init__()
        self.times = None
        self.column = None
        self.record_id = record_id
        self.game_over = None
        self.setWindowTitle("Побег из лаборатории")

        self.con = sqlite3.connect("log_pas_rec.db")
        self.cur = self.con.cursor()

        self.N = 9
        self.names = []
        self.bonus = []
        self.board_building()

        self.main = QHBoxLayout(self)
        self.columnin = QVBoxLayout(self)
        self.line = QHBoxLayout(self)
        self.columncount = QVBoxLayout(self)

        self.move_count_name = QLabel(self)
        self.move_count_name.setText('Количество ходов:')
        self.columncount.addWidget(self.move_count_name)
        self.move_count_name.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.move_count = QLineEdit(self)
        self.move_count.setText('0')
        self.move_count.setEnabled(False)
        self.columncount.addWidget(self.move_count)
        self.move_count.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.score_count_name = QLabel(self)
        self.score_count_name.setText('Количество очков:')
        self.columncount.addWidget(self.score_count_name)
        self.score_count_name.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.score_count = QLineEdit(self)
        self.score_count.setText('0')
        self.score_count.setEnabled(False)
        self.columncount.addWidget(self.score_count)
        self.score_count.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.column_last = -1
        self.line_last = 0
        self.board = []
        for line in range(self.N):
            button_row = []
            for column in range(self.N):
                self.current_button = QPushButton(self)
                self.current_button.line = line
                self.current_button.column = column
                self.current_button.times = 0

                # self.board[i].append(self.current_button)

                self.current_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.current_button.setText('')
                self.current_button.setStyleSheet("background-color : white")
                self.current_button.clicked.connect(self.convert)

                # self.board[line][column] = self.current_button
                button_row.append(self.current_button)
                self.line.addWidget(self.current_button)
            self.board.append(button_row)
            self.columnin.addLayout(self.line)
            self.line = QHBoxLayout(self)
        self.count = 0
        self.main.addLayout(self.columnin)
        self.main.addLayout(self.columncount)
        # self.game_over = Game_over(self.move_count.text(), self.score_count.text())

        # self.board[2][3].setStyleSheet("background-color:red")

    def board_building(self):
        for i in range(5):
            self.bonus.append('+1')
        for i in range(3):
            self.bonus.append('-1')
        for i in range(5):
            self.bonus.append('+2')
        for i in range(3):
            self.bonus.append('-1')
        for i in range(3):
            self.bonus.append('+5')
        self.bonus.append('-5')
        for i in range(1):
            self.bonus.append('+10')
        for i in range(self.N * self.N - 21):
            self.bonus.append('')

        random.shuffle(self.bonus)
        for i in range(self.N):
            self.names.append([])
            for j in range(self.N):
                self.names[i].append(self.bonus[i * self.N + j])

    def board_cleaning(self):
        for i in range(self.N):
            for j in range(self.N):
                self.board[i][j].setText('')
                self.board[i][j].setStyleSheet("background-color : white")
        self.line_last = 0
        self.column_last = -1
        self.move_count.setText('0')
        self.score_count.setText('0')

    def convert(self):
        if (self.sender().column == self.column_last
            and abs(self.sender().line - self.line_last) == 1) \
                or (self.sender().line == self.line_last
                    and abs(self.sender().column - self.column_last) == 1):
            if self.column_last >= 0:
                self.board[self.line_last][self.column_last].setStyleSheet("background-color : green")
            self.column_last = self.sender().column
            self.line_last = self.sender().line
            self.sender().setStyleSheet("background-color : green")
            self.sender().setStyleSheet("border :4px solid ;"
                                        "border-color : red;"
                                        "background-color : green")
            self.move_count.setText(str(int(self.move_count.text()) + 1))
            if self.sender().times == 0:
                self.sender().setText(self.names[self.sender().line][self.sender().column])
                s = self.sender().text()
                self.sender().times = 1
                if s != '':
                    if s[0] == '+':
                        self.score_count.setText(str(int(s[1:]) + int(self.score_count.text())))
                    else:
                        self.score_count.setText(str(int(self.score_count.text()) - int(s[1:])))
            if self.sender().line == self.N - 1 and self.sender().column == self.N - 1:
                # self.game_over = Game_over(self.move_count, self.score_count)
                self.game_over = GameOver(self.move_count.text(), self.score_count.text(),
                                          self.record_id)
                self.game_over.exec()
                self.board_building()
                self.board_cleaning()


class RuleWindow(QWidget):
    def __init__(self):
        super(RuleWindow, self).__init__()
        self.setWindowTitle('Правила игры')
        self.info = QLabel(self)
        self.info.setText('Для начала игры нажмите на левую верхнюю кнопку. Ваша цель - добраться '
                          'до правой нижней, двигаясь по соседним по стороне кнопкам. На пути Вас '
                          'будут ждать бонусы, в том чисел и увеличение очков, при этом бонус '
                          'кнопки не видно до нажатия на неё. Итоговой результат складывается из '
                          'количества ходов (чем меньше, тем лучше) и количества очков (чем '
                          'больше, тем лучше. Каждый бонус может быть активирован единожды.'
                          'Подробнее о бонусах можно прочитать, перейдя по кнопке меню основного '
                          'окна.')
        self.info.setWordWrap(True)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.info)


class BonusWindow(QWidget):
    def __init__(self):
        super(BonusWindow, self).__init__()
        self.setWindowTitle('О бонусах')
        self.info = QLabel(self)
        self.info.setText('Бонусы ррдеставляет собой эффект, происходящий в случае '
                          'нажатия на кнопку. Вы можете прочитать названия эффекта на '
                          'кнопке после нажатия. Эффект может быть пустым, может влиять '
                          'на количество очков, как в лучшую так и в худшую сторону. Ваша задача '
                          '- дойти до конца, набрав как можно больше очков. Однако стоит помнить, '
                          'что помимо количества очков на итоговый результат влияет и количество '
                          'ходов, поэтому желательно максимизировать очки, минимизировав ходы.'
                          'Список эффектов:\n'
                          '1) + 1/2/5/10 - увеличение количества очков на соответствующее значение.\n'
                          '2) - 1/2/5 - уменьшение количества очков на соответствующее значение.\n')
        self.info.setWordWrap(True)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.info)


class MainWindow(QMainWindow):
    def __init__(self, record_id):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Побег из лаборатории")
        self.setCentralWidget(Window(record_id))

        self.about_rules = QAction(self)
        self.about_rules.setText('Правила игры')
        self.about_rules.triggered.connect(self.rules)
        self.menuBar().addAction(self.about_rules)
        self.rulewindow = RuleWindow()

        self.about_bonuses = QAction(self)
        self.about_bonuses.setText('О бонусах')
        self.about_bonuses.triggered.connect(self.bonuses)
        self.menuBar().addAction(self.about_bonuses)
        self.bonuswindow = BonusWindow()

    def rules(self):
        self.rulewindow.show()

    def bonuses(self):
        self.bonuswindow.show()


class GameStart(QWidget):
    def __init__(self):
        super(GameStart, self).__init__()
        self.lineEdit_4 = None
        self.lineEdit_3 = None
        self.lineEdit = None
        self.lineEdit_2 = None
        self.pushButton = None
        self.pushButton_2 = None
        self.record_id = None
        self.login_id = None
        self.strlogin = None
        self.result = None
        self.password = None
        self.login = None
        uic.loadUi('game_start.ui', self)

        self.con = sqlite3.connect("log_pas_rec.db")
        self.cur = self.con.cursor()

        self.mainwidow = None
        self.pushButton.clicked.connect(self.reg)
        self.pushButton_2.clicked.connect(self.log)

    def reg(self):
        self.login = (self.lineEdit_2.text(),)
        self.strlogin = self.lineEdit_2.text()
        self.password = self.lineEdit.text()
        self.result = self.cur.execute("""SELECT passwords FROM logins_passwords
                WHERE logins = ?""", self.login).fetchall()
        if len(self.result) == 0:
            self.cur.execute(f"""INSERT INTO logins_passwords(logins, passwords)
             VALUES('{self.strlogin}', '{self.password}')""")
            self.con.commit()
            self.cur.execute("""INSERT INTO records(record)
                         VALUES('0')""")
            self.con.commit()
            self.login_id = self.cur.execute(f"""SELECT id FROM logins_passwords
        WHERE logins = '{self.strlogin}'""").fetchone()[0]
            self.record_id = self.cur.execute(f"""SELECT max(id) FROM records""").fetchone()[0]
            self.cur.execute(f"""INSERT INTO logins_records(id_login, id_record)
                         VALUES('{self.login_id}', '{self.record_id}')""")
            self.con.commit()
            self.mainwidow = MainWindow(self.record_id)
            self.mainwidow.show()
            self.close()
        else:
            self.pushButton.setText('Данный логин уже существует')

    def log(self):
        self.login = (self.lineEdit_3.text(),)
        self.strlogin = self.lineEdit_3.text()
        self.password = self.lineEdit_4.text()
        self.result = self.cur.execute("""SELECT passwords FROM logins_passwords
        WHERE logins = ?""", self.login).fetchall()
        if len(self.result) != 0 and self.password == self.result[0][0]:
            self.login_id = self.cur.execute(f"""SELECT id FROM logins_passwords
                    WHERE logins = '{self.strlogin}'""").fetchone()[0]
            self.record_id = self.cur.execute(f"""SELECT id_record FROM logins_records
                    WHERE id_login = '{self.login_id}'""").fetchone()[0]
            self.mainwidow = MainWindow(self.record_id)
            self.mainwidow.show()
            self.close()
        else:
            self.pushButton.setText('Неправильный логин или пароль')


class GameOver(QDialog):
    def __init__(self, move_count, score_count, record_id):
        super(GameOver, self).__init__()
        self.lineEdit_3 = None
        self.lineEdit_2 = None
        self.lineEdit = None
        self.label = None
        self.verticalLayout = None
        self.lineEdit_4 = None
        uic.loadUi('game_over.ui', self)

        self.con = sqlite3.connect("log_pas_rec.db")
        self.cur = self.con.cursor()

        self.pic = QLabel(self)
        self.verticalLayout.addWidget(self.pic, alignment=Qt.AlignCenter)

        self.pixmap = QPixmap('picture.jpg')
        self.pic.setPixmap(self.pixmap)
        self.pic.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setText(move_count)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_2.setText(score_count)
        self.lineEdit_3.setEnabled(False)
        self.res = 4 * int(score_count) - 3 * int(move_count)
        self.lineEdit_3.setText(str(self.res))
        self.lineEdit_4.setEnabled(False)
        self.rec = int(self.cur.execute(f"""SELECT record FROM records WHERE id = 
        '{record_id}'""").fetchone()[0])
        if self.rec < self.res:
            self.rec = self.res
            self.cur.execute(f"""UPDATE records set 
            record = '{self.rec}' WHERE id = '{record_id}'""")
            self.con.commit()
        self.lineEdit_4.setText(str(self.rec))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameStart()
    ex.show()
    sys.exit(app.exec())
