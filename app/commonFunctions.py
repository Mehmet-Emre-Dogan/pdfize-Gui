from json import load, dump
import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialogButtonBox, QLabel, QMessageBox, QFileDialog, QMainWindow, QColorDialog, QPushButton
from pkg_resources import parse_version # Sorting function similar enough to natural sort algorithm

DEBUG = False

###############################
"""Files and folders"""
###############################   

directory = os.path.dirname(os.path.dirname(__file__))
dataDirectory = directory +  "\\data"

settingsFile = "\\settings.json"
configFile = "\\confi.json"

appFolder = "\\app"
dataFolder = "\\data"
inputFolder = "\\input"
outputFolder = "\\output"
themeFolder = "\\themes"

#####################################################################################

###############################
"""Dictionary loaders and dumpers"""
###############################   

def loadSettings():
    global dataDirectory, settingsFile
    filepath = dataDirectory + settingsFile
    with open(filepath, "r", encoding="utf-8") as fil:
        dictToReturn = load(fil)
    return dictToReturn

def dumpSettings(settingsDict):
    global dataDirectory, settingsFile
    filepath = dataDirectory + settingsFile
    with open(filepath, "w", encoding="utf-8") as fil:
        dump(settingsDict, fil)

def loadConfig():
    global dataDirectory, configFile
    filepath = dataDirectory + configFile
    with open(filepath, "r", encoding="utf-8") as fil:
        dictToReturn = load(fil)
    return dictToReturn

def dumpConfig(configDict):
    global dataDirectory, configFile
    filepath = dataDirectory + configFile
    with open(filepath, "w", encoding="utf-8") as fil:
        dump(configDict, fil)

def loadDict(filepath):
    with open(filepath, "r", encoding="utf-8") as fil:
        dictToReturn = load(fil)
    return dictToReturn

def dumpDict(dictionary:dict, filepath):
    with open(filepath, "w", encoding="utf-8") as fil:
        dump(dictionary, fil)

#####################################################################################

def getThemeName(filename:str):
    filename = filename.split(".")[0] # Split from "." to split real filename and file extension. Then assign real filename to variable
    return filename[6:] # Get rid of the "theme_" part

#####################################################################################


class myWindowSkeleton(QMainWindow):

    def initSettings(self):
        self.settings = loadSettings()
        self.msgBoxStrs = loadDict(directory + dataFolder + "\\messageboxStrings.json")
        self.lang = self.settings["lang"]
        self.cosmeticallyUpdate()

        # Update themes, texts etc on language or theme change
    def cosmeticallyUpdate(self):
        # Adjust language
        if self.settings["lang"] == "TR":
            self.ui.translateTR(self)
        else:
            self.ui.retranslateUi(self)

        # Adjust theme
        styleSheet = ""
        try:
            with open(directory + themeFolder + "\\" + self.settings["theme"]) as fil:
                styleSheet = fil.read()
                # if DEBUG:
                #     print(styleSheet)
        except Exception as ex:
            if DEBUG:
                print(ex)
            styleSheet = ""
        self.styleSheetStr = styleSheet
        self.setStyleSheet("")
        self.setStyleSheet(styleSheet)

