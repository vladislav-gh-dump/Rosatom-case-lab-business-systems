from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtWidgets import QFormLayout, QLabel, QLineEdit, QGridLayout, QWidget, QFrame
from PyQt5.QtGui import QDoubleValidator


class PercentagesLayout1(QFrame):
    """
    Виджеты для ввода процентов

    input_pers Процентная ставка
    """

    def __init__(self, parent, command):
        super(PercentagesLayout1, self).__init__(parent=parent)

        self.command = command

        # region Widgets

        self.label_pers = QLabel("Процентная ставка")
        self.input_pers = QLineEdit()

        # endregion

        self.input_pers.setObjectName("InputPers")
        self.input_pers.setPlaceholderText("30.00")

        self.pers_validator = QDoubleValidator(1, 30, 2)
        self.pers_validator.setLocale(QLocale("en_US"))
        self.pers_validator.setNotation(QDoubleValidator.StandardNotation)

        self.input_pers.setValidator(self.pers_validator)
        self.input_pers.textChanged[str].connect(self.command)

        self.input_pers.setAlignment((Qt.AlignLeft | Qt.AlignmentFlag.AlignVCenter))

        # region Grid Layout

        self.grid = QGridLayout(self)
        for i in range(6): self.grid.setRowStretch(i, 1)
        for j in range(2): self.grid.setColumnStretch(j, 0)
        self.grid.addWidget(self.label_pers, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.input_pers, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.grid)

        # endregion

    def get_pers(self) -> float|None:
        pers_text = self.input_pers.text()
        try:
            if ("." in pers_text): 
                pers = float(pers_text) 
            else: pers = int(pers_text)
        except Exception as ex:
            print(ex)
            return None
        return pers
    
    def validate(self, text, pos):
        return self.pers_validator.validate(text, pos)
    
    def set_text(self, text):
        self.input_pers.setText(text)

    def set_cursor_pos(self, cursor_pos):
        self.input_pers.setCursorPosition(cursor_pos)

    def get_cursor_pos(self):
        return self.input_pers.cursorPosition()


class PercentagesLayout2(QFrame):
    """
    Виджеты для ввода процентов

    input_pers1 Процентная ставка\n
    input_pers2 Новая процентная ставка
    """

    def __init__(self, parent, command1, command2):
        super(PercentagesLayout2, self).__init__(parent=parent)

        self.command1 = command1
        self.command2 = command2

        # region Widgets

        self.label_pers1 = QLabel("Процентная ставка")
        self.input_pers1 = QLineEdit()

        self.label_pers2 = QLabel("Новая процентная ставка")
        self.input_pers2 = QLineEdit()

        # endregion

        self.input_pers1.setObjectName("InputPers")
        self.input_pers2.setObjectName("InputPers")
        self.input_pers1.setPlaceholderText("30.00")
        self.input_pers2.setPlaceholderText("30.00")

        self.pers_validator = QDoubleValidator(1, 30, 2)
        self.pers_validator.setLocale(QLocale("en_US"))
        self.pers_validator.setNotation(QDoubleValidator.StandardNotation)

        self.input_pers1.setValidator(self.pers_validator)
        self.input_pers1.textChanged[str].connect(self.command1)
        self.input_pers2.setValidator(self.pers_validator)
        self.input_pers2.textChanged[str].connect(self.command2)

        self.input_pers1.setAlignment((Qt.AlignLeft | Qt.AlignmentFlag.AlignVCenter))
        self.input_pers2.setAlignment((Qt.AlignLeft | Qt.AlignmentFlag.AlignVCenter))

        # region Grid Layout

        self.grid = QGridLayout(self)
        for i in range(8): self.grid.setRowStretch(i, 1)
        for j in range(2): self.grid.setColumnStretch(j, 0)
        self.grid.addWidget(self.label_pers1, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.input_pers1, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.label_pers2, 2, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.input_pers2, 3, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.grid)

        # endregion
        
    def get_pers1(self) -> float|None:
        pers_text = self.input_pers1.text()
        try:
            if ("." in pers_text): 
                pers = float(pers_text) 
            else: pers = int(pers_text)
        except Exception as ex:
            print(ex)
            return None
        return pers
    
    def get_pers2(self) -> float|None:
        pers_text = self.input_pers2.text()
        try:
            if ("." in pers_text): 
                pers = float(pers_text) 
            else: pers = int(pers_text)
        except Exception as ex:
            print(ex)
            return None
        return pers


    def validate(self, text, pos):
        return self.pers_validator.validate(text, pos)
    
    def set_text(self, text, num_widget):
        if (num_widget == 1):
            self.input_pers1.setText(text)
        if (num_widget == 2):
            self.input_pers2.setText(text)

    def set_cursor_pos(self, cursor_pos, num_widget):
        if (num_widget == 1):
            self.input_pers1.setCursorPosition(cursor_pos)
        if (num_widget == 2):
            self.input_pers2.setCursorPosition(cursor_pos)

    def get_cursor_pos(self, num_widget):
        if (num_widget == 1):
            return self.input_pers1.cursorPosition()
        if (num_widget == 2):
            return self.input_pers2.cursorPosition()
