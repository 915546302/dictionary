#!/usr/bin/python
#coding:utf-8

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from dic import Fecth
import time

class Dic(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.frame=1
        
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
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint);
        self.fe=Fecth()
    def clipboardBotton(self):
        clipboard = QtGui.QApplication.clipboard()
        self.edit.setText(clipboard.text())
        self.buttonClicked(clipboard.text())
    def okButton(self):
        src=self.edit.text()
        self.buttonClicked(src)
    def setColor(self,string,key):
        if key==1:
            return '<font color=\"red\">'+string+'</font>'+'<br>'
        elif key==2:
            return '<font color=\"blue\">'+string+'</font>'+'<br>'
        else:
            return '<font color=\"green\">'+string+'</font>'+'<br>'
    def buttonClicked(self,src):
        if src=='':
            return
        rows=self.fe.searchDB(src,None)
        trans=None  
        if rows:
            if rows==1:
                 self.word.setText('<h3>Not Found!</h3>')
                 return
            for row in rows:
                trans = self.setColor(row[0],1)
                if row[1]!='':
                   trans+=self.setColor(row[1]+','+row[2],2)
                trans+= self.setColor(row[3],3)
        else:
            trans=self.setColor(src,1)
            zh=self.fe.fecth('qt')
            trans+=self.setColor(zh[0],2)
            tmp=zh[1]
            if tmp=='':
                tmp='<b>Fetch fail!</b>'
            trans+= self.setColor(tmp,3)
        self.word.setText('<h3>'+trans+'</h3>')

    def keyPressEvent(self, event):
            if event.key() == QtCore.Qt.Key_Return:
                self.okButton()
            elif event.key() == QtCore.Qt.Key_Control|QtCore.Qt.Key_Shift:
                self.clipboardBotton()
        
    def closeEvent(self, event):
        self.fe.close()
    def enterEvent(self, evt):
        self.activateWindow()
        if(self.x() == self.frame-self.width()):
            self.move(-self.frame,self.y())
        elif(self.y() == self.frame-self.height()+self.y()-self.geometry().y()):
            self.move(self.x(),-self.frame)
    def leaveEvent(self,evt):    
      cx,cy=QtGui.QCursor.pos().x(),QtGui.QCursor.pos().y()
      
      if(cx >= self.x() and cx <= self.x()+self.width()
          and cy >= self.y() and cy <= self.geometry().y()):
          self.setWindowOpacity(0.95)
          self.resize(350,150)
          return#title bar
      else:
          self.setWindowOpacity(0.3)
          
      # elif(self.x() < 0 and QtGui.QCursor.pos().x()>0):
      #     self.move(self.frame-self.width(),self.y())
      # elif(self.y() < 0 and QtGui.QCursor.pos().y()>0):
      #     self.move(self.x(), self.frame-self.height()+self.y()-self.geometry().y())
app = QtGui.QApplication(sys.argv)
dic = Dic()
dic.show()
sys.exit(app.exec_())