#####################################################################################

    ###############################
    """Message boxes"""
    ###############################

    # See the link below to learn more about editing texts of message box buttons
    # https://stackoverflow.com/questions/35887523/qmessagebox-change-text-of-standard-button

    def infoMessage(self, title="Info", text="Text text"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon(directory + appFolder + '\\img.png'))
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        btnOk = msg.button(QMessageBox.Ok)
        btnOk.setText(self.msgBoxStrs[self.lang]["ok"])
        msg.setStyleSheet(self.styleSheetStr)
        msg.exec_()

    def errorMessage(self, title="Error", text="An error occured"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon(directory + appFolder + '\\img.png'))
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        btnOk = msg.button(QMessageBox.Ok)
        btnOk.setText(self.msgBoxStrs[self.lang]["ok"])
        msg.setStyleSheet(self.styleSheetStr)
        msg.exec_()

    def confirmationMsg(self, title="Question", text="Are you sure doing xyz?"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon(directory + appFolder + '\\img.png'))
        msg.setText(text)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        btnYes = msg.button(QMessageBox.Yes)
        btnYes.setText(self.msgBoxStrs[self.lang]["yes"])
        btnNo = msg.button(QMessageBox.No)
        btnNo.setText(self.msgBoxStrs[self.lang]["no"])
        msg.setStyleSheet(self.styleSheetStr)
        answer = msg.exec_()
        return answer == QMessageBox.Yes

    # For more info about QFileDialog objects, visit the links below
    # https://learndataanalysis.org/source-code-how-to-use-qfiledialog-file-dialog-in-pyqt5/

    # https://stackoverflow.com/questions/59245576/attributeerror-qdialog-object-has-no-attribute-qfiledialog
    # https://stackoverflow.com/questions/28916010/qfiledialog-to-open-multiple-files

    def getDirectoryDialog(self, title="Select folder"):
        response = QFileDialog.getExistingDirectory(self, caption=title)
        return response

    def getFilesDialog(self, title="Select files", path=directory, filter="All files (*.*)"):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFiles)
        fileList = fileDialog.getOpenFileNames(caption=title, directory=path, filter=filter)[0]
        return fileList

    
    def colorDialog(self, title="Pick a color"):
        colorDia = QColorDialog()
        # colorDia.setOption(QColorDialog.DontUseNativeDialog)
        colorDia.setWindowTitle(title)
        colorDia.setWindowIcon(QtGui.QIcon(directory + appFolder + '\\img.png'))
        colorDia.setCustomColor(0, QtGui.QColor(196, 255, 0)) # Index, color
        colorDia.setCustomColor(1, QtGui.QColor(255, 196, 0)) # Index, color
        colorDia.setStyleSheet(self.styleSheetStr)

        for widget in colorDia.children():
            if isinstance(widget, QLabel) or isinstance(widget, QPushButton):
                if DEBUG:
                    print(widget.text())

                if widget.text() == "&Basic colors":
                    widget.setText(self.msgBoxStrs[self.lang]["basicColors"])
                elif widget.text() == "&Pick Screen Color":
                    widget.setText(self.msgBoxStrs[self.lang]["pickScrColor"])
                elif widget.text() == "&Custom colors":
                    widget.setText(self.msgBoxStrs[self.lang]["customColors"])
                elif widget.text() == "&Add to Custom Colors":
                    widget.setText(self.msgBoxStrs[self.lang]["addToCustomColors"])
            elif isinstance(widget, QDialogButtonBox):
                for button in widget.buttons():
                    if DEBUG:
                        print(button.text())
                    
                    if button.text() == "OK":
                        button.setText(self.msgBoxStrs[self.lang]["ok"])
                    elif button.text() == "Cancel":
                        button.setText(self.msgBoxStrs[self.lang]["cancel"])

        ok = colorDia.exec_()
        color = colorDia.selectedColor()
        if DEBUG:
            print(f"Ok: {ok} Color: {color}")

        if ok:
            return [color.red(), color.green(), color.blue()]
        else:
            return None

#####################################################################################

class emergencyMessage(object):
    def infoMessage(self, title="Info", text="Text text"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def errorMessage(self, title="Error", text="An error occured"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        btnOk = msg.button(QMessageBox.Ok)
        msg.exec_()

    def confirmationMsg(self, title="Question", text="Are you sure doing xyz?"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        answer = msg.exec_()
        return answer == QMessageBox.Yes

#####################################################################################

if __name__ == "__main__" and DEBUG:
    print("Debugging dictionary loaders and dumpers")
    settings = loadSettings()
    config = loadConfig()
    print(f"settings: {str(settings)}")
    print(f"config: {str(config)}")
    print("Swapping settings and config...")
    dumpConfig(settings)
    dumpSettings(config)
    settings = loadSettings()
    config = loadConfig()
    print(f"settings: {str(settings)}")
    print(f"config: {str(config)}")
    print("Swapping back settings and config...")
    dumpConfig(settings)
    dumpSettings(config)
    settings = loadSettings()
    config = loadConfig()
    print(f"settings: {str(settings)}")
    print(f"config: {str(config)}")
    print("Debug completed!")