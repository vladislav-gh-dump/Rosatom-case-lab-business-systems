from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFormLayout, QLabel, QLineEdit, QGridLayout, QWidget, QMessageBox

from MoneyLayouts import *
from PercentagesLayouts import *
from DateLayouts import *
from ResultsLayout import *
from ExcelFileDialog import *


class Tab1(QWidget):

    def __init__(self, parent):
        super(Tab1, self).__init__(parent=parent)

        # region Widgets

        self.label_tab = QLabel("Срочный займ")
        self.money_layout = MoneyLayout1(self, self.money_text_change)
        self.pers_layout = PercentagesLayout1(self, self.pers_text_change)
        self.date_layout = DateLayout1(self, self.date_change)
        self.result_layout = ResultLayout1(self)

        # endregion

        # region Widgets Params

        self.label_tab.setAlignment(Qt.AlignCenter)

        self.label_tab.setObjectName("LabelTab1")

        # endregion
        self.result = ""

        self.is_money_text_change = False

        self.is_result = False

        self.result_layout.set_button_result_command(self.calc)
        self.result_layout.set_button_report_command(self.report)


        # region Grid Layout

        self.grid = QGridLayout(self)
        self.grid.setHorizontalSpacing(20)
        self.grid.setVerticalSpacing(20)
        for i in range(16): self.grid.setRowStretch(i, 1)
        for j in range(16): self.grid.setColumnStretch(j, 1)
        self.grid.addWidget(self.label_tab,     2, 4,   2, 8)
        self.grid.addWidget(self.money_layout,   4, 3,   3, 6)
        self.grid.addWidget(self.pers_layout,    4, 9,   3, 4)
        self.grid.addWidget(self.date_layout,    7, 3,   5, 4)
        self.grid.addWidget(self.result_layout, 7, 7,   5, 6)
        self.setLayout(self.grid)

        # endregion

    def calc(self):
        result_values = {}
        result_values_length = 0
        result_text_end = "/100/365"
        formula = ""

        result_values["money"] = self.money_layout.get_money() 
        result_values["date_diff"]  = self.date_layout.get_date_diff()
        result_values["pers"]  = self.pers_layout.get_pers()

        for key in result_values.keys():
            if (result_values[key] is not None):
                result_values_length += 1

        if (result_values_length == 3):
            self.result = round(result_values["money"]*result_values["date_diff"]*result_values["pers"]/100/365, 2)
            self.is_result = True
            self.result_layout.set_button_report_enabled(True)

        if (result_values["money"] is not None):
            if (result_values["money"] < 0):
                result_values["money"] = f'({result_values["money"]})*'
            else:
                result_values["money"] = f'{result_values["money"]}*'
        else:
            result_values["money"] = '₽*'

        if (result_values["date_diff"] is not None):
            if (result_values["date_diff"] < 0):
                result_values["date_diff"] = f'({result_values["date_diff"]})'
            else:
                result_values["date_diff"] = f'{result_values["date_diff"]}'
        else:
            result_values["date_diff"] = 'Days'

        if (result_values["pers"] is not None):
            if (result_values["pers"] < 0):
                result_values["pers"] = f'*({result_values["pers"]})'
            else:
                result_values["pers"] = f'*{result_values["pers"]}'
        else:
            result_values["pers"] = '*%'

        for key in result_values.keys():
            formula += f"{result_values[key]}"
        formula += result_text_end

        if (self.is_result == True):
            self.result_layout.set_result(f"{self.result}")
        else:
            self.result_layout.set_result(f"{formula} ?")

    def money_text_change(self, text):
        cur_text = text.replace(" ", "").replace(",", "")
        cur_cursor_pos = self.money_layout.get_cursor_pos()

        print(self.money_layout.validate(cur_text, -1))
        if (self.money_layout.validate(cur_text, -1)[0] == 2 or cur_text == ""):
            cur_text = cur_text
        elif (self.money_layout.validate(cur_text, -1)[0] == 1):
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]
        else:
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]

        if (cur_text == "."): cur_text = "1"
        if (len(cur_text) > 0):
            if (cur_text[0] == "0"): cur_text = "1"
            if (float(cur_text) > 1_000_000):
                cur_text = "1000000"
            if (float(cur_text) < 1):
                cur_text = "1"

        self.money_layout.set_text(cur_text)
        self.money_layout.set_cursor_pos(cur_cursor_pos)

        self.result_layout.set_result("")
        self.is_result = False

    def pers_text_change(self, text):
        cur_text = text.replace(" ", "").replace(",", "")
        cur_cursor_pos = self.pers_layout.get_cursor_pos()

        print(self.pers_layout.validate(cur_text, -1))
        if (self.pers_layout.validate(cur_text, -1)[0] == 2 or cur_text == ""):
            cur_text = cur_text
        elif (self.pers_layout.validate(cur_text, -1)[0] == 1):
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]
        else:
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]

        if (cur_text == "."): cur_text = "1"
        if (len(cur_text) > 0):
            if (cur_text[0] == "0"): cur_text = "1"
            if (float(cur_text) > 30):
                cur_text = "30"
            if (float(cur_text) < 1):
                cur_text = "1"

        self.pers_layout.set_text(cur_text)
        self.pers_layout.set_cursor_pos(cur_cursor_pos)

        self.result_layout.set_result("")
        self.is_result = False

    def date_change(self):
        self.result_layout.set_result("")
        
        self.is_result = False

    def report(self):
        if (self.is_result):
            data = {
                "Дата выдачи": self.date_layout.get_date1(),
                "Дата гашения": self.date_layout.get_date2(),
                "Сумма займа": self.money_layout.get_money(),
                "Процентная ставка, %": self.pers_layout.get_pers(),
                "Сумма % по займу": self.result
            }

            excel = Excel(default_name="Срочный_займ")
            filename = excel.save_file()
            if (filename != ""):
                excel.load_data(filename=filename, data=data)

                self.result_layout.set_result("")
                self.is_result = False

                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setText(f"Отчет сформирован\nДиректория документа: {filename}")
                msg_box.setWindowTitle("Information MessageBox")
                msg_box.setStandardButtons(QMessageBox.Ok)
                show = msg_box.exec_()

            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("Документ не сохранен")
                msg_box.setWindowTitle("Warning MessageBox")
                msg_box.setStandardButtons(QMessageBox.Ok)
                show = msg_box.exec_()

        else:

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("Для формирования отчета - заполните все поля")
            msg_box.setWindowTitle("Warning MessageBox")
            msg_box.setStandardButtons(QMessageBox.Ok)
            show = msg_box.exec_()


