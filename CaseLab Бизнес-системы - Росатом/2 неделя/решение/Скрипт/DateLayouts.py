from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QLabel, QGridLayout, QFrame, QDateEdit


class DateLayout1(QFrame):
    """
    Виджеты для ввода даты

    input_date1 Дата выдачи\n
    input_date2 Дата гашения
    """

    def __init__(self, parent, command):
        super(DateLayout1, self).__init__(parent=parent)

        self.command = command

        # region Widgets

        self.label_date1 = QLabel("Дата выдачи")
        self.input_date1 = QDateEdit(QDate.currentDate())

        self.label_date2 = QLabel("Дата гашения")
        self.input_date2 = QDateEdit(QDate.currentDate())

        # endregion

        # region Widgets Params

        min_date = QDate(2000, 1, 1)
        max_date = QDate(2100, 1, 1)

        self.input_date1.setDateRange(min_date, max_date)
        self.input_date1.setDisplayFormat("dd.MM.yyyy")
        self.input_date1.setCalendarPopup(True)

        self.input_date2.setDateRange(min_date, max_date)
        self.input_date2.setDisplayFormat("dd.MM.yyyy")
        self.input_date2.setCalendarPopup(True)

        # endregion

        self.input_date1.dateChanged.connect(self.command)
        self.input_date2.dateChanged.connect(self.command)

        # region Grid Layout

        self.grid = QGridLayout(self)
        for i in range(8): self.grid.setRowStretch(i, 1)
        for j in range(2): self.grid.setColumnStretch(j, 0)

        self.grid.addWidget(self.label_date1, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.input_date1, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.label_date2, 2, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.input_date2, 3, 0, alignment=Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.grid)

        # endregion

    # region Def Get
    
    def get_date1(self) -> str:
        return self.input_date1.text()
    
    def get_date2(self) -> str:
        return self.input_date2.text()
    
    def get_date_diff(self) -> int|None:
        date1 = self.input_date1.date()
        date2 = self.input_date2.date()
        date_diff_value = date1.daysTo(date2)
        print(f"1 1: {date_diff_value}")
        date_diff_value = date_diff_value if (date_diff_value >= 0) else None
        return date_diff_value
    
    # endregion



class DateLayout2(QFrame):
    """
    Виджеты для ввода даты

    input_date1 Дата выдачи\n
    input_date2 Дата гашения\n
    input_date3 Дата изменения процентной ставки
    """

    def __init__(self, parent, command):
        super(DateLayout2, self).__init__(parent=parent)

        self.command = command

        # region Widgets

        self.label_date1 = QLabel("Дата выдачи")
        self.input_date1 = QDateEdit(QDate.currentDate())

        self.label_date2 = QLabel("Дата гашения")
        self.input_date2 = QDateEdit(QDate.currentDate())

        self.label_date3 = QLabel("Дата изменения процентной ставки")
        self.input_date3 = QDateEdit(QDate.currentDate())

        # endregion

        # region Widgets Params

        min_date = QDate(2000, 1, 1)
        max_date = QDate(2100, 1, 1)

        self.input_date1.setDateRange(min_date, max_date)
        self.input_date1.setDisplayFormat("dd.MM.yyyy")
        self.input_date1.setCalendarPopup(True)

        self.input_date2.setDateRange(min_date, max_date)
        self.input_date2.setDisplayFormat("dd.MM.yyyy")
        self.input_date2.setCalendarPopup(True)

        self.input_date3.setDateRange(min_date, max_date)
        self.input_date3.setDisplayFormat("dd.MM.yyyy")
        self.input_date3.setCalendarPopup(True)

        # endregion

        self.input_date1.dateChanged.connect(self.command)
        self.input_date2.dateChanged.connect(self.command)
        self.input_date3.dateChanged.connect(self.command)

        # region Grid Layout

        self.grid = QGridLayout(self)
        for i in range(10): self.grid.setRowStretch(i, 1)
        for j in range(2): self.grid.setColumnStretch(j, 0)

        self.grid.addWidget(self.label_date1, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.input_date1, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.label_date2, 2, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.input_date2, 3, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.label_date3, 4, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.input_date3, 5, 0, alignment=Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.grid)

        # endregion

    # region Def Get
    
    def get_date1(self):
        return self.input_date1.text()
    
    def get_date2(self):
        return self.input_date2.text()
    
    def get_date3(self):
        return self.input_date3.text()
    
    # endregion

    def get_date_diff1(self) -> int|None:
        date1 = self.input_date1.date()
        date3 = self.input_date3.date()
        date_diff_value = date1.daysTo(date3) - 1
        print(f"2 1: {date_diff_value}")
        date_diff_value = date_diff_value if (date_diff_value >= 0) else None
        return date_diff_value

    def get_date_diff2(self) -> int|None:
        date2 = self.input_date2.date()
        date3 = self.input_date3.date()
        date_diff_value = date3.daysTo(date2) + 1
        print(f"2 2: {date_diff_value}")
        date_diff_value = date_diff_value if (date_diff_value >= 0) else None
        return date_diff_value


