from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QGridLayout, QPushButton, QFrame, QLineEdit, QGraphicsDropShadowEffect
from PyQt5.QtCore import pyqtSignal


class ResultLayout1(QFrame):
    """
    Виджеты для вывода результата (для вкладок 1, 2)

    output_result Сумма процентов по займу\n
    button_result Кнопка "Рассчитать"\n
    button_report Кнопка "Отчет"
    """

    def __init__(self, parent):
        super(ResultLayout1, self).__init__(parent=parent)

        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(2)
        shadow.setBlurRadius(10)
        self.setGraphicsEffect(shadow)

        # region Widgets

        self.label_result = QLabel("Сумма процентов по займу")
        self.output_result = QLineEdit()

        self.button_result = QPushButton("Рассчитать")
        self.button_report = QPushButton("Отчет")

        # endregion

        self.output_result.setObjectName("OutputResult")
        self.button_result.setObjectName("ButtonResult")
        self.button_report.setObjectName("ButtonReport")

        self.output_result.setReadOnly(True)
        self.output_result.setPlaceholderText("Результат")

        self.output_result.setAlignment((Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter))

        # region Grid Layout

        self.grid = QGridLayout(self)
        for i in range(8): self.grid.setRowStretch(i, 1)
        for j in range(3): self.grid.setColumnStretch(j, 1)
        self.grid.addWidget(self.label_result, 0, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.output_result, 1, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)

        self.grid.addWidget(self.button_result, 2, 0, 1, 2)
        self.grid.addWidget(self.button_report, 3, 0, 3, 3)
        self.setLayout(self.grid)

        # endregion

    def set_result(self, value):
        self.output_result.setText(f"{value}")

    def set_button_result_command(self, command):
        if (command is not None):
            self.button_result.clicked.connect(command)

    def set_button_report_command(self, command):
        if (command is not None):
            self.button_report.clicked.connect(command)

    def set_button_report_enabled(self, value):
        self.button_report.setEnabled(value)


class ResultLayout2(QFrame):
    """
    Виджеты для вывода результата (для вкладок 1, 2)

    output_result Сумма процентов по займу\n
    button_result Кнопка "Рассчитать"\n
    button_report Кнопка "Отчет"
    """

    def __init__(self, parent):
        super(ResultLayout2, self).__init__(parent=parent)

        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(2)
        shadow.setBlurRadius(10)
        self.setGraphicsEffect(shadow)

        # region Widgets

        self.label_result1 = QLabel("Сумма процентов по займу")
        self.output_result1 = QLineEdit()

        self.label_result2 = QLabel("Гашение займа")
        self.output_result2 = QLineEdit()

        self.button_result = QPushButton("Рассчитать")
        self.button_report = QPushButton("Отчет")

        # endregion

        self.output_result1.setObjectName("OutputResult1")
        self.output_result2.setObjectName("OutputResult2")
        self.button_result.setObjectName("ButtonResult2")
        self.button_report.setObjectName("ButtonReport2")

        self.output_result1.setReadOnly(True)
        self.output_result1.setPlaceholderText("Результат1")

        self.output_result2.setReadOnly(True)
        self.output_result2.setPlaceholderText("Результат2")

        self.output_result1.setAlignment((Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter))
        self.output_result2.setAlignment((Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter))

        # region Grid Layout

        self.grid = QGridLayout(self)
        for i in range(9): self.grid.setRowStretch(i, 1)
        for j in range(3): self.grid.setColumnStretch(j, 1)
        self.grid.addWidget(self.label_result1, 0, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.output_result1, 1, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.label_result2, 2, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.output_result2, 3, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.button_result, 4, 0, 1, 2)
        self.grid.addWidget(self.button_report, 5, 0, 4, 3)
        self.setLayout(self.grid)

        # endregion

    def set_result1(self, value):
        self.output_result1.setText(f"{value}")

    def set_result2(self, value):
        self.output_result2.setText(f"{value}")

    def set_button_result_command(self, command):
        if (command is not None):
            self.button_result.clicked.connect(command)

    def set_button_report_command(self, command):
        if (command is not None):
            self.button_report.clicked.connect(command)

    def set_button_report_enabled(self, value):
        self.button_report.setEnabled(value)