class Tab2(QWidget):

    def __init__(self, parent):
        super(Tab2, self).__init__(parent=parent)

        # region Widgets

        self.label_tab = QLabel("Займ с изменением процентной ставки")
        self.money_layout = MoneyLayout1(self, self.money_text_change)
        self.pers_layout = PercentagesLayout2(self, self.pers_text_change1, self.pers_text_change2)
        self.date_layout = DateLayout2(self, self.date_change)
        self.result_layout = ResultLayout1(self)

        # endregion

        # region Widgets Params

        self.label_tab.setAlignment(Qt.AlignCenter)

        self.label_tab.setObjectName("LabelTab2")

        # endregion
        self.result = ""

        self.is_money_text_change = False

        self.is_result = False

        self.result_layout.set_button_result_command(self.calc)
        self.result_layout.set_button_report_command(self.report)
        

        # region Grid Layout

        self.grid = QGridLayout(self)
        self.grid.setHorizontalSpacing(20)
        self.grid.setVerticalSpacing(20)
        for i in range(16): self.grid.setRowStretch(i, 1)
        for j in range(16): self.grid.setColumnStretch(j, 1)
        self.grid.addWidget(self.label_tab, 2, 4, 2, 8)
        self.grid.addWidget(self.money_layout, 4, 4, 3, 4)
        self.grid.addWidget(self.pers_layout, 4, 8, 3, 4)
        self.grid.addWidget(self.date_layout, 7, 4, 5, 3)
        self.grid.addWidget(self.result_layout, 7, 7, 5, 5)
        self.setLayout(self.grid)

        # endregion

    def calc(self):
        result_values = {}
        result_values_length = 0
        result_text_end = "/100/365"
        formula = ""

        result_values["money"] = self.money_layout.get_money()
        result_values["date_diff1"] = self.date_layout.get_date_diff1()
        result_values["pers1"] = self.pers_layout.get_pers1()
        result_values["date_diff2"] = self.date_layout.get_date_diff2()
        result_values["pers2"] = self.pers_layout.get_pers2()

        for key in result_values.keys():
            if (result_values[key] is not None):
                result_values_length += 1

        if (result_values_length == 5):
            self.result = round(result_values["money"] * (result_values["date_diff1"] * result_values["pers1"] + result_values["date_diff2"] * result_values["pers2"]) / 100 / 365,
                                2)
            self.is_result = True
            self.result_layout.set_button_report_enabled(True)


        if (result_values["money"] is not None):
            if (result_values["money"] < 0):
                result_values["money"] = f'({result_values["money"]})*'
            else:
                result_values["money"] = f'{result_values["money"]}*'
        else:
            result_values["money"] = '₽*'


        if (result_values["date_diff1"] is not None):
            if (result_values["date_diff1"] < 0):
                result_values["date_diff1"] = f'(({result_values["date_diff1"]})*'
            else:
                result_values["date_diff1"] = f'({result_values["date_diff1"]}*'
        else:
            result_values["date_diff1"] = '(Days¹*'


        if (result_values["pers1"] is not None):
            if (result_values["pers1"] < 0):
                result_values["pers1"] = f'({result_values["pers1"]})+'
            else:
                result_values["pers1"] = f'{result_values["pers1"]}+'
        else:
            result_values["pers1"] = '%¹+'


        if (result_values["date_diff2"] is not None):
            if (result_values["date_diff2"] < 0):
                result_values["date_diff2"] = f'({result_values["date_diff2"]})*'
            else:
                result_values["date_diff2"] = f'{result_values["date_diff2"]}*'
        else:
            result_values["date_diff2"] = 'Days²*'


        if (result_values["pers2"] is not None):
            if (result_values["pers2"] < 0):
                result_values["pers2"] = f'({result_values["pers2"]}))'
            else:
                result_values["pers2"] = f'{result_values["pers2"]})'
        else:
            result_values["pers2"] = '%²)'

        for key in result_values.keys():
            formula += f"{result_values[key]}"
        formula += result_text_end

        if (self.is_result == True):
            self.result_layout.set_result(f"{self.result}")
        else:
            self.result_layout.set_result(f"{formula} ?")

    def money_text_change(self, text):
        cur_text = text.replace(" ", "").replace(",", "")
        cur_cursor_pos = self.money_layout.get_cursor_pos()

        print(self.money_layout.validate(cur_text, -1))
        if (self.money_layout.validate(cur_text, -1)[0] == 2 or cur_text == ""):
            cur_text = cur_text
        elif (self.money_layout.validate(cur_text, -1)[0] == 1):
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]
        else:
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]

        if (cur_text == "."): cur_text = "1"
        if (len(cur_text) > 0):
            if (cur_text[0] == "0"): cur_text = "1"
            if (float(cur_text) > 1_000_000):
                cur_text = "1000000"
            if (float(cur_text) < 1):
                cur_text = "1"

        self.money_layout.set_text(cur_text)
        self.money_layout.set_cursor_pos(cur_cursor_pos)


        self.result_layout.set_result("")
        self.is_result = False

    def pers_text_change1(self, text):
        cur_text = text.replace(" ", "").replace(",", "")
        cur_cursor_pos = self.pers_layout.get_cursor_pos(1)

        print(self.pers_layout.validate(cur_text, -1))
        if (self.pers_layout.validate(cur_text, -1)[0] == 2 or cur_text == ""):
            cur_text = cur_text
        elif (self.pers_layout.validate(cur_text, -1)[0] == 1):
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]
        else:
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]

        if (cur_text == "."): cur_text = "1"
        if (len(cur_text) > 0):
            if (cur_text[0] == "0"): cur_text = "1"
            if (float(cur_text) > 30):
                cur_text = "30"
            if (float(cur_text) < 1):
                cur_text = "1"

        self.pers_layout.set_text(cur_text, 1)
        self.pers_layout.set_cursor_pos(cur_cursor_pos, 1)

        self.result_layout.set_result("")
        self.is_result = False

    def pers_text_change2(self, text):
        cur_text = text.replace(" ", "").replace(",", "")
        cur_cursor_pos = self.pers_layout.get_cursor_pos(2)

        print(self.pers_layout.validate(cur_text, -1))
        if (self.pers_layout.validate(cur_text, -1)[0] == 2 or cur_text == ""):
            cur_text = cur_text
        elif (self.pers_layout.validate(cur_text, -1)[0] == 1):
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]
        else:
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]

        if (cur_text == "."): cur_text = "1"
        if (len(cur_text) > 0):
            if (cur_text[0] == "0"): cur_text = "1"
            if (float(cur_text) > 30):
                cur_text = "30"
            if (float(cur_text) < 1):
                cur_text = "1"

        self.pers_layout.set_text(cur_text, 2)
        self.pers_layout.set_cursor_pos(cur_cursor_pos, 2)

        self.result_layout.set_result("")
        self.is_result = False

    def date_change(self):
        self.result_layout.set_result("")
        self.is_result = False


    def report(self):
        if (self.is_result == True):
            data = {
                "Дата выдачи": self.date_layout.get_date1(),
                "Дата гашения": self.date_layout.get_date2(),
                "Сумма займа": self.money_layout.get_money(),
                "Процентная ставка, %": self.pers_layout.get_pers1(),
                "Дата изменения процентной ставки": self.date_layout.get_date3(),
                "Новая процентная ставка, %": self.pers_layout.get_pers2(),
                "Сумма % по займу": self.result
            }

            excel = Excel(default_name="Займ_с_изменением_процентной_ставки")
            filename = excel.save_file()
            if (filename != ""):
                excel.load_data(filename=filename, data=data)

                self.result_layout.set_result("")
                self.is_result = False

                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setText(f"Отчет сформирован\nДиректория документа: {filename}")
                msg_box.setWindowTitle("Information MessageBox")
                msg_box.setStandardButtons(QMessageBox.Ok)
                show = msg_box.exec_()

            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("Документ не сохранен")
                msg_box.setWindowTitle("Warning MessageBox")
                msg_box.setStandardButtons(QMessageBox.Ok)
                show = msg_box.exec_()

        else:

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("Для формирования отчета - заполните все поля")
            msg_box.setWindowTitle("Warning MessageBox")
            msg_box.setStandardButtons(QMessageBox.Ok)
            show = msg_box.exec_()