class DateLayout3(QFrame):
    """
    Виджеты для ввода даты

    input_date1 Дата выдачи\n
    input_date2 Дата гашения\n
    input_date3 Дата изменения процентной ставки
    """

    def __init__(self, parent, command):
        super(DateLayout3, self).__init__(parent=parent)

        self.command = command

        # region Widgets

        self.label_date1 = QLabel("Дата выдачи")
        self.input_date1 = QDateEdit(QDate.currentDate())

        self.label_date2 = QLabel("Дата гашения")
        self.input_date2 = QDateEdit(QDate.currentDate())

        self.label_date3 = QLabel("Дата изменения процентной ставки")
        self.input_date3 = QDateEdit(QDate.currentDate())

        self.label_date4 = QLabel("Дата частичного гашения")
        self.input_date4 = QDateEdit(QDate.currentDate())

        # endregion

        # region Widgets Params

        min_date = QDate(2000, 1, 1)
        max_date = QDate(2100, 1, 1)

        self.input_date1.setDateRange(min_date, max_date)
        self.input_date1.setDisplayFormat("dd.MM.yyyy")
        self.input_date1.setCalendarPopup(True)

        self.input_date2.setDateRange(min_date, max_date)
        self.input_date2.setDisplayFormat("dd.MM.yyyy")
        self.input_date2.setCalendarPopup(True)

        self.input_date3.setDateRange(min_date, max_date)
        self.input_date3.setDisplayFormat("dd.MM.yyyy")
        self.input_date3.setCalendarPopup(True)

        self.input_date4.setDateRange(min_date, max_date)
        self.input_date4.setDisplayFormat("dd.MM.yyyy")
        self.input_date4.setCalendarPopup(True)

        # endregion

        self.input_date1.dateChanged.connect(self.command)
        self.input_date2.dateChanged.connect(self.command)
        self.input_date3.dateChanged.connect(self.command)
        self.input_date4.dateChanged.connect(self.command)

        # region Grid Layout

        self.grid = QGridLayout(self)
        for i in range(12): self.grid.setRowStretch(i, 1)
        for j in range(2): self.grid.setColumnStretch(j, 0)

        self.grid.addWidget(self.label_date1, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.input_date1, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.label_date2, 2, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.input_date2, 3, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.label_date3, 4, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.input_date3, 5, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.label_date4, 6, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.input_date4, 7, 0, alignment=Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.grid)

        # endregion

    # region Def Get

    def get_date1(self):
        return self.input_date1.text()

    def get_date2(self):
        return self.input_date2.text()

    def get_date3(self):
        return self.input_date3.text()

    def get_date4(self):
        return self.input_date4.text()

    # endregion

    def get_date_diff1(self) -> int|None:
        date1 = self.input_date1.date()
        date3 = self.input_date3.date()
        date4 = self.input_date4.date()

        date_diff_value = date1.daysTo(date4)
        if (date4 >= date3):
            date_diff_value = date1.daysTo(date3) - 1

        print(f"3 1: {date_diff_value}")
        date_diff_value = date_diff_value if (date_diff_value >= 0) else None
        return date_diff_value

    def get_date_diff2(self) -> int | None:
        date3 = self.input_date3.date()
        date4 = self.input_date4.date()

        date_diff_value = date4.daysTo(date3) - 1
        if (date4 >= date3):
            date_diff_value = date3.daysTo(date4) + 1

        print(f"3 2: {date_diff_value}")
        date_diff_value = date_diff_value if (date_diff_value >= 0) else None
        return date_diff_value

    def get_date_diff3(self) -> int | None:
        date2 = self.input_date2.date()
        date3 = self.input_date3.date()
        date4 = self.input_date4.date()

        date_diff_value = date3.daysTo(date2) + 1
        if (date4 >= date3):
            date_diff_value = date4.daysTo(date2)

        print(f"3 3: {date_diff_value}")
        date_diff_value = date_diff_value if (date_diff_value >= 0) else None
        return date_diff_value