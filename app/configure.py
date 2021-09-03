# For GUI
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import PyQt5
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtCore import pyqtSignal

# My files
from configGui import Ui_configWindow
from commonFunctions import *

# Other
import sys

class myConfigWindow(myWindowSkeleton):
    sigConfigSaved = pyqtSignal(bool)
    def __init__(self):
        super(myConfigWindow, self).__init__()
        self.ui = Ui_configWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(directory + appFolder + '\\img.png'))

        self.initSettings()
        self.resizeWindow()
        self.config = loadConfig()

        self.lang = self.settings["lang"]
        self.initializeUiElements()

        # Btn connections
        self.ui.btnSavePrefs.clicked.connect(self.saveConfig)
        self.ui.btnChgPNumFore.clicked.connect(self.changePNumFore)
        self.ui.btnChgNumBack.clicked.connect(self.changePNumBack)
        self.ui.btnChgWaterColor.clicked.connect(self.changeWaterFore)

        self.ui.checkBoxPnumAddBG.toggled.connect(self.setEnabledPnumBack)
        self.ui.checkBoxEnableWater.toggled.connect(self.setEnabledWatermarkElements)
        self.ui.checkBoxEnableCrop.toggled.connect(self.setEnabledCroppingElements)

    def resizeWindow(self):
        # Adjust window size
        if DEBUG:
            print(f"Window size old: {self.size()}")
        self.resize(self.minimumSizeHint())
        if DEBUG:
            print(f"Window size: {self.size()}")

    def changePNumFore(self):
        color = self.colorDialog(self.msgBoxStrs[self.lang]["pickAColor"])
        if color:
            self.config["pgnumColor"] = color.copy()
            self.ui.lblPnumFore.setStyleSheet(f'color: rgb({self.config["pgnumColor"][0]}, {self.config["pgnumColor"][1]}, {self.config["pgnumColor"][2]});')
            self.previewPageNum()
            if DEBUG:
                print(f"page number fore color: {color}")

    def changePNumBack(self):
        color = self.colorDialog(self.msgBoxStrs[self.lang]["pickAColor"])
        if color:
            self.config["bgColor"] = color.copy()
            self.ui.lblPnumBack.setStyleSheet(f'color: rgb({self.config["bgColor"][0]}, {self.config["bgColor"][1]}, {self.config["bgColor"][2]});')
            self.previewPageNum()
            if DEBUG:
                print(f"page number back color: {color}")

    def changeWaterFore(self):
        color = self.colorDialog(self.msgBoxStrs[self.lang]["pickAColor"])
        if color:
            newColorArray = color.copy()
            newColorArray.append(self.ui.spinBoxWaterOpacity.value())
            self.config["watermarkColor"] = newColorArray
            self.ui.lblWaterColor.setStyleSheet(f'color: rgb({self.config["watermarkColor"][0]}, {self.config["watermarkColor"][1]}, {self.config["watermarkColor"][2]});')
            if DEBUG:
                print(f"page number back color: {color}")
    
    # Adjust whether items enabled or disabled

    def setEnabledPnumBack(self):
        isEnabled = self.ui.checkBoxPnumAddBG.isChecked()
        if DEBUG:
            print(f"Checkbox add page number background ticked: {isEnabled}")
        self.config["isBgExists"] = isEnabled

        self.ui.groupBoxBckColor.setEnabled(isEnabled)
        self.previewPageNum()
    
    def setEnabledWatermarkElements(self):
        isEnabled = self.ui.checkBoxEnableWater.isChecked()
        self.config["watermarkEnabled"] = isEnabled

        self.ui.lineEditWaterText.setEnabled(isEnabled)
        self.ui.groupBoxWaterColor.setEnabled(isEnabled)
        self.ui.spinBoxWaterFontSize.setEnabled(isEnabled)
        self.ui.spinBoxWaterOpacity.setEnabled(isEnabled)
        self.ui.lblWaterOpacity.setEnabled(isEnabled)
        self.ui.spinBoxWaterAngle.setEnabled(isEnabled)
        self.ui.lblAngle.setEnabled(isEnabled)
        self.ui.lblFontSize2.setEnabled(isEnabled)

    def setEnabledCroppingElements(self):
        isEnabled = self.ui.checkBoxEnableCrop.isChecked()
        self.config["noCrop"] = not isEnabled

        self.ui.spinBoxLeftMargin.setEnabled(isEnabled)
        self.ui.spinBoxRightMargin.setEnabled(isEnabled)
        self.ui.spinBoxUpMargin.setEnabled(isEnabled)
        self.ui.spinBoxDownMargin.setEnabled(isEnabled)

        self.ui.lblLeft.setEnabled(isEnabled)
        self.ui.lblRight.setEnabled(isEnabled)
        self.ui.lblUp.setEnabled(isEnabled)
        self.ui.lblDown.setEnabled(isEnabled)


    def initializeUiElements(self):
        # Page number
        self.ui.radioFil.setChecked(self.config["pagenumIsFilename"])
        self.ui.radioNumb.setChecked(not self.config["pagenumIsFilename"])
        self.ui.lblPnumFore.setStyleSheet(f'color: rgb({self.config["pgnumColor"][0]}, {self.config["pgnumColor"][1]}, {self.config["pgnumColor"][2]});')
        self.ui.checkBoxPnumAddBG.setChecked(self.config["isBgExists"])
        self.ui.lblPnumBack.setStyleSheet(f'color: rgb({self.config["bgColor"][0]}, {self.config["bgColor"][1]}, {self.config["bgColor"][2]});')
        self.ui.comboBoxPnumPos.setCurrentIndex(self.config["numPos"] - 1)
        self.setEnabledPnumBack()

        # Watermark
        self.ui.checkBoxEnableWater.setChecked(bool(self.config["watermarkEnabled"]))
        self.ui.lineEditWaterText.setText(self.config["watermark"])
        self.ui.lblWaterColor.setStyleSheet(f'color: rgb({self.config["watermarkColor"][0]}, {self.config["watermarkColor"][1]}, {self.config["watermarkColor"][2]});')
        self.ui.spinBoxWaterFontSize.setValue(self.config["fontSizeWatermark"])
        self.ui.spinBoxWaterOpacity.setValue(self.config["watermarkColor"][3])
        self.ui.spinBoxWaterAngle.setValue(self.config["watermarkAngle"])
        self.setEnabledWatermarkElements()

        # Cropping
        isCropEn = not self.config["noCrop"]
        self.ui.checkBoxEnableCrop.setChecked(isCropEn)
        self.setEnabledCroppingElements()

        self.ui.spinBoxLeftMargin.setValue(self.config["left"])
        self.ui.spinBoxRightMargin.setValue(self.config["right"])
        self.ui.spinBoxUpMargin.setValue(self.config["up"])
        self.ui.spinBoxDownMargin.setValue(self.config["down"])

        # Other
        self.ui.spinBoxDpi.setValue(self.config["dpi"])
        self.ui.spinBoxFidelity.setValue(self.config["fidelity"])

    def saveConfig(self):
        try:
            # Page number
            self.config["pagenumIsFilename"] = self.ui.radioFil.isChecked()
            self.config["isBgExists"] = self.ui.checkBoxPnumAddBG.isChecked()
            self.config["fontSize"] = self.ui.spinBoxPNumFontSize.value()
            self.config["numPos"] = (self.ui.comboBoxPnumPos.currentIndex() + 1)

            # Watermark
            self.config["watermarkEnabled"] = self.ui.checkBoxEnableWater.isChecked()
            self.config["watermark"] = self.ui.lineEditWaterText.text()
            self.config["fontSizeWatermark"] = self.ui.spinBoxWaterFontSize.value()
            self.config["watermarkColor"][3] = self.ui.spinBoxWaterOpacity.value()
            self.config["watermarkAngle"] = self.ui.spinBoxWaterAngle.value()

            # Crop
            self.config["noCrop"] = not self.ui.checkBoxEnableCrop.isChecked()
            self.config["up"] = self.ui.spinBoxUpMargin.value()
            self.config["down"] = self.ui.spinBoxDownMargin.value()
            self.config["left"] = self.ui.spinBoxLeftMargin.value()
            self.config["right"] = self.ui.spinBoxRightMargin.value()

            # Other
            self.config["dpi"] = self.ui.spinBoxDpi.value()
            self.config["fidelity"] = self.ui.spinBoxFidelity.value()

            dumpConfig(self.config)
            self.sigConfigSaved.emit(True)
            self.infoMessage(title=self.msgBoxStrs[self.lang]["success"], text=self.msgBoxStrs[self.lang]["prefsSaved"])
        
        except (Exception, OSError, FileNotFoundError) as err:
            self.errorMessage(title=self.msgBoxStrs[self.lang]["errorOccured"], text=str(err))

    def previewPageNum(self):
        if self.config["isBgExists"]:
            self.ui.lblPreviewNum.setStyleSheet(f"""color: rgb({self.config["pgnumColor"][0]}, {self.config["pgnumColor"][1]}, {self.config["pgnumColor"][2]});
                                                    background-color: rgb({self.config["bgColor"][0]}, {self.config["bgColor"][1]}, {self.config["bgColor"][2]});
            
            """)
        else:
            self.ui.lblPreviewNum.setStyleSheet(f'color: rgb({self.config["pgnumColor"][0]}, {self.config["pgnumColor"][1]}, {self.config["pgnumColor"][2]});')
        self.ui.spinBoxPNumFontSize.setValue(self.config["fontSize"])


if __name__ == "__main__":
    def app():
        app = QtWidgets.QApplication(sys.argv)
        emrgMsg = emergencyMessage()
        try:
            app.setStyle('Fusion')
            win = myConfigWindow()
            # app.aboutToQuit.connect(win.onAboutToQuit)
            win.show()
            sys.exit(app.exec_())
        except (Exception, OSError, FileNotFoundError, AttributeError) as err:
            emrgMsg.errorMessage(text=str(err))

    app()