class Tab3(QWidget):

    def __init__(self, parent):
        super(Tab3, self).__init__(parent=parent)

        # region Widgets

        self.label_tab = QLabel("Займ с досрочным гашением")
        self.money_layout = MoneyLayout2(self, self.money_text_change1, self.money_text_change2)
        self.pers_layout = PercentagesLayout2(self, self.pers_text_change1, self.pers_text_change2)
        self.date_layout = DateLayout3(self, self.date_change)
        self.result_layout = ResultLayout2(self)

        # endregion

        # region Widgets Params

        self.label_tab.setAlignment(Qt.AlignCenter)

        self.label_tab.setObjectName("LabelTab3")

        # endregion
        self.result1 = ""
        self.result2 = ""

        self.is_money_text_change = False

        self.is_result = False

        self.result_layout.set_button_result_command(self.calc)
        self.result_layout.set_button_report_command(self.report)
        

        # region Grid Layout

        self.grid = QGridLayout(self)
        self.grid.setHorizontalSpacing(20)
        self.grid.setVerticalSpacing(20)
        for i in range(16): self.grid.setRowStretch(i, 1)
        for j in range(16): self.grid.setColumnStretch(j, 1)
        self.grid.addWidget(self.label_tab, 2, 4, 2, 8)
        self.grid.addWidget(self.money_layout, 4, 4, 3, 4)
        self.grid.addWidget(self.pers_layout, 4, 8, 3, 4)
        self.grid.addWidget(self.date_layout, 7, 4, 5, 3)
        self.grid.addWidget(self.result_layout, 7, 7, 5, 5)
        self.setLayout(self.grid)

        # endregion

    def calc(self):
        result_values = {}

        result1_values_part1 = []
        result1_values_part2 = []
        result1_values_part3 = []
        result1_values = []
        result2_values = []

        formula1 = ""
        formula2 = ""

        result1 = None
        result2 = None
        result3 = None

        result_values_count = 0
        result1_values_length = 0
        result2_values_length = 0

        result_values["money1"] = self.money_layout.get_money1()
        result_values["money2"] = self.money_layout.get_money2()
        result_values["date_diff1"] = self.date_layout.get_date_diff1()
        result_values["date_diff2"] = self.date_layout.get_date_diff2()
        result_values["date_diff3"] = self.date_layout.get_date_diff3()
        print(f'1: {result_values["date_diff1"]} 2: {result_values["date_diff2"]} 3: {result_values["date_diff3"]}')
        result_values["pers1"] = self.pers_layout.get_pers1()
        result_values["pers2"] = self.pers_layout.get_pers2()

        date3 = self.date_layout.get_date3()
        date4 = self.date_layout.get_date4()

