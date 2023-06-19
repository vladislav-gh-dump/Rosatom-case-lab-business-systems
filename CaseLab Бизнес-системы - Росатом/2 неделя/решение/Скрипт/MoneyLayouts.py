from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QFrame
from PyQt5.QtGui import QDoubleValidator, QValidator


class MoneyLayout1(QFrame):
    """
    Виджеты для ввода суммы

    input_money Сумма займа
    """

    def __init__(self, parent, command):
        super(MoneyLayout1, self).__init__(parent=parent)

        self.command = command

        # region Widgets

        self.label_money = QLabel("Сумма займа")
        self.input_money = QLineEdit()

        # endregion

        self.input_money.setObjectName("InputMoney")
        self.input_money.setPlaceholderText("1000000.00")

        self.money_validator = QDoubleValidator(1, 1_000_000, 2)
        self.money_validator.setLocale(QLocale("en_US"))
        self.money_validator.setNotation(QDoubleValidator.StandardNotation)
        
        self.input_money.setValidator(self.money_validator)
        self.input_money.textChanged[str].connect(self.command)

        self.input_money.setAlignment((Qt.AlignLeft | Qt.AlignmentFlag.AlignVCenter))

        # region Grid Layout

        self.grid = QGridLayout(self)
        for i in range(6): self.grid.setRowStretch(i, 1)
        for j in range(2): self.grid.setColumnStretch(j, 0)

        self.grid.addWidget(self.label_money, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.input_money, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.grid)

        # endregion

    
    def get_money(self) -> float|None:
        money_text = self.input_money.text()
        try:
            if ("." in money_text): 
                money = float(money_text) 
            else: money = int(money_text)
        except Exception as ex:
            print(ex)
            return None
        return money


    def validate(self, text, pos):
        return self.money_validator.validate(text, pos)
    
    def set_text(self, text):
        self.input_money.setText(text)

    def set_cursor_pos(self, cursor_pos):
        self.input_money.setCursorPosition(cursor_pos)

    def get_cursor_pos(self):
        return self.input_money.cursorPosition()


class MoneyLayout2(QFrame):
    """
    Виджеты для ввода суммы

    input_money Сумма займа
    """

    def __init__(self, parent, command1, command2):
        super(MoneyLayout2, self).__init__(parent=parent)

        self.command1 = command1
        self.command2 = command2

        # region Widgets

        self.label_money1 = QLabel("Сумма займа")
        self.input_money1 = QLineEdit()

        self.label_money2 = QLabel("Сумма частичного гашения")
        self.input_money2 = QLineEdit()

        # endregion

        self.input_money1.setObjectName("InputMoney1")
        self.input_money1.setPlaceholderText("1000000.00")

        self.input_money2.setObjectName("InputMoney2")
        self.input_money2.setPlaceholderText("1000000.00")

        ########################################################### region
        self.money_validator = QDoubleValidator(1, 1_000_000, 2)
        self.money_validator.setLocale(QLocale("en_US"))
        self.money_validator.setNotation(QDoubleValidator.StandardNotation)
        ########################################################### endregion

        self.input_money1.setValidator(self.money_validator)
        self.input_money1.textChanged[str].connect(self.command1)

        self.input_money2.setValidator(self.money_validator)
        self.input_money2.textChanged[str].connect(self.command2)

        self.input_money1.setAlignment((Qt.AlignLeft | Qt.AlignmentFlag.AlignVCenter))
        self.input_money2.setAlignment((Qt.AlignLeft | Qt.AlignmentFlag.AlignVCenter))

        # region Grid Layout

        self.grid = QGridLayout(self)
        for i in range(8): self.grid.setRowStretch(i, 1)
        for j in range(2): self.grid.setColumnStretch(j, 0)

        self.grid.addWidget(self.label_money1, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.input_money1, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.label_money2, 2, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.input_money2, 3, 0, alignment=Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.grid)

        # endregion

    def get_money1(self) -> float | None:
        money_text = self.input_money1.text()
        try:
            if ("." in money_text):
                money = float(money_text)
            else:
                money = int(money_text)
        except Exception as ex:
            print(ex)
            return None
        return money

    def get_money2(self) -> float | None:
        money_text = self.input_money2.text()
        try:
            if ("." in money_text):
                money = float(money_text)
            else:
                money = int(money_text)
        except Exception as ex:
            print(ex)
            return None
        return money

    def validate(self, text, pos):
        return self.money_validator.validate(text, pos)

    def set_text(self, text, num_widget):
        if (num_widget == 1):
            self.input_money1.setText(text)
        if (num_widget == 2):
            self.input_money2.setText(text)

    def set_cursor_pos(self, cursor_pos, num_widget):
        if (num_widget == 1):
            self.input_money1.setCursorPosition(cursor_pos)
        if (num_widget == 2):
            self.input_money2.setCursorPosition(cursor_pos)

    def get_cursor_pos(self, num_widget):
        if (num_widget == 1):
            return self.input_money1.cursorPosition()
        if (num_widget == 2):
            return self.input_money2.cursorPosition()