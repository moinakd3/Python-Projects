# moinakd3 project!
# syntax highlight added
# auto word/code completion/hinting added
# linker added

import sys, re, os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from others import *

#DEF = ('#include <iostream>\nusing namespace std;\n\nint main() {\n// your code goes here\nreturn 0;}')

class MH(QSyntaxHighlighter):

    def __init__( self, parent, theme ):
      QSyntaxHighlighter.__init__( self, parent )

      self.parent = parent

      keyword = QTextCharFormat()
      reservedClasses = QTextCharFormat()
      delimiter = QTextCharFormat()
      specialConstant = QTextCharFormat()
      boolean = QTextCharFormat()
      define = QTextCharFormat()
      number = QTextCharFormat()
      comment = QTextCharFormat()
      comment2 = QTextCharFormat()
      string = QTextCharFormat()
      singleQuotedString = QTextCharFormat()
      hashdef = QTextCharFormat()

      self.highlightingRules = []


      #keywords
      brush = QBrush(Qt.darkYellow, Qt.SolidPattern)
      reservedClasses.setForeground( brush )
      reservedClasses.setFontWeight( QFont.Bold )
      keywords = QStringList( ["auto", "double", "int", "break","else", "long", "switch", "case", "enum",
                               "register","typedef", "char", "extern", "return", "union", "const", "float", "short",
                               "unsigned", "continue", "for", "signed", "void", "default", "goto", "sizeof", "volatile",
                               "if", "while", "bool", "using", "namespace"] )
      for word in keywords:
        pattern = QRegExp("\\b" + word + "\\b")
        rule = HighlightingRule( pattern, reservedClasses )
        self.highlightingRules.append( rule )

      #delimiters
      pattern = QRegExp("[\)\(]+|[\{\}]+")
      delimiter.setForeground( brush )
      delimiter.setFontWeight( QFont.Bold )
      rule = HighlightingRule( pattern, delimiter )
      self.highlightingRules.append( rule )

      #specialConstant
      brush = QBrush( Qt.green, Qt.SolidPattern )
      specialConstant.setForeground( brush )
      keywords = QStringList( [ "NULL" ] )
      for word in keywords:
        pattern = QRegExp("\\b" + word + "\\b")
        rule = HighlightingRule( pattern, specialConstant )
        self.highlightingRules.append( rule )

      #bool
      boolean.setForeground( brush )
      keywords = QStringList( [ "true", "false" ] )
      for word in keywords:
        pattern = QRegExp("\\b" + word + "\\b")
        rule = HighlightingRule( pattern, boolean )
        self.highlightingRules.append( rule )

      #define
      brush = QBrush(Qt.magenta, Qt.SolidPattern)
      define.setForeground(brush)
      keywords = QStringList(["define", "include"])
      for word in keywords:
          pattern = QRegExp("\\b" + word + "\\b")
          rule = HighlightingRule(pattern, define)
          self.highlightingRules.append(rule)

      #number_all_types
      brush = QBrush(Qt.cyan, Qt.SolidPattern)
      pattern = QRegExp( "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?" )
      pattern.setMinimal( True )
      number.setForeground( brush )
      rule = HighlightingRule( pattern, number )
      self.highlightingRules.append( rule )

      '''  
      #hashdef
      brush = QBrush(Qt.darkCyan, Qt.SolidPattern)
      pattern = QRegExp("#[^\n]*")
      hashdef.setForeground(brush)
      rule = HighlightingRule(pattern, hashdef)
      self.highlightingRules.append(rule)
      '''

      #singlelinecomment
      brush = QBrush( Qt.blue, Qt.SolidPattern )
      pattern = QRegExp( "//[^\n]*" )
      comment.setForeground( brush )

      rule = HighlightingRule( pattern, comment )
      self.highlightingRules.append( rule )


      #multilinecomment
      brush = QBrush(Qt.blue, Qt.SolidPattern)
      comment2.setForeground(brush)

      pattern = QRegExp("/\\*");
      rule = HighlightingRule(pattern, comment2)
      self.highlightingRules.append(rule)

      pattern2 = QRegExp("\\*/");
      rule = HighlightingRule(pattern2, comment2)
      self.highlightingRules.append(rule)

      #string
      brush = QBrush( Qt.red, Qt.SolidPattern )
      pattern = QRegExp( "\".*\"" )
      pattern.setMinimal( True )
      string.setForeground( brush )
      rule = HighlightingRule( pattern, string )
      self.highlightingRules.append( rule )

      #singleQuote_char
      pattern = QRegExp( "\'.*\' + \\'\n'.*'\'" )

      pattern.setMinimal( True )
      singleQuotedString.setForeground( brush )
      rule = HighlightingRule( pattern, singleQuotedString )
      self.highlightingRules.append( rule )

    #importatnt part here
    def highlightBlock( self, text ):
      for rule in self.highlightingRules:
        expression = QRegExp( rule.pattern )
        index = expression.indexIn( text )
        while index >= 0:
          length = expression.matchedLength()
          self.setFormat( index, length, rule.format )
          index = text.indexOf( expression, index + length )
      self.setCurrentBlockState( 0 )
      self.startIndex = 0
      if self.previousBlockState() != 1:
          startIndex = pattern.indexIn(text)
      while startIndex >= 0:
          endIndex = pattern2.indexIn(text, startIndex)
          if endIndex == -1:
              self.setCurrentBlockState(1)
              commentLength = len(text) - startIndex
          else:
              commentLength = endIndex - startIndex + pattern2.matchedLength()
          self.setFormat(startIndex,commentLength,comment2)
          startIndex = pattern.indexIn(text, startIndex + commentLength)

