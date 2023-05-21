import sys
import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob
import os
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
from functools import partial
from pathlib import Path
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
matplotlib.use('QtAgg')
plt.style.use('_classic_test_patch')
matplotlib.rcParams['font.size'] = 7

PARAMS = crud.get_parameters_list()
DATASET_DIRECTORY = ''.join([str(Path(__file__).parent.parent.absolute()), '\\datasets_to_predict'])
PREDICTS_DIRECTORY = ''.join([str(Path(__file__).parent.parent.absolute()), '\\predicts'])


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        #self.fig = Figure(figsize=(width, height))
        #self.fig.tight_layout(pad=5.0)
        # plt.xticks(fontsize=7)
        # plt.yticks(fontsize=7)
        self.fig, self.axes = plt.subplots(nrows=4,
                                           ncols=1,
                                           gridspec_kw={'height_ratios': [5, 5, 2, 2]},
                                           figsize=(width, height),
                                           layout='constrained')
        # self.fig, self.ax = plt.subplots(figsize=(width, height))
        # self.fig.subplots_adjust(left=0.1,
        #                          bottom=0.1,
        #                          right=0.9,
        #                          top=0.9,
        #                          wspace=0.4,
        #                          hspace=0.4)
        #self.axes = self.fig.subplots(nrows=4, ncols=1, figsize=(10, 7))
        super(MplCanvas, self).__init__(self.fig)


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
            button.setObjectName(name)
            button.setCheckable(True)
            button.setFixedSize(210, 110)
            button.clicked.connect(partial(self.the_button_was_pressed, btn=button))
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

    def the_button_was_pressed(self, btn: QPushButton):
        param = btn.objectName()
        predict = pd.read_csv(self.get_current_dataset(PREDICTS_DIRECTORY))
        dataset = pd.read_csv(self.get_current_dataset(DATASET_DIRECTORY))
        test_dataset = pd.read_csv('C:\\Users\\miha-\\Desktop\\diplom_program\\programs\\test_datasets\\test_dataset1.csv')
        y_pred = predict[param].values
        y_test = test_dataset[param][-24:].values
        y_past = dataset[param].values

        sc = MplCanvas(self, width=20, height=10)
        toolbar = NavigationToolbar(sc)

        sc.axes[0].plot(list(range(-len(y_past), 0)), y_past,
                        label='Данные наблюдаемого периода',
                        color='steelblue', marker='.', linewidth=0.7)
    
        sc.axes[0].plot(np.arange(len(y_pred)),
                        y_pred,
                        color='orange', marker='.', linewidth=0.7,
                        label='Предсказанные значения прогнозируемого периода'.format(param))
        
        sc.axes[1].plot(np.arange(len(y_test)), y_test,
                        label='Данные наблюдаемого периода',
                        color='steelblue', marker='.', linewidth=0.7)
    
        sc.axes[1].plot(np.arange(len(y_pred)),
                        y_pred,
                        color='orange', marker='.', linewidth=0.7,
                        label='Предсказанные значения прогнозируемого периода'.format(param))
        
        sc.axes[2].plot(np.arange(len(y_test)), y_test,
                        label='Данные наблюдаемого периода',
                        color='steelblue', marker='.', linewidth=0.7)
    
        sc.axes[3].plot(np.arange(len(y_pred)),
                        y_pred,
                        color='orange', marker='.', linewidth=0.7,
                        label='Предсказанные значения прогнозируемого периода'.format(param))
        
        for ax in sc.axes:
            #ax.legend(loc='upper left')
            ax.grid(which='both', linewidth='0.2', color='grey')
            ax.minorticks_on()
            ax.tick_params(which='minor', bottom=False, left=False, grid_linewidth=0.2)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            # ax.set_ylabel('Значение', size=7)
            # ax.set_xlabel('Периоды, час', size=7)

        graphics_layout = QVBoxLayout()
        graphics_layout.addWidget(toolbar)
        graphics_layout.addWidget(sc)

        graphics_widget = QWidget()
        graphics_widget.setLayout(graphics_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        scroll.setWidget(graphics_widget)
        self.image_layout.addWidget(scroll)
        print('Clicked!')

    def get_current_dataset(self, directory):
        dataset_file = ''

        files = glob.glob(directory + '\\' + '*.csv')
        if files:
            files = sorted(files, key=os.path.getctime)
            dataset_file = files[-1]

        return dataset_file


app = QApplication(sys.argv)
app.setStyleSheet(Path('style.qss').read_text())

window = MainWindow()
#window.showMaximized()
window.show()

app.exec()