# region result1_values
# region result1_values_part1

        result1_values_part1 = [result_values["money1"], result_values["date_diff1"], result_values["pers1"]]
        for i in result1_values_part1:
            if (i is not None): result1_values_length += 1

        if (result1_values_length == 3):
            print(f"result1_values_part1: {result1_values_part1} [{result1_values_length}]")
            result1 = result_values["money1"] * result_values["date_diff1"] * result_values["pers1"] / 100 / 365
            result_values_count += 1

        result1_values_length = 0
# endregion
# region result1_values_part2

        result1_values_part2 = [result_values["money1"], result_values["money2"], result_values["date_diff2"], result_values["pers1"]]
        for i in result1_values_part2:
            if (i is not None): result1_values_length += 1

        if (result1_values_length == 4):
            print(f"result1_values_part2 (1): {result1_values_part2} [{result1_values_length}]")
# region result1_values_part2 (2)

            result1_values_length = 0
            result1_values_part2 = [date4, date3, result_values["money1"], result_values["date_diff2"], result_values["pers2"]]
            for i in result1_values_part2:
                if (i is not None): result1_values_length += 1

            if (result1_values_length == 5):
                print(f"result1_values_part2 (2): {result1_values_part2} [{result1_values_length}]")
                result2 = (result_values["money1"] - result_values["money2"]) * result_values["date_diff2"] * result_values["pers1"] / 100 / 365
                if (date4 >= date3):
                    result2 = result_values["money1"] * result_values["date_diff2"] * result_values["pers2"] / 100 / 365
                result_values_count += 1

        result1_values_length = 0