class HighlightingRule():
  def __init__( self, pattern, format ):
    self.pattern = pattern
    self.format = format

class HighlightingRule2():
  def __init__( self, pattern, pattern2, format ):
    self.pattern = pattern
    self.pattern2 = pattern2
    self.format = format


class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):

        QtGui.QMainWindow.__init__(self, parent)
        self.filename = ""
        self.initUI()

    def initToolbar(self):

        self.newAction = QtGui.QAction(QtGui.QIcon("icons/new.png"), "New File", self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.setStatusTip("Create a new file")
        self.newAction.triggered.connect(self.new)

        self.buildAction = QtGui.QAction(QtGui.QIcon("icons/build.png"), "Build the File", self)
        self.buildAction.setShortcut("Ctrl+M")
        self.buildAction.setStatusTip("Build the File and Execute")
        self.buildAction.triggered.connect(self.build)

        self.openAction = QtGui.QAction(QtGui.QIcon("icons/open.png"), "Open File", self)
        self.openAction.setStatusTip("Open an existing document")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtGui.QAction(QtGui.QIcon("icons/save.png"), "Save File", self)
        self.saveAction.setStatusTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)


        self.printAction = QtGui.QAction(QtGui.QIcon("icons/print.png"), "Print File", self)
        self.printAction.setStatusTip("Print document")
        self.printAction.setShortcut("Ctrl+P")
        self.printAction.triggered.connect(self.printHandler)

        self.previewAction = QtGui.QAction(QtGui.QIcon("icons/preview.png"), "Page View", self)
        self.previewAction.setStatusTip("Preview page")
        self.previewAction.setShortcut("Ctrl+Shift+P")
        self.previewAction.triggered.connect(self.preview)



        self.findAction = QtGui.QAction(QtGui.QIcon("icons/find.png"), "Find and Replace", self)
        self.findAction.setStatusTip("Find and replace words")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(find.Find(self).show)

        self.cutAction = QtGui.QAction(QtGui.QIcon("icons/cut.png"), "Cut", self)
        self.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.text.cut)

        self.copyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"), "Copy", self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.text.copy)

        self.pasteAction = QtGui.QAction(QtGui.QIcon("icons/paste.png"), "Paste", self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.text.paste)

        self.undoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"), "Undo", self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.text.undo)

        self.redoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"), "Redo", self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.text.redo)

        wordCountAction = QtGui.QAction(QtGui.QIcon("icons/count.png"), "See word / Symbol count", self)
        wordCountAction.setStatusTip("See word/symbol count")
        wordCountAction.setShortcut("Ctrl+W")
        wordCountAction.triggered.connect(self.wordCount)

        '''
        imageAction = QtGui.QAction(QtGui.QIcon("icons/image.png"), "Insert Image", self)
        imageAction.setStatusTip("Insert image")
        imageAction.setShortcut("Ctrl+Shift+I")
        imageAction.triggered.connect(self.insertImage)

        bulletAction = QtGui.QAction(QtGui.QIcon("icons/bullet.png"), "Insert Bullet List", self)
        bulletAction.setStatusTip("Insert bullet list")
        bulletAction.setShortcut("Ctrl+Shift+B")
        bulletAction.triggered.connect(self.bulletList)

        numberedAction = QtGui.QAction(QtGui.QIcon("icons/number.png"), "Insert Numbered List", self)
        numberedAction.setStatusTip("Insert numbered list")
        numberedAction.setShortcut("Ctrl+Shift+L")
        numberedAction.triggered.connect(self.numberList)
        '''

        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.buildAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.previewAction)


        self.toolbar.addSeparator()

        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.findAction)
        self.toolbar.addAction(wordCountAction)
        '''
        self.toolbar.addAction(imageAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(bulletAction)
        self.toolbar.addAction(numberedAction)
        '''
        #self.addToolBarBreak()

    def initFormatbar(self):

        #fontBox = QtGui.QFontComboBox(self)
        #fontBox.currentFontChanged.connect(lambda font: self.text.setCurrentFont(font))

        fontSize = QtGui.QSpinBox(self)

        fontSize.valueChanged.connect(lambda size: self.text.setFontPointSize(size))
        fontSize.valueChanged.connect(lambda size: self.text.setFontPointSize(size))

        fontSize.setValue(16)

        #fontColor = QtGui.QAction(QtGui.QIcon("icons/font-color.png"), "Change Font Color", self)
        #fontColor.triggered.connect(self.fontColorChanged)


        indentAction = QtGui.QAction(QtGui.QIcon("icons/indent.png"), "Indent Area", self)
        indentAction.setShortcut("Ctrl+Tab")
        indentAction.triggered.connect(self.indent)

        dedentAction = QtGui.QAction(QtGui.QIcon("icons/dedent.png"), "Dedent Area", self)
        dedentAction.setShortcut("Shift+Tab")
        dedentAction.triggered.connect(self.dedent)

        '''
        backColor = QtGui.QAction(QtGui.QIcon("icons/highlight.png"), "Change Background Color", self)
        backColor.triggered.connect(self.highlight)
        '''

        self.formatbar = self.addToolBar("Format")

        #self.formatbar.addWidget(fontBox)
        self.formatbar.addWidget(fontSize)

        self.formatbar.addSeparator()

        '''
        self.formatbar.addAction(fontColor)
        self.formatbar.addAction(backColor)

        self.formatbar.addSeparator()

        
        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(underlAction)
        self.formatbar.addAction(strikeAction)
        self.formatbar.addAction(superAction)
        self.formatbar.addAction(subAction)

        self.formatbar.addSeparator()

        
        self.formatbar.addAction(alignLeft)
        self.formatbar.addAction(alignCenter)
        self.formatbar.addAction(alignRight)
        self.formatbar.addAction(alignJustify)

        self.formatbar.addSeparator()
        '''

        self.formatbar.addAction(indentAction)
        self.formatbar.addAction(dedentAction)

    def initMenubar(self):

        menubar = self.menuBar()

        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")

        file.addAction(self.newAction)
        file.addAction(self.buildAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)

        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.copyAction)
        edit.addAction(self.pasteAction)
        edit.addAction(self.findAction)

        ###################################
        toolbarAction = QtGui.QAction("Toggle Toolbar", self)
        toolbarAction.triggered.connect(self.toggleToolbar)

        formatbarAction = QtGui.QAction("Toggle Formatbar", self)
        formatbarAction.triggered.connect(self.toggleFormatbar)

        statusbarAction = QtGui.QAction("Toggle Statusbar", self)
        statusbarAction.triggered.connect(self.toggleStatusbar)

        view.addAction(toolbarAction)
        view.addAction(formatbarAction)
        view.addAction(statusbarAction)

    def initUI(self):

        self.text = QtGui.QTextEdit(self)
        #self.setPlainText(DEF)
        self.text.setTabStopWidth(23)

        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()

        self.setCentralWidget(self.text)
        self.statusbar = self.statusBar()

        self.text.cursorPositionChanged.connect(self.cursorPosition)
        self.highlighter = MH(self.text,"Classic")
        self.setGeometry(253, 253, 950, 600)
        self.setWindowTitle("My Project")
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

        pal = QtGui.QPalette()
        bgc = QtGui.QColor(0, 0, 0)
        pal.setColor(QtGui.QPalette.Base, bgc)
        textc = QtGui.QColor(255, 255, 255)
        pal.setColor(QtGui.QPalette.Text, textc)
        self.setPalette(pal)

    def toggleToolbar(self):

        state = self.toolbar.isVisible()

        self.toolbar.setVisible(not state)

    def toggleFormatbar(self):

        state = self.formatbar.isVisible()

        self.formatbar.setVisible(not state)

    def toggleStatusbar(self):

        state = self.statusbar.isVisible()

        self.statusbar.setVisible(not state)

    def new(self):

        completer = DictionaryCompleter()
        te = CompletionTextEdit()
        te.setCompleter(completer)
        te.show()

    def build(self):

        os.system("gnome-terminal -e 'bash -c \"./a.sh; exec bash\"'")

    def open(self):

        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', ".", "*.cpp")

        if self.filename:
            with open(self.filename, "rt") as file:
                self.text.setText(file.read())

    def save(self):

        if not self.filename:
            self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')

        if not self.filename.endsWith(".cpp"):
            self.filename += ".cpp"

        with open(self.filename, "wt") as file:
            file.write(self.text.toPlainText())

    def preview(self):

        preview = QtGui.QPrintPreviewDialog()

        preview.paintRequested.connect(lambda p: self.text.print_(p))

        preview.exec_()

    def printHandler(self):

        # Open printing dialog
        dialog = QtGui.QPrintDialog()

        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.text.document().print_(dialog.printer())

    def cursorPosition(self):

        cursor = self.text.textCursor()

        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1

        self.statusbar.showMessage("Line: {} : Column: {}".format(line, col))

    def wordCount(self):

        wc = wordcount.WordCount(self)
        wc.getText()
        wc.show()

    def alignLeft(self):
        self.text.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.text.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.text.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.text.setAlignment(Qt.AlignJustify)

    def indent(self):

        cursor = self.text.textCursor()

        if cursor.hasSelection():

            temp = cursor.blockNumber()

            cursor.setPosition(cursor.anchor())

            diff = cursor.blockNumber() - temp

            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down

            for n in range(abs(diff) + 1):
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)

                cursor.insertText("\t")

                cursor.movePosition(direction)

        else:

            cursor.insertText("\t")

    def handleDedent(self, cursor):

        cursor.movePosition(QtGui.QTextCursor.StartOfLine)

        line = cursor.block().text()

        if line.startsWith("\t"):

            cursor.deleteChar()

        else:
            for char in line[:8]:

                if char != " ":
                    break

                cursor.deleteChar()

    def dedent(self):

        cursor = self.text.textCursor()

        if cursor.hasSelection():

            temp = cursor.blockNumber()

            cursor.setPosition(cursor.anchor())

            diff = cursor.blockNumber() - temp

            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down

            for n in range(abs(diff) + 1):
                self.handleDedent(cursor)

                cursor.movePosition(direction)

        else:
            self.handleDedent(cursor)


