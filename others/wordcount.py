from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

class WordCount(QtGui.QDialog):
    
    def __init__(self,parent = None):
        QtGui.QDialog.__init__(self, parent)
	self.parent = parent
        self.initUI()
 
    def initUI(self):

        currentLabel = QtGui.QLabel("Current selection",self)
        currentLabel.setStyleSheet("font-weight:bold; font-size: 15px;")

        currentWordsLabel = QtGui.QLabel("Words: ", self)
        currentSymbolsLabel = QtGui.QLabel("Symbols: ",self)
        
        self.currentWords = QtGui.QLabel(self)
        self.currentSymbols = QtGui.QLabel(self)

        totalLabel = QtGui.QLabel("Total",self)
        totalLabel.setStyleSheet("font-weight:bold; font-size: 15px;")

        totalWordsLabel = QtGui.QLabel("Words: ", self)
        totalSymbolsLabel = QtGui.QLabel("Symbols: ",self)

        self.totalWords = QtGui.QLabel(self)
        self.totalSymbols = QtGui.QLabel(self)

        # Layout
        
        layout = QtGui.QGridLayout(self)
	layout.addWidget(currentLabel,0,0)
        layout.addWidget(currentWordsLabel,1,0)
        layout.addWidget(self.currentWords,1,1)
	layout.addWidget(currentSymbolsLabel,2,0)
        layout.addWidget(self.currentSymbols,2,1)

        spacer = QtGui.QWidget()
        spacer.setFixedSize(0,5)

        layout.addWidget(spacer,3,0)
	layout.addWidget(totalLabel,4,0)
	layout.addWidget(totalWordsLabel,5,0)
        layout.addWidget(self.totalWords,5,1)
	layout.addWidget(totalSymbolsLabel,6,0)
        layout.addWidget(self.totalSymbols,6,1)

        self.setWindowTitle("Word count")
        self.setGeometry(303,303,200,200)
        self.setLayout(layout)
        
    def getText(self):

        text = unicode(self.parent.text.textCursor().selectedText())

        words = str(len(text.split()))

        symbols = str(len(text))

        self.currentWords.setText(words)
        self.currentSymbols.setText(symbols)

        text = unicode(self.parent.text.toPlainText())

        words = str(len(text.split()))
        symbols = str(len(text))

        self.totalWords.setText(words)
        self.totalSymbols.setText(symbols)
