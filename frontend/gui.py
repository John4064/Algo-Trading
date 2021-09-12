#from PyQt5.QtWidgets import *
from random import randrange
from PySide6.QtCore import QPointF,Qt
from PySide6.QtGui import QColor, QPainter,QIcon
#from PySide6.QtWidgets import QMainWindow, QGridLayout,QWidget, QApplication,QPushButton,QLabel
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtWidgets import *
class MainWin(QWidget):
    def cssInt(self):
        #Declares all style sheets here
        self.css = "QPushButton { background-color: #003f4c }"
        #Mainbody color: #003f4c
        return
    def chart(self):
        # Creating a series and importing the data
        self.series = QLineSeries()
        self.series.append(0, 6)
        self.series.append(2, 4)
        self.series.append(3, 8)
        self.series.append(7, 4)
        self.series.append(10, 5)
        self.series.append(QPointF(11, 1))
        self.series.append(QPointF(13, 3))
        self.series.append(QPointF(17, 6))
        self.series.append(QPointF(18, 3))
        self.series.append(QPointF(20, 2))
        # self.series.setColor(QColor(255,255,0,127))
        # Creat echart and add the series in the chart
        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTitle("Simple line chart example")

        self.chart.setTheme(QChart.ChartThemeBlueCerulean)
        # The rendering of the chart
        self.chartview = QChartView(self.chart,self)
        self.chartview.setRenderHint(QPainter.Antialiasing)
        return
    def placement(self):
        """
        This Method handles the placement of all the elements of the gui
        :return:
        """
        #Graph
        self.chartview.setGeometry(300, 100, 650, 450)
        #Buttons
        self.closeB.setGeometry(1150, 0, 50, 25)
        self.minB.setGeometry(1100, 0, 50, 25)
        return
    def buttons(self):
        """
        This Method just declares and handles the connection between buttons
        :return: void
        """
        #CREATE A LAYOUT
        self.closeB = QPushButton('X', self)
        self.closeB.clicked.connect(lambda: self.close())
        self.closeB.setMaximumWidth(50)
        self.minB = QPushButton('-', self)
        self.minB.clicked.connect(lambda: self.showMinimized())
        self.minB.setMaximumWidth(50)
        self.setB = QPushButton('===', self)
        self.setB.clicked.connect(lambda: print('Settings'))
        self.setB.setMaximumWidth(50)
        #Style Sheets
        #self.closeB.setStyleSheet("font-family: Arial;color: white; background-color: blue")
        #self.minB.setStyleSheet("font-family: Arial;color: white; background-color: blue")
        self.closeB.setStyleSheet(self.css)
        self.minB.setStyleSheet(self.css)
        self.minB.setFlat(False)
        return
    def __init__(self):
        super().__init__()
        #Setting the windows Requirements
        self.setGeometry(400, 100, 1200, 800)
        self.setStyleSheet("QWidget {background-image: url(./background.png) }")
#"QWidget {background-image: url(./image.png) }"
        self.setFixedSize(1200,800)
        self.setWindowTitle("Stonk")
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.cssInt()
        self.buttons()
        self.chart()
        self.placement()
        return

def deadcode():
    #just a list of dead code for reference atm
    # TEST STUFF
    self.box = QGroupBox(self)
    self.box.setGeometry(0, 0, 1200, 50)
    self.box.setStyleSheet(self.test)
    lay = QGridLayout(self.box)
    """
    lay.setSpacing(10)
    lay.addWidget(self.setB,0,0)
    lay.addWidget(self.minB,0,8)
    lay.addWidget(self.closeB,0,9)
"""
    # self.box.setFlat(True)
    # self.box.setAlignment(5)