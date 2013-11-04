#!/usr/bin/python
#--*--coding:utf-8--*--

import sys,re
from PyQt4 import QtGui
from PyQt4 import QtCore
from dic import Fecth
import time,os
class IrregularForm(QtGui.QWidget): 
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)
            self.parent=parent

            mask=QtGui.QPixmap("./icons/search40.png")
            self.setMask(QtGui.QBitmap(mask.mask()))
            p=QtGui.QPalette()
            p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(mask))
            self.setPalette(p)
            self.setGeometry(200, 100, 40, 40)
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)

            self.setWindowIcon(QtGui.QIcon('./icons/search50.png'))
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
            if event.key() == QtCore.Qt.Key_X:
                self.emit(QtCore.SIGNAL('trueVisible()'))
            elif event.key() == QtCore.Qt.Key_Control:
                QtGui.qApp.quit()
class Dic(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.alt=None
        self.irregular=IrregularForm()
        self.irregular.show() 
 
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
        self.setWindowIcon(QtGui.QIcon('./icons/search50.png'))
        self.connect(okButton, QtCore.SIGNAL('clicked()'), \
            self.okButton)
        self.connect(cbbtn, QtCore.SIGNAL('clicked()'), \
            self.clipboardBotton)
        self.connect(self.irregular, QtCore.SIGNAL('trueVisible()'), \
            self,QtCore.SLOT('trueVisible()') )
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #self.fe=Fecth()
    @QtCore.pyqtSlot()
    def trueVisible(self):
        self.setVisible(True)
        self.irregular.setVisible(False)

    def clipboardBotton(self):
        clipboard = QtGui.QApplication.clipboard()
	#print clipboard.text()
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
        self.fe=Fecth()
        rows=self.fe.searchDB(src,None)
        trans=''
        if rows:
            for row in rows:
                trans = self.setColor(row[0],'red')
                if row[1]!='':
                   trans+=self.setColor(row[1]+','+row[2],'blue')
                trans+= self.setColor(row[3],'green')
            self.word.setText('<h3>'+trans+'</h3>')
        else:
            
            trans=self.setColor(src,'red')
            zh=self.fe.fecth('qt')
            trans+=self.setColor(zh[0],'blue')
            tmp=zh[1]
            if tmp=='':
                tmp='<b>Fetch fail!</b>'
            trans+= self.setColor(tmp,'green')
            self.word.setText('<h3>'+trans+'</h3>')
        self.fe.close()
    def keyReleaseEvent(self, event):
            
            if event.key() == QtCore.Qt.Key_Return:
                self.okButton()
            elif event.key() == QtCore.Qt.Key_Shift:
                self.clipboardBotton()
            elif event.key() == QtCore.Qt.Key_Alt:
                self.alt=QtCore.Qt.Key_Alt
                self.setVisible(False)
                self.irregular.setVisible(True)
            elif event.key() == QtCore.Qt.Key_Space:
                self.edit.setText('')
            elif event.key() == QtCore.Qt.Key_Control:
                QtGui.qApp.quit()
    def closeEvent(self, event):
        
        QtGui.qApp.quit()
        #self.irregular.destroy()
    def leaveEvent(self,evt): 
        if self.alt==QtCore.Qt.Key_Alt:
            self.alt=-1
            return
        cx,cy=QtGui.QCursor.pos().x(),QtGui.QCursor.pos().y()
        if(cx >= self.x() and cx <= self.x()+self.width()
            and cy >= self.y() and cy <=self.y()+self.height()):
            pass
        else:
            
            self.irregular.setVisible(True)
            self.setVisible(False)
            #self.setWindowOpacity(0.3)
def run():
    app = QtGui.QApplication(sys.argv)
    dic = Dic()
    dic.show()
    sys.exit(app.exec_())
if __name__=='__main__':
    if len(sys.argv)==1:
        run()
    elif len(sys.argv)==2:
        if sys.argv[1]=='--fork' or \
            sys.argv[1]=='-f':
            try:
                if os.fork() > 0:
                    os._exit(0)
            except OSError,error:
                print 'fork #1 failed: %d (%s)' % (error.errno, error.strerror)
                os._exit(1)
            run()
        elif sys.argv[1]=='-h':
            print 'Usage:','\n\t-h help,\n\t--fork,-f daemon run...'
