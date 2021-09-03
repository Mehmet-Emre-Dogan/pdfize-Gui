# For GUI
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

# My files
from appSettingsGui import Ui_Settings
from commonFunctions import *

# Other
import sys

class mySettingsWindow(myWindowSkeleton):
    sigSettingsSaved = pyqtSignal(bool)
    def __init__(self):
        super(mySettingsWindow, self).__init__()
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(directory + appFolder + '\\img.png'))

        self.initSettings()
        self.settingsStrings = loadDict(directory + dataFolder + "\\appSettingsStrings.json")
        self.lang = self.settings["lang"]
        
        self.loadCboxThemes()
        self.loadCboxLang()

        self.ui.lineEditOutput.setText(self.settings["defaultOutputFolder"])
        self.ui.lineEditInput.setText(self.settings["defaultInputFolder"])

        # Btn connections
        self.ui.btnChgInput.clicked.connect(self.onBtnChgInput)
        self.ui.btnChgOutput.clicked.connect(self.onBtnChgOutput)
        self.ui.btnSavePrefs.clicked.connect(self.onBtnSavePrefs)

    def onBtnChgInput(self):
        txt = self.getDirectoryDialog(title=self.settingsStrings[self.lang]["fileDialogs"]["defaultTitle"])
        if DEBUG:
            print(f"Selected folder: {txt}")
        if txt:
            self.settings["defaultInputFolder"] = txt
            self.ui.lineEditInput.setText(txt)

    def onBtnChgOutput(self):
        txt = self.getDirectoryDialog(title=self.settingsStrings[self.lang]["fileDialogs"]["defaultTitle"])
        if txt:
            self.settings["defaultOutputFolder"] = txt
            self.ui.lineEditOutput.setText(txt)

    def onBtnSavePrefs(self):
        self.settings["theme"] = f"theme_{self.ui.comboBoxTheme.currentText()}.txt"
        currentLang = self.ui.comboBoxLang.currentText()
        if currentLang == "Türkçe":
            self.settings["lang"] = "TR"
        else:
            self.settings["lang"] = "EN"
        dumpSettings(self.settings)
        self.initSettings()
        self.loadCboxThemes()
        self.loadCboxLang()
        self.ui.lineEditOutput.setText(self.settings["defaultOutputFolder"])
        self.ui.lineEditInput.setText(self.settings["defaultInputFolder"])
        self.sigSettingsSaved.emit(True)

    def loadCboxLang(self):
        if self.lang == "TR":
            self.ui.comboBoxLang.setCurrentText("Türkçe")
        else:
            self.ui.comboBoxLang.setCurrentText("English")  


    def loadCboxThemes(self):
        self.ui.comboBoxTheme.clear()
        themes = os.listdir(directory + themeFolder)
        themes.sort(key=parse_version, reverse=False)
        themes = [getThemeName(theme) for theme in themes]
        self.ui.comboBoxTheme.addItems(themes)
        self.ui.comboBoxTheme.setCurrentIndex(themes.index(getThemeName(self.settings["theme"])))
        if DEBUG:
            print("Themes:")
            print(themes)


if __name__ == "__main__":
    def app():
        app = QtWidgets.QApplication(sys.argv)
        app.setStyle('Fusion')
        win = mySettingsWindow()
        # app.aboutToQuit.connect(win.onAboutToQuit)
        win.show()
        sys.exit(app.exec_())
    app()

    