# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow , QDialog
from .Ui_mainwindow import Ui_MainWindow
from .Ui_about import Ui_Dialog


import numpy as np
import pyqtgraph as pg



class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    qeStr=""
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.btn_quit.clicked.connect(self.close)
        self.ln_a.setFocus()
        pg.setConfigOptions(antialias=True)
        self.QEplot = self.graphicsView.addPlot(title="y=ax²+bx+c")
        self.QEplot.showGrid(x=True, y=True)
        self.QEplot.setLabel('bottom', "X - Axis")
        self.QEplot.setLabel('left', "Y - Axis")
        self.QEplot.enableAutoRange()  
        
        self.LEplot = self.graphicsView_2.addPlot(title="X-Y Plot")
        self.LEplot.showGrid(x=True, y=True)
        self.LEplot.setLabel('bottom', "X - Axis")
        self.LEplot.setLabel('left', "Y - Axis")
        self.LEplot.enableAutoScale()
        
        self.ln_a.returnPressed.connect(self.on_btn_fr_clicked)
        self.ln_b.returnPressed.connect(self.on_btn_fr_clicked)
        self.ln_c.returnPressed.connect(self.on_btn_fr_clicked)
        self.ln_2v_a1.returnPressed.connect(self.on_btn_fs_clicked)
        self.ln_2v_a2.returnPressed.connect(self.on_btn_fs_clicked)
        self.ln_2v_b1.returnPressed.connect(self.on_btn_fs_clicked)
        self.ln_2v_b2.returnPressed.connect(self.on_btn_fs_clicked)
        self.ln_2v_c1.returnPressed.connect(self.on_btn_fs_clicked)
        self.ln_2v_c2.returnPressed.connect(self.on_btn_fs_clicked)
        
#   ******** These functions are helpful to format and to find roots of quadratic equations**********  

    def qeClear(self, i):
        
        self.ln_info.setText("")
        self.ln_qe.setText("")
        self.ln_root1.setText("")
        self.ln_root2.setText("")
        self.QEplot.clear()
        self.QEplot.setTitle("")
        if i==0 :
            self.ln_a.setText("")
            self.ln_b.setText("")
            self.ln_c.setText("")

    def qePrintHelper(self, a, b, c):
        str=""
        if a.is_integer():
            a=int(a)
        if b.is_integer():
            b=int(b)
        if c.is_integer():
            c=int(c)
        if a==1 :
            x=''
        elif a==-1:
            x='-'
        else:
            x=a
        if b==1 :
            y=''
        elif b==-1:
            y='-'
        else:
            y=b
        if b>0 and c>0 :
            str="{}x²+{}x+{}".format(x,y,c)
        if b<0 and c>0 :
            str="{}x²{}x+{}".format(x,y,c)
        if b>0 and c<0 :
            str="{}x²+{}x{}".format(x,y,c)
        if b<0 and c<0 :
            str="{}x²{}x{}".format(x,y,c)
        if b==0 and c>0 :
            str="{}x²+{}".format(x,c)
        if b==0 and c<0 :
            str="{}x²{}".format(x,c)
        if c==0 and b>0 :
            str="{}x²+{}x".format(x,y)
        if c==0 and b<0 :
            str="{}x²{}x".format(x,y)
        if b==0 and c==0 :
            str="{}x²".format(x)
        self.ln_qe.setText(str+"=0")
        self.qeStr="y="+str
    
    def rootPrint(self, rt1, rt2):
        try :
            if rt1.is_integer() :
                rt1=int(rt1)
            if rt2.is_integer() :
                rt2=int(rt2)
        except AttributeError:
            print("roots are imaginary")
        self.ln_root1.setText("{:.2f}".format(rt1))
        self.ln_root2.setText("{:.2f}".format(rt2))

    def roots(self, a, b, c):
        desc=(b*b)-(4*a*c)
        if desc==0:
            rt=(-b)/(2*a)
            self.rootPrint(rt, rt)
            self.ln_info.setText("* roots are equal and real ( b² - 4ac = 0 ). ")
            self.parabola(a, b, c, rt, rt)
        if desc>0:
            rt=((-b)+np.sqrt(desc))/(2*a)
            rt2=((-b)-np.sqrt(desc))/(2*a)
            self.rootPrint(rt, rt2)
            self.ln_info.setText("* roots are distinct and real ( b² - 4ac > 0 ). ")
            self.parabola(a, b, c, rt, rt2)
        if desc<0: 
            rt=((-b)+np.sqrt(complex(desc)))/(2*a)
            rt2=((-b)-np.sqrt(complex(desc)))/(2*a)
            self.rootPrint(rt, rt2)
            self.ln_info.setText("* roots are distinct and imaginary ( b² - 4ac < 0 ). ")
            self.parabola(a, b, c, np.real(rt), np.real(rt2))
            
    def parabola(self, a, b, c,  rt1, rt2):
        self.QEplot.setTitle(self.qeStr)
        x=np.arange(-10, 11)
        y=(a*x*x)+(b*x)+c
        self.QEplot.plot(x, y, pen=pg.mkPen('g', width=2), symbol='o')
        self.QEplot.autoRange()
    
    @pyqtSlot()
    def on_btn_fr_clicked(self): 
        self.qeClear(1)
        try:
            a=self.ln_a.text()
            b=self.ln_b.text()
            c=self.ln_c.text()
            a=float(a)
            b=float(b)
            c=float(c)
        except ValueError :
            self.ln_info.setText("* Please input valid coefficients")
            self.QEplot.setTitle("")
        if a==0:
            self.ln_info.setText("* a must not be zero!! please input valid coefficients")
            self.QEplot.setTitle("")
        if isinstance(a, float) and isinstance(b, float) and isinstance(c, float) and a!=0 :
            self.qePrintHelper(a, b, c)
            self.roots(a, b, c)
               
    @pyqtSlot()
    def on_btn_clr_clicked(self):
        self.qeClear(0)
        
