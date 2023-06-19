from PyQt5.QtWidgets import QFileDialog

from openpyxl import Workbook


class Excel(Workbook):

    def __init__(self, default_name):
        super(Excel, self).__init__()

        self.default_name = default_name
        self.ws = None

    def save_file(self):
        file_filter = 'Data File (*.xlsx);; Excel File (*.xlsx *.xls)'
        try:
            file_dialog = QFileDialog.getSaveFileName(
                caption='Save file',
                directory=self.default_name + ".xlsx",
                filter=file_filter,
                initialFilter='Excel File (*.xlsx *.xls)'
            )
            return file_dialog[0]
        except Exception:
            return ""

    def load_data(self, filename, data: dict):
        self.ws = self.active
        data_dict = data
        for key, value in data_dict.items():
            self.ws.append([key, value])

        self.save(filename=filename)

