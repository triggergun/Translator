from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog as QFile
from PySide6.QtCore import QTranslator, QTimer
from libs.translate import translate, online_translate
from libs.config import Setting
from libs.tool import main as tool_main, load
from .main import UILogic
from libs.ui.setting import Ui_Settings
from pywinstyles import apply_style
from threading import Thread
from time import sleep
from res import version

class LogicFrame:
    def __init__(self, file=None):
        super().__init__()
        #Window Build
        self.app = QApplication()
        self.MainWindow = QMainWindow()
        self.ui = UILogic()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()
        #Setting
        self.setting = QDialog(self.MainWindow)
        self.setting_ui = Ui_Settings()
        self.setting_ui.setupUi(self.setting)
        #Variable
        self.tool_thread = Thread()
        self.online = False
        self.running = True
        #Connections
        self.MainWindow.closeEvent = self.close
        self.ui.actionSetting.triggered.connect(self.setting_show)
        self.ui.actionOnline.triggered.connect(self.command_online)
        self.ui.actionRun.triggered.connect(lambda:self.start_tool() if not self.tool_thread.is_alive() else ...)
        self.setting_ui.Lang.currentIndexChanged.connect(lambda:self.retrans(self.setting_ui.Lang.currentIndex()))
        self.ui.actionTool_Reload.triggered.connect(lambda:load() or self.show_tools())
        self.setting_ui.buttonBox.accepted.connect(self.accept)
        self.setting_ui.buttonBox.rejected.connect(self.setting.hide)
        self.setting_ui.viewVocabulary.clicked.connect(lambda:(lambda f:self.setting_ui.Vocabulary.setText(f) if f else ...)(QFile.getOpenFileName(self.setting, 'Default Vocabulary File', './', '*.tvf')[0]))
        self.setting_ui.Auto_Save.stateChanged.connect(lambda:self.setting_ui.Interval.setEnabled(self.setting_ui.Auto_Save.isChecked()))
        #UI
        self.retrans()
        self.ui.setShotcuts()
        self.ui.load_dicts()
        apply_style(self.MainWindow, 'acrylic')
        #Threading
        self.argv = file
        Thread(target=lambda:self.ui.load(file)).start()
        Thread(target=self.auto_translate).start()
        self.auto_save_timer = self.ticker(lambda:self.ui.save_all() if not self.tool_thread.is_alive() and Setting.Auto_save else ..., Setting.Auto_save_interval*1000)
        self.ticker(lambda:self.ui.actionRun.setEnabled(not self.tool_thread.is_alive()), 500)
        self.ticker(lambda:(lambda f:(self.ui.load(f) if f!='Show\n' else ...) or (self.MainWindow.activateWindow() or self.MainWindow.showNormal()) if f else ...)(open('res/running').read().split('\n')[1]) or open('res/running', 'w').write('True\n'), 500)

    def ticker(self, func, interval):
        timer = QTimer(self.MainWindow)
        timer.timeout.connect(func)
        timer.start(interval)
        return timer

    def accept(self):
        Setting.Auto_save = self.setting_ui.Auto_Save.isChecked()
        Setting.Auto_save_interval = self.setting_ui.Interval.value()
        self.auto_save_timer.setInterval(Setting.Auto_save_interval*1000)
        Setting.Vocubulary = self.setting_ui.Vocabulary.text()
        Setting.Key_Add = self.setting_ui.Key_Add.keySequence().toString()
        Setting.Key_Del = self.setting_ui.Key_Delete.keySequence().toString()
        Setting.Key_Top = self.setting_ui.Key_Top.keySequence().toString()
        self.ui.setShotcuts()
        Setting.dump()

    def setting_show(self):
        apply_style(self.setting, 'acrylic')
        self.setting_ui.Lang.setCurrentIndex(Setting.Language)
        self.setting_ui.Auto_Save.setChecked(Setting.Auto_save)
        self.setting_ui.Interval.setEnabled(Setting.Auto_save)
        self.setting_ui.Interval.setValue(Setting.Auto_save_interval)
        self.setting_ui.Vocabulary.setText(Setting.Vocubulary)
        self.setting_ui.Key_Add.setKeySequence(Setting.Key_Add)
        self.setting_ui.Key_Delete.setKeySequence(Setting.Key_Del)
        self.setting_ui.Key_Top.setKeySequence(Setting.Key_Top)
        self.setting.show()

    def show_tools(self):
        self.ui.menuTools_Run.clear()
        from libs.tool import Tools
        for tl in Tools.values():
            tl.ui = self
            action = tl.action(Setting.Language)
            if tl.type: self.ui.menuTools_Run.addMenu(action)
            else: self.ui.menuTools_Run.addAction(action)

    def command_online(self):
        if self.online:
            self.online = False
            self.ui.menuDicts.setEnabled(True)
        else:
            self.online = True
            self.ui.menuDicts.setEnabled(False)

    def retrans(self, lang=None):
        if lang is not None:
            Setting.Language = lang
        if Setting.Language:
            self.setting_ui.retranslateUi(self.setting)
            self.ui.retranslateUi(self.MainWindow)
        else:
            translator = QTranslator(self.MainWindow)
            self.app.installTranslator(translator)
            translator.load('./res/lang/setting.qm')
            self.setting_ui.retranslateUi(self.setting)
            translator.load('./res/lang/zh.qm')
            self.ui.retranslateUi(self.MainWindow)
            self.app.removeTranslator(translator)
        self.MainWindow.setWindowTitle(f'{self.MainWindow.windowTitle()} {version.Translator}')
        self.show_tools()

    def auto_translate(self):
        tick = 0
        while self.running:
            #Auto Translate
            ticking = tick > 20
            if self.ui.text_changed or ticking:
                tick = 0
                self.ui.text_changed = False
                word = self.ui.Word_Entry.text().strip()
                if word != '':
                    if (not ticking) and (word not in self.ui.Bank.words):
                        self.ui.Bank.roll(word)
                    self.ui._result = online_translate(word, self.ui.Bank.results) if self.online else translate(word, self.ui.Bank.results)
                    if self.ui.text_changed:
                        continue
                    self.ui.signal.set_result_singal.emit()
            tick += 1
            sleep(0.05)

    def start_tool(self):
        self.tool_thread = Thread(target=tool_main, daemon=True)
        self.tool_thread.start()

    def exec(self): return self.app.exec()

    def close(self, *evt):
        self.running = False
        if Setting.Auto_save:
            self.ui.save_all(False)
        open('res/running', 'w').write('False\n')
        
