from PySide6.QtWidgets import QMessageBox, QMenu, QFileDialog as QFile
from PySide6.QtGui import QAction
from libs.io import io
from libs.stdout import print
from ._base._logic import LogicFrame
from subprocess import Popen

class Action:
    tool = ... #type: Tool
    visible = True
    enabled = True
    shortcut = ''
    def __call__(self, lang):
        action = QAction(self.tool.get_name(lang), self.tool.ui.MainWindow)
        action.setStatusTip(self.tool.get_doc(lang))
        action.setVisible(self.visible)
        action.setEnabled(self.enabled)
        action.setShortcut(self.shortcut)
        action.triggered.connect(lambda *x,_t=self.tool:_t())
        return action

class Menu:
    tool = ... #type: Tool
    tools = [] #type: list[Tool]
    visible = True
    enabled = True
    def __call__(self, lang):
        for tool in self.tools: tool.ui = self.tool.ui
        menu = QMenu(self.tool.get_name(lang), self.tool.ui.ui.menuBar)
        menu.setVisible(self.visible)
        menu.setEnabled(self.enabled)
        for tool in self.tools:
            action = tool.action(lang)
            action.setParent(menu)
            if tool.type: action.setMenu(action)
            else: menu.addAction(action)
        menu.hide()
        return menu

class Tool:
    ui = ... #type: LogicFrame
    #Basic Infos
    attr = 'White',
    name = 'New Tool'
    name_zh = ''
    doc = 'This is a new tool'
    doc_zh = ''
    help = 'No Argument Needed'
    entrance = None
    def __init__(self, type=0):
        self.type = type
        self.action = Menu() if type else Action()
        self.action.tool = self
    def __call__(self, *args):
        if self.entrance: self.entrance(*args)
        else: print(f"Can't find an entrance of the tool {self.name}", 'Red')
    #Get Info in Diffrent Languages
    _get = lambda self, attr, lang:getattr(self, attr if lang else f'{attr}_zh')
    def get_name(self, lang):
        return self._get('name', lang)
    def get_doc(self, lang):
        return self._get('doc', lang)
    #Show Info to User
    def _msg(self, info, icon):
        msg = QMessageBox(self.ui.MainWindow)
        msg.setWindowTitle(self.name)
        msg.setText(str(info))
        msg.setIcon(icon)
        return msg
    def Show(self, info):
        self._msg(info, QMessageBox.Icon.Information).exec()
    def Warn(self, info):
        self._msg(info, QMessageBox.Icon.Warning).exec()
    def Error(self, info):
        self._msg(info, QMessageBox.Icon.Critical).exec()
    def Ask(self, info):
        msg = self._msg(info, QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        return msg.exec() == QMessageBox.StandardButton.Yes
    #File Operation
    def OpenDir(self, title=None, dir='./'):
        if not title: title = self.name
        return QFile.getExistingDirectory(self.ui.MainWindow, title, dir)
    def OpenFile(self, title=None, dir='./', type=...):
        if not title: title = self.name
        return QFile.getOpenFileName(self.ui.MainWindow, title, dir, type)[0]
    def OpenFiles(self, title=None, dir='./', type=...):
        if not title: title = self.name
        return QFile.getOpenFileNames(self.ui.MainWindow, title, dir, type)[0]
    def SaveFile(self, title=None, dir='./', type=...):
        if not title: title = self.name
        return QFile.getSaveFileName(self.ui.MainWindow, title, dir, type)[0]
    @staticmethod
    def Pop(f):
        return Popen(f'"{f}"', shell=True)

__all__ = ['Tool', 'print', 'io']