from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QRect, Qt
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QVXYModelMapper
class CustomTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.input_data = []
        self.mapping = {}
        self.column_count = 4
        self.row_count = 15
class gui:
    def __init__(self):
        app = QApplication([])
        lis = [
            "An element", "Another element", "Yay! Another one."
        ]
        model = QStringListModel(lis)
        view = QListView()
        view.setModel(model)
        view.show()
        app.exec()

