# For function definitions
from typing import List

# My files
from mainGui import Ui_mainWindow
import pdfizer
from commonFunctions import *
from appSettings import mySettingsWindow
from configure import myConfigWindow

# For GUI
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QThread, pyqtSignal

# from PyQt5 import QtCore 
from PyQt5 import QtGui 
import sys

# Other libraries
import os
from time import sleep
from pathlib import Path
import psutil

##########################################################################################
DEBUG = False
SLEEP = False
MAX_LEN_STR = 45
TICK_INTERVAL = 1
directory = os.path.dirname(os.path.dirname(__file__))  # For more info about parent directories, visit the link. 
                                                        # https://stackoverflow.com/questions/58778625/how-to-get-the-path-of-the-parent-directory-in-python

##########################################################################################

class ticker(QThread):
    tickSignal = pyqtSignal(int)
    def run(self):
        while True:
            self.tickSignal.emit(1)
            sleep(TICK_INTERVAL)

class pdfizerWorker(QThread):
    sigProgress = pyqtSignal(str) # For progressbar position
    sigFile = pyqtSignal(str) # For filename being processing
    successSig = pyqtSignal(str) # Whether worked successfully saved pdf or an error message
    def __init__(self, images:List[str]):
        super(pdfizerWorker, self).__init__()
        self.rawImages = images
        self.processedImages = []
        self.cou = len(images)

    def run(self):
        try:
            for i, image in enumerate(self.rawImages):
                i = i + 1
                self.sigFile.emit(image.split("/")[-1])
                self.sigProgress.emit(f"{i}/{self.cou}")
                self.processedImages.append(pdfizer.process(image, i))
                if SLEEP:
                    sleep(0.5)
                # if DEBUG: # Shows only shallow ram usage
                #     print(f"processed images ram usage: {sys.getsizeof(self.processedImages)/(1024**3)} GB")
            
            self.successSig.emit("writingToPdfFile")
            whether = pdfizer.save2(self.processedImages)
            self.successSig.emit(whether)
        except (Exception, ValueError, OSError, FileNotFoundError, IndexError) as err:
            self.successSig.emit(str(err))
        finally:
            # Clean up ram
            for im in self.processedImages:
                im.close()

            # if DEBUG:
            #     print(f"processed images cou: {len(self.processedImages)}")

