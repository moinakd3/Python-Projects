from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

import re

class Find(QtGui.QDialog):
    def __init__(self, parent = None):
        
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
	self.lastStart = 0
	self.initUI()
 
    def initUI(self):

        findButton = QtGui.QPushButton("Find",self)
        findButton.clicked.connect(self.find)
	replaceButton = QtGui.QPushButton("Replace",self)
        replaceButton.clicked.connect(self.replace)
	allButton = QtGui.QPushButton("Replace all",self)
        allButton.clicked.connect(self.replaceAll)

        self.normalRadio = QtGui.QRadioButton("Normal",self)

        #regexRadio = QtGui.QRadioButton("RegEx",self)

        self.findField = QtGui.QTextEdit(self)
        self.findField.resize(240,53)

        self.replaceField = QtGui.QTextEdit(self)
        self.replaceField.resize(240,53)
        
        layout = QtGui.QGridLayout()

        layout.addWidget(self.findField,1,0,1,4)
        layout.addWidget(self.normalRadio,2,2)
        #layout.addWidget(regexRadio,2,3)
        layout.addWidget(findButton,2,0,1,2)
        
        layout.addWidget(self.replaceField,3,0,1,4)
        layout.addWidget(replaceButton,4,0,1,2)
        layout.addWidget(allButton,4,2,1,2)

        self.setGeometry(303,303,360,250)
        self.setWindowTitle("Find and Replace")
        self.setLayout(layout)

        self.normalRadio.setChecked(True)

    def find(self):

        text = unicode(self.parent.text.toPlainText())
        query = unicode(self.findField.toPlainText())

        if self.normalRadio.isChecked():

            self.lastStart = text.find(query,self.lastStart + 1)
	    if self.lastStart >= 0:
		end = self.lastStart + len(query)
                self.moveCursor(self.lastStart,end)

            else:

                self.lastStart = 0
                self.parent.text.moveCursor(QtGui.QTextCursor.End)

        else:

            pattern = re.compile(query)

            match = pattern.search(text,self.lastStart + 1)

            if match:
		self.lastStart = match.start()
                self.moveCursor(self.lastStart,match.end())
            else:
		self.lastStart = 0
                self.parent.text.moveCursor(QtGui.QTextCursor.End)

    def replace(self):

        cursor = self.parent.text.textCursor()

        if cursor.hasSelection():

            cursor.insertText(self.replaceField.toPlainText())
            self.parent.text.setTextCursor(cursor)

    def replaceAll(self):

        self.lastStart = 0
        self.find()
	#till laststrt = 0
        while self.lastStart:
            self.replace()
            self.find()

    def moveCursor(self,start,end):

        cursor = self.parent.text.textCursor()

        cursor.setPosition(start)

        cursor.movePosition(QtGui.QTextCursor.Right,QtGui.QTextCursor.KeepAnchor, end - start)

        self.parent.text.setTextCursor(cursor)
