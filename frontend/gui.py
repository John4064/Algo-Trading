#from PyQt5.QtWidgets import *
from random import randrange
from PySide6.QtCore import QPointF,Qt
from PySide6.QtGui import QColor, QPainter,QIcon
from PySide6.QtCore import QPointF,Qt,QRect
from PySide6.QtGui import QColor, QPainter,QIcon,QPixmap,QPalette,QBrush

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
        return
    def __init__(self):
        super().__init__()
        #Setting the windows Requirements
        self.equityN=0;
        self.setGeometry(400, 100, 1200, 800)
        self.setFixedSize(1200,800)
        self.setWindowTitle("Stonk")
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.cssInt()
        self.buttons()
        self.chartWid()
        self.statusWid()
        self.placement()
        return
    def cssInt(self):
        #Declares all style sheets here
        #Background #907495
        #Button  #2b7a95
        self.css = "QPushButton {background-color: #2b7a95; border: 0px; font-size: 24px; }"
        self.setStyleSheet("background-color:#2b7a95; color: red")
        #Stylesheet doesnt work for background jpg only applies to all widgets not background no clue why but this works
        self.photo = QLabel(self)
        self.photo.setGeometry(QRect(0, 0, 1200, 800))
        self.photo.setText("")
        self.photo.setPixmap(QPixmap("background.jpg"))
        self.photo.setScaledContents(False)
        self.photo.setObjectName("photo")

        #Mainbody color: #003f4c
        return
    def chartWid(self):
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

        self.chartview.setStyleSheet('border:0px; background-color: #907495; color: #907495')
        #self.chartview.setStyleSheet(background-color: #907495; border: 0px;)
        #Buttons
        self.closeB.setGeometry(1150, 0, 50, 25)
        self.minB.setGeometry(1100, 0, 50, 25)
        self.setB.setGeometry(0, 0, 50, 25)
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
    def statusWid(self):
        self.status = QLabel(self)
        self.statusText = "                        RCS STOCKS\n" \
                          "Current Buying Power: ${}\nCurrent Day Performance: {}%\n" \
                          "Current Equity: ${}\nCurrent Time: {}\nddddddddd \n" \
                          "dd"
        self.status.setText(self.statusText)
        #75 and 656 is the top right of bottom left box
        #Size is 234 width and 144 height
        self.status.setGeometry(75,656,234,144)
        self.status.setStyleSheet("background-color:#2c0e99; border: 3px solid #2b7a95;")
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
    self.setB = QPushButton(' ===', self)
    self.setB.clicked.connect(lambda: print('Settings'))
    self.setB.setMaximumWidth(100)
    #Style Sheets
    #self.closeB.setStyleSheet("font-family: Arial;color: white; background-color: blue")
    #self.minB.setStyleSheet("font-family: Arial;color: white; background-color: blue")
    self.topbar = [self.setB, self.minB, self.closeB]
    for x in self.topbar:
          x.setStyleSheet(self.css)
    return

