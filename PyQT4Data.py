# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 22:02:35 2018

@author: austin
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QComboBox, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore
import numpy as np
from datetime import datetime
import matplotlib as mpl 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd #pandas大法好

mpl.use('Qt5Agg')
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体 
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题
progname = os.path.basename(sys.argv[0])
progversion = "0.1"

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class PlotCount(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
	
    def AutoLabel(self):
        global df2
        t = df2.index
        ax1=self.axes
        rects1= self.rects1
        for rect, label in zip(rects1, t):
            height = rect.get_height()
            ax1.text(rect.get_x() + rect.get_width() / 2, 0, height,
            ha='center', va='bottom')
            ax1.text(rect.get_x() + rect.get_width() / 2, height/2, label,
            ha='center', va='bottom', rotation='vertical')
			
    def compute_initial_figure(self):
        global df2
        t = df2.index
        data1 = df2['单价']
        ax1 = self.axes
        x=np.arange(len(t))
        self.rects1 = ax1.bar(x, data1)
        ax1.set_ylabel('成交数量')
        ax1.set_xticks(x)
        ax1.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
        #ax1.text(x, data1, t)
        self.AutoLabel()
        ax1.yaxis.grid(True, linestyle='--', which='major',
                   color='grey', alpha=.25)
        #self.axes.autoscale_view(True,'both',True)
		
    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        global df2
        ax1 = self.axes
        t = df2.index
        x=np.arange(len(t))
        data1 = df2['单价']
        self.rects1.remove()
        ax1.texts.clear()
        self.draw()        
        self.rects1 = ax1.bar(x, data1)
        ax1.set_xlim([-1, len(t)])
        #self.axes.relim()
        ax1.set_xticks(x)
        #ax.yaxis.set_major_formatter(matplotlib.ticker.NullFormatter())
        ax1.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
        self.AutoLabel()
        self.draw()
		
class PlotCanvas(MyMplCanvas):
 
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)   
    
        #self.plot()
   
    def align_yaxis(ax1, v1, ax2, v2):
        """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
        _, y1 = ax1.transData.transform((0, v1))
        _, y2 = ax2.transData.transform((0, v2))
        inv = ax2.transData.inverted()
        _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
        miny, maxy = ax2.get_ylim()
        ax2.set_ylim(miny+dy, maxy+dy)
        
    def compute_initial_figure(self):
        global df1
        t = df1.index
        data1 = df1['单价']
        data2 = df1['总价']        
        #fig, (ax1, ax2) = plt.subplots(2, sharex=True)
        ax1 = self.axes
        #fig, ax1 = plt.subplots()
        #ax1.plot(t, s1)
        color = 'tab:red'
        self.l1,=ax1.plot(t, data1, color=color, marker='o', linestyle=':',linewidth=0, markersize=7)
        #self.l1=ax1.scatter(t, data1, c=color)
        ax1.set_xlabel('成交日期')
        ax1.set_ylabel('单价', color=color)        
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.yaxis.grid(True, linestyle='--', which='major',
                   color='grey', alpha=.25)
        ax1.xaxis.grid(True, linestyle='--', which='major',
                   color='grey', alpha=.25)
				   
        self.axes2= self.axes.twinx()
        ax2 = self.axes2  # instantiate a second axes that shares the same x-axis
        #ax2.plot(t, s2)
        color = 'tab:blue'
        ax2.set_ylabel('总价', color=color)  # we already handled the x-label with ax1
        self.l2,=ax2.plot(t, data2, color=color, marker='s', linestyle=':',linewidth=0, markersize=7)
        #self.l2=ax2.scatter(t, data2, c=color)
        ax2.tick_params(axis='y', labelcolor=color)

        #self.axes.autoscale_view(True,'both',True)
        #self.draw()
        
    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        #l = [random.randint(0, 10) for i in range(4)]
        global df1
        t = df1.index
        data1 = df1['单价']
        data2 = df1['总价'] 
        
        self.l1.set_data(t,data1)
        self.l2.set_data(t,data2)
        #self.l1.set_ydata(data1)
        #self.l1.set_ydata(data2)
        #self.axes.autoscale_view(True,True,True)
        #self.l2.autoscale_view(True,True,True)
        self.axes.relim()
        self.axes.autoscale_view()
        self.axes2.relim()
        self.axes2.autoscale_view()
        self.draw()
        self.flush_events()
        
#        self.axes.cla()
#        self.axes.plot(t, data1)
#        self.axes.twinx().plot(t, data2)
#        self.draw()


class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
#        QMainWindow.__init__(self)
#        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#        self.left = 100
#        self.top = 100
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
#        self.width = 800
#        self.height = 600
        self.initUI()
 
    def initUI(self):
        global df,df1,df2
                #import data 
        # def parse_dates(x):
        #     return datetime.strptime(x, "%Y.%m.%d")    
        dateparse = lambda x: datetime.strptime(x, '%Y.%m.%d')    
        df=pd.read_csv('LianJia.csv',encoding='ANSI',index_col=0,parse_dates=['成交日期'],date_parser=dateparse) #注意编码格式和索引
        df.set_index('成交日期', inplace=True)  #利用 '时间' 为index
#        Select_XiaoQu = App.getcombo1Information #self.combo1.currentText()
#        print(Select_XiaoQu)
#        if Select_XiaoQu == None:
#            Select_XiaoQu='瀚盛家园'
        Select_XiaoQu = '瀚盛家园'
        df1=df[df['小区'] == Select_XiaoQu]
        
        df2=df[df['板块'] == '唐镇'].groupby(['小区']).count()
#        df2.groupby(['小区']).count().index
#        df2.groupby(['小区']).count()['单价']
        
        self.setWindowTitle(self.title)
#        self.setGeometry(self.left, self.top, self.width, self.height)
        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)


        
        self.main_widget = QWidget(self)
        l = QVBoxLayout(self.main_widget)
        self.m = PlotCanvas(self.main_widget, width=8, height=4, dpi=100)
        self.n = PlotCount(self.main_widget, width=8, height=4, dpi=100)
        #m.move(0,0)

        
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        
        self.combo = QComboBox(self)
        self.combo1 = QComboBox(self)
        l.addWidget(self.combo)
        l.addWidget(self.combo1)
        l.addWidget(self.m)
        l.addWidget(self.n)
        self.combo1.addItem('瀚盛家园')
        #self.combo.move(500, 30)
        for ListItem in df['板块'].unique():
            self.combo.addItem(ListItem)
        self.combo.currentTextChanged.connect(self.comboChanged)
        self.combo.activated.connect(self.BanKuaiChanged)
        self.combo1.activated.connect(self.XiaoQuChanged)
		
        #self.combo.activated.connect(self.comboChanged)
        #self.roomBox.activated.connect(self.m.plot)
        
        #self.combo1.move(600, 30)
        #self.combo1.activated.connect(m.plot())

        #button = QPushButton('PyQt5 button', self)
        #button.setToolTip('This s an example button')
        #button.move(500,0)
        #button.resize(140,100)

        #combo.activated[str].connect(self.onActivated)  
 
        #self.show()
    
    def comboChanged(self, text):
        #self.mediaBox.setEnabled(True)
        global df,df1
        Select_XiaoQu = self.combo.currentText()
        #print(Select_XiaoQu)
        self.combo1.clear()
        df1=df[df['板块'] == Select_XiaoQu]
        #print(df1['小区'].unique())
        for ListItem in df1['小区'].unique():
            self.combo1.addItem(ListItem)
    
    def XiaoQuChanged(self, text):
        global df,df1
        #self.mediaBox.setEnabled(True)
        Select_XiaoQu = self.combo1.currentText()
        df1=df[df['小区'] == Select_XiaoQu]
        self.m.update_figure()

    def BanKuaiChanged(self, text):
        global df,df2
        #self.mediaBox.setEnabled(True)
        Select_XiaoQu = self.combo.currentText()
        df2=df[df['板块'] == Select_XiaoQu].groupby(['小区']).count()
        self.n.update_figure()        
    
    def getcombo1Information(self):
        textMedia = self.combo1.currentText()
        #print(textMedia)
        return textMedia
    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QMessageBox.about(self, "About",
                                    """embedding_in_qt5.py example
Copyright 2005 Fand qt5"""
                                )


        
if __name__ == '__main__':
    #app = QApplication(sys.argv)
   app = QCoreApplication.instance()
   if app is None:
       app = QApplication(sys.argv)
       
   ex = App()
   ex.show()
   sys.exit(app.exec_())
#    def run_app():
#        app = QApplication(sys.argv)
#        mainWin = App()
#        mainWin.show()
#        app.exec_()
#    run_app()
    # if not QApplication.instance():
    #     app = QApplication(sys.argv)
    # else:
    #     app = QApplication.instance() 
    # ex =App()
    # ex.show()
    # app.quit()
        
