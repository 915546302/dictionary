#!/usr/bin/python
#coding:utf-8

import sys,re
from PyQt4 import QtGui
from PyQt4 import QtCore
from dic import Fecth
import time
class IrregularForm(QtGui.QWidget):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)
            self.parent=parent

            mask=QtGui.QPixmap("./icons/search50.png")
            self.setMask(QtGui.QBitmap(mask.mask()))
            p=QtGui.QPalette()
            p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(mask))
            self.setPalette(p)
            self.setGeometry(100, 100, 100, 100)
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.mouseMovePos = QtCore.QPoint(0, 0)
        def mouseMoveEvent(self,event):
             if(self.mouseMovePos != QtCore.QPoint(0, 0)):
                self.move(self.geometry().x() + event.globalPos().x() \
                    - self.mouseMovePos.x(),self.geometry().y() \
                    + event.globalPos().y() - self.mouseMovePos.y())
                self.mouseMovePos = event.globalPos()
        def mousePressEvent(self,event):
            self.mouseMovePos = event.globalPos()

        def mouseReleaseEvent(self,event):
            self.mouseMovePos = QtCore.QPoint(0, 0)
        def mouseDoubleClickEvent(self, event):
            self.emit(QtCore.SIGNAL('trueVisible()'))
        def keyPressEvent(self, event):
            self.emit(QtCore.SIGNAL('trueVisible()'))
class Dic(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.frame=1
        self.irregular=IrregularForm()
        self.irregular.show() 
        #self.irregular.setVisible(False)
        self.curTime=time.strftime("%Y-%m-%d %H:%M", \
            time.localtime(time.time()))
        okButton = QtGui.QPushButton("OK")
        cbbtn = QtGui.QPushButton("clip")

        self.edit = QtGui.QLineEdit()
        self.word = QtGui.QLabel( self.curTime)
        rem = QtGui.QLabel('<h2><i>Word:</i></h2>')
        self.edit.setStyleSheet("color: blue;" 
                         "selection-color: yellow;" 
                         "selection-background-color: blue;")
        #cbbtn.setStyleSheet("color:red");
        cbbtn.setStyleSheet("color: blue;border:2px groove gray;"
                          "border-radius:10px;padding:2px 4px;")
        okButton.setStyleSheet("border:2px groove gray;"
                          "border-radius:10px;padding:2px 4px;")

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(rem)
        hbox.addWidget(self.edit)
        hbox.addWidget(okButton)
        hbox.addWidget(cbbtn)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.word)
        
        self.setLayout(vbox)
        self.setWindowOpacity(0.95)
        self.setWindowTitle('Dictionary')
        self.setGeometry(300, 300, 350, 150)
       # self.setWindowIcon(QtGui.QIcon('icons/dic.png'))
        self.connect(okButton, QtCore.SIGNAL('clicked()'), \
            self.okButton)
        self.connect(cbbtn, QtCore.SIGNAL('clicked()'), \
            self.clipboardBotton)
        self.connect(self.irregular, QtCore.SIGNAL('trueVisible()'), \
            self,QtCore.SLOT('trueVisible()') )
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.fe=Fecth()
    @QtCore.pyqtSlot()
    def trueVisible(self):
        self.setVisible(True)
        self.irregular.setVisible(False)

    def clipboardBotton(self):
        clipboard = QtGui.QApplication.clipboard()
        self.edit.setText(clipboard.text())
        self.buttonClicked(clipboard.text())
    def okButton(self):
        src=self.edit.text()
        self.buttonClicked(src)
    def setColor(self,string,key):
        if key=='red':
            return '<font color=\"red\">'+string+'</font>'+'<br>'
        elif key=='blue':
            return '<font color=\"blue\">'+string+'</font>'+'<br>'
        else:
            return '<font color=\"green\">'+string+'</font>'+'<br>'
    def buttonClicked(self,src):

        g=re.match('[a-zA-Z]+',src)
        if not g:
            self.word.setText(self.setColor('<h3>Not a word!</h3>','red'))
            return
        src=g.group()
        rows=self.fe.searchDB(src,None)
        trans=None  
        if rows:
            for row in rows:
                trans = self.setColor(row[0],'red')
                if row[1]!='':
                   trans+=self.setColor(row[1]+','+row[2],'blue')
                trans+= self.setColor(row[3],'green')
        else:
            trans=self.setColor(src,'red')
            zh=self.fe.fecth('qt')
            trans+=self.setColor(zh[0],'blue')
            tmp=zh[1]
            if tmp=='':
                tmp='<b>Fetch fail!</b>'
            trans+= self.setColor(tmp,'green')
        self.word.setText('<h3>'+trans+'</h3>')

    def keyPressEvent(self, event):
            if event.key() == QtCore.Qt.Key_Return:
                self.okButton()
            elif event.key() == QtCore.Qt.Key_Control|QtCore.Qt.Key_Shift:
                self.clipboardBotton()
            elif event.key() == QtCore.Qt.Key_Control|QtCore.Qt.Key_Alt:
                self.setVisible(False)
                self.irregular.setVisible(True)
    def closeEvent(self, event):
        self.fe.close()
        self.irregular.destroy()
    def enterEvent(self, evt):
        self.activateWindow()
        if(self.x() == self.frame-self.width()):
            self.move(-self.frame,self.y())
        elif(self.y() == self.frame-self.height()+self.y()-self.geometry().y()):
            self.move(self.x(),-self.frame)
    def leaveEvent(self,evt): 
         
        cx,cy=QtGui.QCursor.pos().x(),QtGui.QCursor.pos().y()
        if(cx >= self.x() and cx <= self.x()+self.width()
            and cy >= self.y() and cy <=self.y()+self.height()):
            #self.setWindowOpacity(0.95)
            self.setVisible(True)            
            self.irregular.setVisible(False)
        else:
            
            self.irregular.setVisible(True)
            self.setVisible(False)
            #self.setWindowOpacity(0.3)

app = QtGui.QApplication(sys.argv)
dic = Dic()
dic.show()
sys.exit(app.exec_())
