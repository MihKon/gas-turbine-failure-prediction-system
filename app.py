import sys
import matplotlib
import matplotlib.image as mpimg
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedLayout,
    QToolBar,
    QWidget,
    QMenuBar,
    QMenu,
    QFrame,
    QSplitter,
    QButtonGroup,
    QGroupBox,
    QScrollArea,
    QStatusBar
)
from database import crud
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
matplotlib.use('QtAgg')

PARAMS = crud.get_parameters_list()


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class FrameButton(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)

        if self.parent is None:
            self.frame = QFrame(self)
        else:
            self.frame = QFrame(self.parent)
        self.frame.setFrameShape(QFrame.Shape.Panel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(4)

    def resizeEvent(self, event):
        self.frame.resize(self.size())
        QWidget.resizeEvent(self, event)

    def show_image(self):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 720)
        self.setWindowTitle("My App")

        self.param_widget = QWidget()

        self.page_layout = QHBoxLayout()
        self.param_layout = QVBoxLayout()
        #self.param_layout.setGeometry(QtCore.QRect(0, 0, 300, 1020))
        
        self.graphics_layout = QVBoxLayout()
        self.image_layout = QStackedLayout()

        # self.frame_params = QFrame(self.param_widget)
        # self.frame_params.setFrameShape(QFrame.Shape.Panel)
        # self.frame_params.setFrameShadow(QFrame.Shadow.Raised)
        # self.frame_params.setLineWidth(2)

        group = QButtonGroup(self.param_widget)

        for i in range(len(PARAMS)):
            name = PARAMS[i].split('_')[0]
            # frame_2 = QFrame(self.frame_params)
            # frame_2.setFrameShape(QFrame.Shape.Panel)
            # frame_2.setFrameShadow(QFrame.Shadow.Raised)
            # frame_2.setLineWidth(4)
            # frame_2.setGeometry(QtCore.QRect(10, i*150, 210, 110))

            button = QPushButton(name, self.param_widget)
            button.setCheckable(True)
            button.setGeometry(QtCore.QRect(0, 0, 210, 110))
            button.clicked.connect(self.the_button_was_clicked)
            button.move(10, i*120)
            group.addButton(button)
            
        #self.param_layout.addWidget()
            # param_layout.addStretch(1)

        # btn = FrameButton('test 1')

        # sc = MplCanvas(self, width=5, height=4, dpi=100)
        # image = mpimg.imread('C:\\Users\\miha-\\Desktop\\diplom_program\\programs\\predicts_images\\Compressor T5 average_predict.png')
        # sc.axes.imshow(image)
        # graphics_layout.addWidget(sc)
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.param_widget)

        self.param_layout.addWidget(scroll)

        self.page_layout.addLayout(self.param_layout)
        self.page_layout.addLayout(self.graphics_layout)

        widget = QWidget(self)
        widget.setLayout(self.page_layout)
        self.setCentralWidget(widget)

    def the_button_was_clicked(self):
        print('Clicked!')


app = QApplication(sys.argv)

window = MainWindow()
#window.showMaximized()
window.show()

app.exec()