class myWindow(myWindowSkeleton):
    def __init__(self):
        super(myWindow, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(directory + appFolder + '\\img.png'))
        
        # Variables
        self.settings = {}
        self.config = {}
        self.styleSheetStr = ""
        # self.initSettings()
        self.mainStrs = loadDict(directory + dataFolder + "\\mainStrings.json")
        self.status = "ready"
        self.process = psutil.Process(os.getpid())

        self.statusLabel = QLabel()
        self.statusBar().addWidget(self.statusLabel)

        self.initSettings()
        self.initConfig()
        self.initSettings2()
        self.prepareFiles()
        self.emptyPB()
        self.showFileCou()

        self.ui.menubar.triggered.connect(self.whoGotSelected)

        self.ticker = ticker()
        self.ticker.tickSignal.connect(self.showRamUsage)
        self.ticker.start()
        
        # Btn connections
        self.ui.btnSelectFolder.clicked.connect(self.onSelectFolderClicked)
        self.ui.btnSelectFiles.clicked.connect(self.onSelectFilesClicked)
        self.ui.btnConfigure.clicked.connect(self.setConfig)
        self.ui.btnPdfize.clicked.connect(self.startPdfizing)
        self.ui.btnOpenOutputFolder.clicked.connect(self.openOutputDir)

        self.setAcceptDrops(True)

    # Drag and drop. See the link below for more info
    # https://gist.github.com/peace098beat/db8ef7161508e6500ebe
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [item.toLocalFile() for item in event.mimeData().urls() if  any(str(item.toLocalFile()).endswith(extension) for extension in pdfizer.validExtensions)]
        if len(files):
            self.files = files
            self.config["inputFolder"] = "selectedMultiFiles"
            dumpConfig(self.config)
            self.setStatusbarLabelText()
            self.showFileCou()
        if DEBUG:
            for item in event.mimeData().urls():
                print(item.toLocalFile())


    ################################
    """Pdfizing operations"""
    ################################   

    def setControlBtnsEnabled(self, whether):
        self.ui.btnPdfize.setEnabled(whether)
        self.ui.btnSelectFolder.setEnabled(whether)
        self.ui.btnSelectFiles.setEnabled(whether)

    def onSelectFolderClicked(self):
        txt = self.getDirectoryDialog(title=self.msgBoxStrs[self.lang]["selectFolder"])
        if txt:
            self.config["inputFolder"] = txt
            self.setStatusbarLabelText()
            dumpConfig(self.config)
            self.prepareFiles()
            self.showFileCou()

    def onSelectFilesClicked(self):
        files = self.getFilesDialog(title=self.msgBoxStrs[self.lang]["selectPics"], filter=self.msgBoxStrs[self.lang]["pictures"])
        if len(files):
            self.files = files
            self.config["inputFolder"] = "selectedMultiFiles"
            dumpConfig(self.config)
            self.setStatusbarLabelText()
            self.showFileCou()
            if DEBUG:
                for file in self.files:
                    print(file)

    def prepareFiles(self):
        try:
            self.files = pdfizer.getFiles(self.config["inputFolder"])
        except:
            self.infoMessage(title=self.msgBoxStrs[self.lang]["errorOccured"], text=self.msgBoxStrs[self.lang]["usingFactoryDefaultDir"])
            self.files = pdfizer.getFiles(directory + inputFolder)
        if DEBUG:
            for file in self.files:
                print(file)

    def startPdfizing(self):
        if not len(self.files):
            self.errorMessage(title=self.msgBoxStrs[self.lang]["error"], text=self.mainStrs[self.lang]["thisFolderContainsNoIms"])
            self.status = "ready"
            self.ui.lblStatus.setText(self.mainStrs[self.lang][self.status])
            return
        self.setControlBtnsEnabled(False)
        self.status = "processing"
        self.ui.lblStatus.setText(self.mainStrs[self.lang][self.status])
        self.ui.lblProgress.setText
        
        # Background worker
        self.worker = pdfizerWorker(self.files)
        self.worker.sigProgress.connect(self.onWorkerProgres)
        self.worker.sigFile.connect(self.onSigFileReceived)
        self.worker.successSig.connect(self.onSuccessSig)
        self.worker.start()

    def onWorkerProgres(self, sig):
        self.ui.lblProgress.setText(sig)
        arr = sig.split("/")
        if len(arr) == 2:
            self.progressArr = arr
        else:
            self.progressArr = ["0", "0"]
        self.ui.progressBar.setMaximum(int(self.progressArr[1]))
        self.ui.progressBar.setValue(int(self.progressArr[0]))
    
    def onSigFileReceived(self, sig):
        if len(sig) <= MAX_LEN_STR:
            pass
        else:
            txtArr = sig.split(".")
            fileExtension = "." + txtArr[-1]
            extensionLen = len(fileExtension)
            sig = sig[:(MAX_LEN_STR - extensionLen - len("... "))] + "... " + fileExtension
        
        self.ui.lblFileName.setText(sig)
        self.showRamUsage()

        if DEBUG:
            print(f"ram usage: {self.process.memory_info()[0]/(1024**3)} GB")
        
    def onSuccessSig(self, sig):
        if sig == "writingToPdfFile":
            self.status = sig
            self.marqueePB()
        elif sig == "Success":
            self.infoMessage(title=self.msgBoxStrs[self.lang]["success"], text=self.msgBoxStrs[self.lang]["pdfCreatedSuccss"])
            self.status = "finished"
            self.fillPB()
            self.setControlBtnsEnabled(True)
        else:
            self.errorMessage(title=self.msgBoxStrs[self.lang]["errorOccured"], text=sig)
            self.status = "error"
            self.emptyPB()
            self.setControlBtnsEnabled(True)

        self.ui.lblStatus.setText(self.mainStrs[self.lang][self.status])
        self.ui.lblFileName.setText("")
        self.ui.lblProgress.setText("")


    ################################
    """Control progressbar"""
    ################################

    def emptyPB(self):
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(1)
        self.ui.progressBar.setValue(0)

    def fillPB(self):
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(1)
        self.ui.progressBar.setValue(1)

    def marqueePB(self):
        # Progressbar Marquee effect. See the link.
        # https://www.codetd.com/en/article/8287143
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(0)

    ################################
    """Unclassificied functions"""
    ################################

    def showRamUsage(self):
        self.ui.lblRamUsage.setText(f'{self.mainStrs[self.lang]["ramUsage"]} {round(self.process.memory_info()[0]/(1024**3), 2)} GB')

    def showFileCou(self):
        self.ui.lblProgress.setText(f"0/{len(self.files)}")
        self.emptyPB()

    def openOutputDir(self):
        try:
            # Detect the latest created file, see link below for more info
            # https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
            filesWithAbsPaths = sorted(Path(self.config["outputFolder"]).iterdir(), key=os.path.getctime, reverse=True)
            if DEBUG:
                for filename in filesWithAbsPaths:
                    print(filename)
            if len(filesWithAbsPaths):
                os.system(f"""start explorer.exe  /select, "{filesWithAbsPaths[0]}" """)
            else:
                os.system(f"""start explorer.exe  "{self.config["outputFolder"]}" """)
        except (Exception, ValueError, OSError, FileNotFoundError, IndexError) as err:
            self.errorMessage(title=self.msgBoxStrs[self.lang]["errorOccured"], text=str(err)) 

    def sanityCheckIODirs(self):
        # input
        if os.path.isdir(self.config["inputFolder"]):
            pass
        elif self.config["inputFolder"] == "./pdfize-Gui/input":
            self.config["inputFolder"] = directory + inputFolder
        else:
            self.errorMessage(title=self.msgBoxStrs[self.lang]["unableToaccessDefaultDir"], text=self.msgBoxStrs[self.lang]["usingFactoryDefaultDir"])
            self.config["inputFolder"] = directory + inputFolder
        
        # output
        if os.path.isdir(self.config["outputFolder"]):
            pass
        elif self.config["outputFolder"] == "./pdfize-Gui/output":
            self.config["outputFolder"] = directory + outputFolder
        else:
            self.errorMessage(title=self.msgBoxStrs[self.lang]["unableToaccessDefaultDir"], text=self.msgBoxStrs[self.lang]["usingFactoryDefaultDirOut"])
            self.config["outputFolder"] = directory + outputFolder      

    def setStatusbarLabelText(self):
        if  self.config["inputFolder"] == "selectedMultiFiles":
            self.statusLabel.setText("-> " + self.mainStrs[self.lang]["selectedMultiFiles"] + "   "
                            "-> " + self.msgBoxStrs[self.lang]["outputDir"] + self.config["outputFolder"]) 
        else:
            self.statusLabel.setText("-> " + self.msgBoxStrs[self.lang]["inputDir"] + self.config["inputFolder"] + "   "
                                    "-> " + self.msgBoxStrs[self.lang]["outputDir"] + self.config["outputFolder"]) 

        # Menu bar selection 
    def whoGotSelected(self, selection):
        txt = selection.text()
        if DEBUG:
            print(f"Selection from menubar: {txt}")
        
        if txt == "See online help":
            self.showHelpOnline(lang="EN")
        elif txt == "Çevrimiçi yardımı aç":
            self.showHelpOnline(lang="TR")
        elif txt == "See offline help":
            self.showHelpOffline(lang="EN")
        elif txt == "Çevrimdışı yardımı aç":
            self.showHelpOffline(lang="TR")
        elif txt == "App settings" or "Uygulama ayarları":
            self.setSettings()


    ################################
    """Help displayers"""
    ################################

    def showHelpOnline(self, lang="EN"):
        if lang == "TR":
            os.system('start https://github.com/Mehmet-Emre-Dogan/pdfize-Gui/blob/main/BEN%C4%B0OKU.md')
        else:
           os.system('start https://github.com/Mehmet-Emre-Dogan/pdfize-Gui/blob/main/README.md')

    def showHelpOffline(self, lang="EN"):
        try:
            if lang == "TR":
                os.system(f'start notepad.exe "{directory}\\benioku.txt"')
            else:
                os.system(f'start notepad.exe "{directory}\\readme.txt"')
        except (Exception, OSError, FileNotFoundError) as err:
            if lang == "TR":
                self.errorMessage(title="Çevrimdışı yardım görüntülenemiyor", text="'benioku.txt' dosyasını sildiniz mi?")
            else:
                self.errorMessage(title="Unable to show offline help", text="Did you deleted 'readme.txt' file?")


    ################################
    """Setting - configuration updaters"""
    ################################

    def setSettings(self):
        self.settingsWindow = mySettingsWindow()
        self.settingsWindow.show()
        self.settingsWindow.sigSettingsSaved.connect(self.initSettings2)

    def initSettings2(self):
        self.initSettings()
        self.setStatusbarLabelText()
        if hasattr(self, "configWindow"):
            self.configWindow.initSettings()
            self.configWindow.resizeWindow()
        self.ui.lblStatus.setText(self.mainStrs[self.lang][self.status])
        # self.settingsWindow.initSettings()

    def setConfig(self):
        self.configWindow = myConfigWindow()
        self.configWindow.show()
        self.configWindow.sigConfigSaved.connect(self.initConfig)
    
    def initConfig(self):
        self.config = loadConfig()
        self.config["inputFolder"] = self.settings["defaultInputFolder"]
        self.config["outputFolder"] = self.settings["defaultOutputFolder"]
        self.sanityCheckIODirs()
        dumpConfig(self.config)
        pdfizer.updateConfi()

    
def app():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    emrgMsg = emergencyMessage()
    try:
        win = myWindow()
        # app.aboutToQuit.connect(win.onAboutToQuit)
        try:
            win.show()
            sys.exit(app.exec_())
        except (Exception, ValueError, OSError, FileNotFoundError, IndexError) as err:
            win.errorMessage(title=win.msgBoxStrs[win.lang]["errorOccured"], text=str(err))
    except (Exception, ValueError, OSError, FileNotFoundError, IndexError) as err:
        emrgMsg.errorMessage(title="Very fatal error occured", text=str(err))


if __name__ == "__main__":
    app()