class DictionaryCompleter(QtGui.QCompleter):
    def __init__(self, parent=None):
        words = []
        try:
            f = open("/home/moinak/Desktop/proj_latest/word","r")
            for word in f:
                words.append(word.strip())
            f.close()
        except IOError:
            print "wrong path!!!"
        QtGui.QCompleter.__init__(self, words, parent)

class CompletionTextEdit(Main):
    def __init__(self, parent=None):
        super(CompletionTextEdit, self).__init__(parent)

        self.text.completer = None
        self.text.moveCursor(QtGui.QTextCursor.End)

    def setCompleter(self, completer):
        if self.text.completer:
            self.text.disconnect(self.text.completer, 0, self, 0)
        if not completer:
            return

        completer.setWidget(self)
        completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.text.completer = completer
        self.text.connect(self.text.completer,
            QtCore.SIGNAL("activated(const QString&)"), self.insertCompletion)

    def insertCompletion(self, completion):
        tc = self.text.textCursor()
        extra = (completion.length() -
            self.text.completer.completionPrefix().length())
        tc.movePosition(QtGui.QTextCursor.Left)
        tc.movePosition(QtGui.QTextCursor.EndOfWord)
        tc.insertText(completion.right(extra))
        self.text.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.text.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        if self.text.completer:
            self.text.completer.setWidget(self);
        QtGui.QTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        if self.text.completer and self.text.completer.popup().isVisible():
            if event.key() in (
            QtCore.Qt.Key_Enter,
            QtCore.Qt.Key_Return,
            QtCore.Qt.Key_Escape,
            QtCore.Qt.Key_Tab,
            QtCore.Qt.Key_Backtab):
                event.ignore()
                return

        ## press ctrl-Space to trigger auto - code completion

        isShortcut = (event.modifiers() == QtCore.Qt.ControlModifier and
                      event.key() == QtCore.Qt.Key_Space)
        if (not self.text.completer or not isShortcut):
            QtGui.QTextEdit.keyPressEvent(self.text, event)

        ## ctrl or shift key on it's own??
        ctrlOrShift = event.modifiers() in (QtCore.Qt.ControlModifier ,
                QtCore.Qt.ShiftModifier)
        if ctrlOrShift and event.text().isEmpty():
            # ctrl or shift key on it's own
            return

        eow = QtCore.QString("~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-=") #end of word

        hasModifier = ((event.modifiers() != QtCore.Qt.NoModifier) and
                        not ctrlOrShift)

        completionPrefix = self.textUnderCursor()

        if (not isShortcut and (hasModifier or event.text().isEmpty() or
        completionPrefix.length() < 3 or
        eow.contains(event.text().right(1)))):
            self.text.completer.popup().hide()
            return

        if (completionPrefix != self.text.completer.completionPrefix()):
            self.text.completer.setCompletionPrefix(completionPrefix)
            popup = self.text.completer.popup()
            popup.setCurrentIndex(
                self.text.completer.completionModel().index(0,0))

        cr = self.text.cursorRect()
        cr.setWidth(self.text.completer.popup().sizeHintForColumn(0)
            + self.text.completer.popup().verticalScrollBar().sizeHint().width())
        self.text.completer.complete(cr) ## popup it up!

if __name__ == "__main__":

    app = QtGui.QApplication([])
    completer = DictionaryCompleter()
    jbl = CompletionTextEdit()
    jbl.setCompleter(completer)
    jbl.show()
    app.exec_()