#   ********* These functions are helpful to format and to find solution of linear equations ********
    
    def lePrintHelper(self, a, b, c, id):
        str=""
        if a.is_integer():
            a=int(a)
        if b.is_integer():
            b=int(b)
        if c.is_integer():
            c=int(c)
        if a==1 :
            x=''
        elif a==-1:
            x='-'
        else:
            x=a
        if b==1 :
            y=''
        elif b==-1:
            y='-'
        else:
            y=b
        if a!=0 and b>0 :
            str="{}x+{}y={}".format(x, y, c)
        if a!=0 and b<0 :
            str="{}x{}y={}".format(x, y, c)
        if a!=0 and b==0 :
            str="{}x={}".format(x, c)
        if b!=0 and a==0 :
            str="{}y={}".format(y, c)
        if id==0:
            self.ln_2v_eq1.setText(str)
        if id==1:
            self.ln_2v_eq2.setText(str)
            
    def line(self, a, b, c, clr, sol_x, wid):
        x=np.arange(sol_x-5, sol_x+6)
        y=((c-(a*x))/b)
        self.LEplot.plot(x, y, pen=pg.mkPen(clr, width=wid), symbol='o')
        self.LEplot.autoRange()
        
    
    def solution(self, a1, b1, c1, a2, b2, c2):
        if (a1/a2)!=(b1/b2):
            u=np.array([[ a1, b1], [a2, b2]])
            v=np.array([c1, c2])
            sol=np.linalg.solve(u, v)
            sol_x=sol[0]
            sol_y=sol[1]
            if sol_x.is_integer():
                sol_x=int(sol_x)
            if sol_y.is_integer():
                sol_y=int(sol_y)
            self.ln_info2.setText("* Lines are Intersecting and consistent ( a1/a2 ≠  b1/b2)")
            self.ln_sol.setText("( x,y )=({:.2f} , {:.2f})".format(sol_x, sol_y))
            self.line(a1, b1, c1, 'g', sol_x, 2)
            self.line(a2, b2, c2, 'r', sol_x, 2)
        elif (a1/a2)==(b1/b2)!=(c1/c2):
            self.ln_info2.setText("* Lines are Parallel and inconsistent ( a1/a2 = b1/b2 ≠ c1/c2 )")
            self.ln_sol.setText("No solution")
            self.line(a1, b1, c1, 'g', 0, 2)
            self.line(a2, b2, c2, 'r', 0, 2)
        elif (a1/a2)==(b1/b2)==(c1/c2):
            self.ln_info2.setText("* Lines are Dependent and consistent ( a1/a2 = b1/b2 = c1/c2 )")
            self.ln_sol.setText("infinite solutions")
            self.line(a1, b1, c1, 'g', 0, 4)
            self.line(a2, b2, c2, 'r', 0, 2)
    
    def leClear(self, i):
        
        self.ln_info2.setText("")
        self.ln_sol.setText("")
        self.ln_2v_eq1.setText("")
        self.ln_2v_eq2.setText("")
        self.LEplot.clear()
        
        if i==0 :
            self.ln_2v_a1.setText("")
            self.ln_2v_a2.setText("")
            self.ln_2v_b1.setText("")
            self.ln_2v_b2.setText("")
            self.ln_2v_c1.setText("")
            self.ln_2v_c2.setText("")
        
    @pyqtSlot()
    def on_btn_fs_clicked(self):
        self.leClear(1)
        try:
            a1=self.ln_2v_a1.text()
            a2=self.ln_2v_a2.text()
            b1=self.ln_2v_b1.text()
            b2=self.ln_2v_b2.text()
            c1=self.ln_2v_c1.text()
            c2=self.ln_2v_c2.text()
            a1=float(a1)
            a2=float(a2)
            b1=float(b1)
            b2=float(b2)
            c1=float(c1)
            c2=float(c2)
        except ValueError:
            self.ln_info2.setText("*Please input valid co-efficients")
        if a1==0 and b1==0:
            self.ln_info2.setText("*Please enter valid co-efficients (a²+b²≠0)")
        elif a2==0 and b2==0:
            self.ln_info2.setText("*Please enter valid co-efficients (a²+b²≠0)")
        if isinstance(a1, float) and isinstance(a2, float) and isinstance(b1, float) and isinstance(b2, float) and isinstance(c1, float) and isinstance(c2, float) and (a1!=0 or b1!=0) and (a2!=0 or b2!=0) :
            self.lePrintHelper(a1, b1, c1, 0)
            self.lePrintHelper(a2, b2, c2, 1)
            self.solution(a1, b1, c1, a2, b2, c2)
            
    @pyqtSlot()
    def on_btn_clr2_clicked(self):
        self.leClear(0)
        
    @pyqtSlot()
    def on_btn_help_clicked(self):
        raise NotImplementedError
    
    @pyqtSlot()
    def on_btn_about_clicked(self):
        Dialog = QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.exec_()
