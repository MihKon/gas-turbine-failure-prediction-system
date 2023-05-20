import sys
import matplotlib
import matplotlib.image as mpimg
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QSizePolicy,
    QLayout,
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
from pathlib import Path
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
matplotlib.use('QtAgg')

PARAMS = crud.get_parameters_list()
DATASET_DIRECTORY = ''.join([str(Path(__file__).parent.parent.absolute()), '\\datasets_to_predict'])
PREDICTS_DIRECTORY = ''.join([str(Path(__file__).parent.parent.absolute()), '\\predicts'])


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class FrameButton(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)

        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.Shape.Panel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(8)

    def resizeEvent(self, event):
        self.frame.resize(self.size())
        QWidget.resizeEvent(self, event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 720)
        self.setWindowTitle("My App")

        self.param_widget = QWidget()

        self.page_layout = QHBoxLayout()
        self.param_layout = QVBoxLayout()
        self.param_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.image_layout = QStackedLayout()

        buttons = QButtonGroup(self.param_widget)

        for i in range(len(PARAMS)):
            name = PARAMS[i].split('_')[0]

            button = QPushButton(name)
            button.setCheckable(True)
            button.setFixedSize(210, 110)
            button.clicked.connect(self.the_button_was_clicked)
            button.move(10, i*120)

            font = QFont()
            font.setPointSize(12)

            buttons.addButton(button)
            self.param_layout.addWidget(button)
            
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)

        self.param_widget.setLayout(self.param_layout)
        scroll.setWidget(self.param_widget)
        scroll.setFixedWidth(250)

        self.page_layout.addWidget(scroll)
        self.page_layout.addLayout(self.image_layout)

        widget = QWidget(self)
        widget.setLayout(self.page_layout)
        self.setCentralWidget(widget)

    def the_button_was_clicked(self):
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        image = mpimg.imread('C:\\Users\\miha-\\Desktop\\diplom_program\\programs\\predicts_images\\Compressor T5 average_predict.png')
        sc.axes.imshow(image)
        graphics_layout = QVBoxLayout()
        self.image_layout.addWidget(sc)
        print('Clicked!')


app = QApplication(sys.argv)
app.setStyleSheet(Path('style.qss').read_text())

window = MainWindow()
#window.showMaximized()
window.show()

app.exec()