# endregion
#endregion
# region result1_values_part3

        result1_values_part3 = [result_values["money1"], result_values["money2"], result_values["date_diff3"], result_values["pers2"]]
        for i in result1_values_part3:
            if (i is not None): result1_values_length += 1

        if (result1_values_length == 4):
            print(f"result1_values_part3: {result1_values_part3} [{result1_values_length}]")
            result3 = (result_values["money1"] - result_values["money2"]) * result_values["date_diff3"] * result_values["pers2"]/100/365
            result_values_count += 1

# endregion
# endregion

        result1_values = [result1, result2, result3]
        symbs = ["¹", "²", "³"]
        for i in range(len(result1_values)):
            if (result1_values[i] is not None):
                if (result1_values[i] < 0):
                    formula1 += f"({round(result1_values[i], 2)})+"
                else:
                    formula1 += f"{round(result1_values[i], 2)}+"
            else:
                formula1 += f"Sum{symbs[i]}+"
        formula1 = formula1[:-1]

        if (result_values_count == 3):
            self.result1 = round(result1 + result2 + result3, 2)
            self.result_layout.set_result1(f'{self.result1}')
        else:
            self.result_layout.set_result1(f"{formula1} ?")

        # region result2_values

        result2_values = [result_values["money1"], result_values["money2"]]
        for i in range(len(result2_values)):
            if (result2_values[i] is not None):
                result2_values_length += 1
                if (result2_values[i] < 0):
                    formula2 += f"({round(result2_values[i], 2)})-"
                else:
                    formula2 += f"{round(result2_values[i], 2)}-"
            else:
                formula2 += f"₽{symbs[i]}-"
        formula2 = formula2[:-1]


        if (result2_values_length == 2):
            self.result2 = round(result_values["money1"] - result_values["money2"], 2)
            result_values_count += 1
            self.result_layout.set_result2(f'{self.result2}')
        else:
            self.result_layout.set_result2(f"{formula2} ?")

        # endregion

        if (result_values_count == 4):
            self.is_result = True


    def money_text_change1(self, text):
        cur_text = text.replace(" ", "").replace(",", "")
        cur_cursor_pos = self.money_layout.get_cursor_pos(1)

        print(self.money_layout.validate(cur_text, -1))
        if (self.money_layout.validate(cur_text, -1)[0] == 2 or cur_text == ""):
            cur_text = cur_text
        elif (self.money_layout.validate(cur_text, -1)[0] == 1):
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]
        else:
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]

        if (cur_text == "."): cur_text = "1"
        if (len(cur_text) > 0):
            if (cur_text[0] == "0"): cur_text = "1"
            if (float(cur_text) > 1_000_000):
                cur_text = "1000000"
            if (float(cur_text) < 1):
                cur_text = "1"

        self.money_layout.set_text(cur_text, 1)
        self.money_layout.set_cursor_pos(cur_cursor_pos, 1)


        self.result_layout.set_result1("")
        self.result_layout.set_result2("")
        
        self.is_result = False

    def money_text_change2(self, text):
        cur_text = text.replace(" ", "").replace(",", "")
        cur_cursor_pos = self.money_layout.get_cursor_pos(2)

        print(self.money_layout.validate(cur_text, -1))
        if (self.money_layout.validate(cur_text, -1)[0] == 2 or cur_text == ""):
            cur_text = cur_text
        elif (self.money_layout.validate(cur_text, -1)[0] == 1):
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]
        else:
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]

        if (cur_text == "."): cur_text = "1"
        if (len(cur_text) > 0):
            if (cur_text[0] == "0"): cur_text = "1"
            if (float(cur_text) > 1_000_000):
                cur_text = "1000000"
            if (float(cur_text) < 1):
                cur_text = "1"

        self.money_layout.set_text(cur_text, 2)
        self.money_layout.set_cursor_pos(cur_cursor_pos, 2)

        self.result_layout.set_result1("")
        self.result_layout.set_result2("")
        
        self.is_result = False


    def pers_text_change1(self, text):
        cur_text = text.replace(" ", "").replace(",", "")
        cur_cursor_pos = self.pers_layout.get_cursor_pos(1)

        print(self.pers_layout.validate(cur_text, -1))
        if (self.pers_layout.validate(cur_text, -1)[0] == 2 or cur_text == ""):
            cur_text = cur_text
        elif (self.pers_layout.validate(cur_text, -1)[0] == 1):
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]
        else:
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]

        if (cur_text == "."): cur_text = "1"
        if (len(cur_text) > 0):
            if (cur_text[0] == "0"): cur_text = "1"
            if (float(cur_text) > 30):
                cur_text = "30"
            if (float(cur_text) < 1):
                cur_text = "1"

        self.pers_layout.set_text(cur_text, 1)
        self.pers_layout.set_cursor_pos(cur_cursor_pos, 1)

        self.result_layout.set_result1("")
        self.result_layout.set_result2("")
        
        self.is_result = False

    def pers_text_change2(self, text):
        cur_text = text.replace(" ", "").replace(",", "")
        cur_cursor_pos = self.pers_layout.get_cursor_pos(2)

        print(self.pers_layout.validate(cur_text, -1))
        if (self.pers_layout.validate(cur_text, -1)[0] == 2 or cur_text == ""):
            cur_text = cur_text
        elif (self.pers_layout.validate(cur_text, -1)[0] == 1):
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]
        else:
            cur_text = cur_text[:cur_cursor_pos] + cur_text[cur_cursor_pos:]

        if (cur_text == "."): cur_text = "1"
        if (len(cur_text) > 0):
            if (cur_text[0] == "0"): cur_text = "1"
            if (float(cur_text) > 30):
                cur_text = "30"
            if (float(cur_text) < 1):
                cur_text = "1"

        self.pers_layout.set_text(cur_text, 2)
        self.pers_layout.set_cursor_pos(cur_cursor_pos, 2)

        self.result_layout.set_result1("")
        self.result_layout.set_result2("")
        
        self.is_result = False

    def date_change(self):
        self.result_layout.set_result1("")
        self.result_layout.set_result2("")
        
        self.is_result = False

    def report(self):
        if (self.is_result):
            data = {
                "Дата выдачи": self.date_layout.get_date1(),
                "Дата гашения": self.date_layout.get_date2(),
                "Сумма займа": self.money_layout.get_money1(),
                "Процентная ставка, %": self.pers_layout.get_pers1(),
                "Дата изменения процентной ставки": self.date_layout.get_date3(),
                "Новая процентная ставка, %": self.pers_layout.get_pers2(),

                "Дата частичного гашения": self.date_layout.get_date4(),
                "Сумма частичного гашения": self.money_layout.get_money2(),
                "Сумма процентов": self.result1,
                "Гашение займа": self.result2
            }

            excel = Excel(default_name="Займ_с_досрочным_гашением")
            filename = excel.save_file()
            if (filename != ""):
                excel.load_data(filename=filename, data=data)

                self.result_layout.set_result1("")
                self.result_layout.set_result2("")
                self.is_result = False

                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setText(f"Отчет сформирован\nДиректория документа: {filename}")
                msg_box.setWindowTitle("Information MessageBox")
                msg_box.setStandardButtons(QMessageBox.Ok)
                show = msg_box.exec_()

            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("Документ не сохранен")
                msg_box.setWindowTitle("Warning MessageBox")
                msg_box.setStandardButtons(QMessageBox.Ok)
                show = msg_box.exec_()

        else:

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("Для формирования отчета - заполните все поля")
            msg_box.setWindowTitle("Warning MessageBox")
            msg_box.setStandardButtons(QMessageBox.Ok)
            show = msg_box.exec_()