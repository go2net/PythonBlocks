from PyQt4 import QtCore, QtGui, QtXml

class XmlHandler(QtXml.QXmlDefaultHandler):
    def __init__(self, root):
        QtXml.QXmlDefaultHandler.__init__(self)
        self._root = root
        self._item = None
        self._text = ''
        self._error = ''

    def startElement(self, namespace, name, qname, attributes):
        if qname == 'folder' or qname == 'item':
            if self._item is not None:
                self._item = QtGui.QTreeWidgetItem(self._item)
            else:
                self._item = QtGui.QTreeWidgetItem(self._root)
            self._item.setData(0, QtCore.Qt.UserRole, qname)
            self._item.setText(0, 'Unknown Title')
            if qname == 'folder':
                self._item.setExpanded(True)
            elif qname == 'item':
                self._item.setText(1, attributes.value('type'))
        self._text = ''
        return True

    def endElement(self, namespace, name, qname):
        if qname == 'title':
            if self._item is not None:
                self._item.setText(0, self._text)
        elif qname == 'folder' or qname == 'item':
            self._item = self._item.parent()
        return True

    def characters(self, text):
        self._text += text
        return True

    def fatalError(self, exception):
        print('Parse Error: line %d, column %d:\n  %s' % (
              exception.lineNumber(),
              exception.columnNumber(),
              exception.message(),
              ))
        return False

    def errorString(self):
        return self._error

class Window(QtGui.QTreeWidget):
    def __init__(self):
        QtGui.QTreeWidget.__init__(self)
        self.header().setResizeMode(QtGui.QHeaderView.Stretch)
        self.setHeaderLabels(['Title', 'Type'])
        source = QtXml.QXmlInputSource()
        source.setData(xml)
        handler = XmlHandler(self)
        reader = QtXml.QXmlSimpleReader()
        reader.setContentHandler(handler)
        reader.setErrorHandler(handler)
        reader.parse(source)

xml = """\
<root>
    <folder>
        <title>Folder One</title>
        <item type="1">
            <title>Item One</title>
        </item>
        <item type="1">
            <title>Item Two</title>
        </item>
        <item type="2">
            <title>Item Three</title>
        </item>
        <folder>
            <title>Folder Two</title>
            <item type="3">
                <title>Item Four</title>
            </item>
            <item type="0">
                <title>Item Five</title>
            </item>
            <item type="1">
                <title>Item Six</title>
            </item>
        </folder>
    </folder>
    <folder>
        <title>Folder Three</title>
        <item type="0">
            <title>Item Six</title>
        </item>
        <item type="2">
            <title>Item Seven</title>
        </item>
        <item type="2">
            <title>Item Eight</title>
        </item>
    </folder>
</root>
"""

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec_())
