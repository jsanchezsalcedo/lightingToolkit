import maya.cmds as cmds
from PySide2 import QtCore
from PySide2 import QtWidgets
from maya import OpenMayaUI as omui
import shiboken2 as shi
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from lighting_tools_maya2018 import areaLightAttr

mainWindow = None
__title__ = 'Lighting Tool'
__version__ = '0.25'

def getMainWindow():
    ptr = omui.MQtUtil.mainWindow()
    mainWindow = shi.wrapInstance(long(ptr), QtWidgets.QMainWindow)
    return mainWindow

class lightType:
    AREA = 'Area Light'
    SKYDOME = 'Ai Sky Dome Light'
    DIRECTIONAL = 'Directional Light'
    POINT = 'Point Light'
    SPOT = 'Spot Light'

    @classmethod
    def getList(cls):
        return [cls.AREA, cls.SKYDOME, cls.DIRECTIONAL, cls.POINT, cls.SPOT]

class lightSource:
    KEY = 'key'
    FILL = 'fill'
    BOUNCE = 'bnc'
    SPEC = 'spc'
    VOL = 'vol'
    DOME = 'dome'

    @classmethod
    def getList(cls):
        return [cls.KEY, cls.FILL, cls.BOUNCE, cls.SPEC, cls.VOL, cls.DOME]

class lightDecay:
    NODECAY = 'No Decay'
    LINEAR = 'Linear'
    QUADRATIC = 'Quadratic'
    CUBIC = 'Cubic'

    @classmethod
    def getList(cls):
        return [cls.NODECAY, cls.LINEAR, cls.QUADRATIC, cls.CUBIC]

class lightFormat:
    MIRROR_BALL = 'Mirrored Ball'
    ANGULAR = 'Angular'
    LATLONG = 'Latlong'

    @classmethod
    def getList(cls):
        return [cls.MIRROR_BALL, cls.ANGULAR, cls.LATLONG]

class lightingTool(QtWidgets.QDialog):

    valueChanged = QtCore.Signal(float)

    def __init__(self, parent=None):
        super(lightingTool,self).__init__(parent)
        self.setWindowTitle('{} {}'.format(__title__,__version__))
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.createUI()

    def createUI(self):
        self.mainLayout = QtWidgets.QVBoxLayout()
        
        ### CREATE LIGHT BOX ###
        createLgtLyt = QtWidgets.QVBoxLayout()
        createLgtBox = QtWidgets.QGroupBox('Create Light')
        createLgtBox.setAlignment(QtCore.Qt.AlignTop)
        createLgtBoxLyt = QtWidgets.QVBoxLayout(createLgtBox)
        createLgtLyt.addWidget(createLgtBox)

        ### SOURCE LIGHT ###
        createSrcLyt = QtWidgets.QHBoxLayout()
        createSrcPrefix = QtWidgets.QLineEdit('group')
        createSrcPrefix.setFixedWidth(75)
        createSrcPrefix.setAlignment(QtCore.Qt.AlignLeft)
        createSrcLyt.addWidget(createSrcPrefix)
        createSrcCbx = QtWidgets.QComboBox()
        createSrcCbx.setFixedWidth(65)
        createSrcCbx.addItems(lightSource.getList())
        createSrcLyt.addWidget(createSrcCbx)
        createSrcSuffix = QtWidgets.QLineEdit('description')
        createSrcSuffix.setFixedWidth(150)
        createSrcSuffix.setAlignment(QtCore.Qt.AlignLeft)
        createSrcLyt.addWidget(createSrcSuffix)

        createLgtBoxLyt.addLayout(createSrcLyt)
        
        ### TYPE LIGHT ###
        createTypeLyt = QtWidgets.QHBoxLayout()
        createTypeLyt.setAlignment(QtCore.Qt.AlignLeft)
        createTypeLbl = QtWidgets.QLabel('Type')
        createTypeLbl.setFixedWidth(75)
        createTypeLbl.setAlignment(QtCore.Qt.AlignRight)
        createTypeLyt.addWidget(createTypeLbl)
        self.createTypeCbx = QtWidgets.QComboBox()
        self.createTypeCbx.setFixedWidth(160)
        self.createTypeCbx.addItems(lightType.getList())
        createTypeLyt.addWidget(self.createTypeCbx)
        createLgtBoxLyt.addLayout(createTypeLyt)

        ### ATTRIBUTES LAYOUT ###
        self.attrLgtLyt = QtWidgets.QStackedLayout()

        ### AREA LIGHT ATTR ###
        self.areaLgtAttr = areaLightUI()

        ### SKYDOME LIGHT ATTR ###
        self.domeLgtAttr = domeLightUI()

        ### DIRECTIONAL LIGHT ATTR ###
        self.directionalLgtAttr = directionalLightUI()

        ### POINT LIGHT ATTR ###
        self.pointLgtAttr = pointLightUI()

        ### SPOT LIGHT ATTR ###
        self.spotLgtAttr = spotLightUI()

        self.attrLgtLyt.addWidget(self.areaLgtAttr)
        self.attrLgtLyt.addWidget(self.domeLgtAttr)
        self.attrLgtLyt.addWidget(self.directionalLgtAttr)
        self.attrLgtLyt.addWidget(self.pointLgtAttr)
        self.attrLgtLyt.addWidget(self.spotLgtAttr)

        self.createTypeCbx.activated[str].connect(self.selectUI)

        self.mainLayout.addLayout(createLgtLyt)
        self.mainLayout.addLayout(self.attrLgtLyt)

        self.setLayout(self.mainLayout)
        
    def selectUI(self):
        getLyt = self.createTypeCbx.currentIndex()
        self.attrLgtLyt.setCurrentIndex(getLyt)

class areaLightUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(areaLightUI,self).__init__(parent)
        self.areaAttrUI()

    def areaAttrUI(self):
        self.areaAttrLyt = QtWidgets.QVBoxLayout(self)
        self.areaAttrLyt.setContentsMargins(0,0,0,0)

        self.areaAttrBox = QtWidgets.QGroupBox('Area Light Attributes')
        self.areaAttrLyt.addWidget(self.areaAttrBox)
        self.areaCommonLyt = QtWidgets.QVBoxLayout(self.areaAttrBox)

        self.areaAttrBoxLyt = QtWidgets.QGridLayout()
        self.areaCommonLyt.addLayout(self.areaAttrBoxLyt)

        self.areaClrLbl = QtWidgets.QLabel('Color')
        self.areaClrLbl.setFixedWidth(90)
        self.areaClrLbl.setAlignment(QtCore.Qt.AlignRight)
        self.areaAttrBoxLyt.addWidget(self.areaClrLbl, 0, 0)

        self.areaClrBtn = QtWidgets.QPushButton()
        self.areaClrBtn.setFixedSize(74,15)
        self.areaClrBtn.setStyleSheet('background-color: rgb(255,255,255)')
        self.areaAttrBoxLyt.addWidget(self.areaClrBtn,0,1)

        self.areaClrSld = QtWidgets.QSlider()
        self.areaClrSld.setOrientation(QtCore.Qt.Horizontal)
        self.areaAttrBoxLyt.addWidget(self.areaClrSld,0,2)

        self.areaIntLbl = QtWidgets.QLabel('Intensity')
        self.areaIntLbl.setFixedWidth(90)
        self.areaIntLbl.setAlignment(QtCore.Qt.AlignRight)
        self.areaAttrBoxLyt.addWidget(self.areaIntLbl, 1, 0)

        self.areaIntLed = QtWidgets.QLineEdit()
        self.areaIntLed.setFixedWidth(75)
        self.areaAttrBoxLyt.addWidget(self.areaIntLed, 1, 1)

        self.areaIntSld = QtWidgets.QSlider()
        self.areaIntSld.setOrientation(QtCore.Qt.Horizontal)
        self.areaIntSld.setRange(0, 1000)
        self.areaAttrBoxLyt.addWidget(self.areaIntSld, 1, 2)

        self.areaDecayLyt = QtWidgets.QFormLayout()
        self.areaCommonLyt.addLayout(self.areaDecayLyt)

        self.areaDecayLbl = QtWidgets.QLabel('Decay Rate')
        self.areaDecayLbl.setAlignment(QtCore.Qt.AlignRight)
        self.areaDecayLbl.setFixedWidth(90)

        self.areaDecayCbx = QtWidgets.QComboBox()
        self.areaDecayCbx.setFixedWidth(95)
        self.areaDecayCbx.addItems(lightDecay.getList())
        self.areaDecayLyt.addRow(self.areaDecayLbl, self.areaDecayCbx)

        self.areaAiBox = QtWidgets.QGroupBox('Arnold')
        self.areaAttrLyt.addWidget(self.areaAiBox)
        self.areaAiLyt = QtWidgets.QVBoxLayout(self.areaAiBox)

        self.areaAiTempLyt = QtWidgets.QGridLayout()
        self.areaAiLyt.addLayout(self.areaAiTempLyt)

        self.areaNullLbl = QtWidgets.QLabel('')
        self.areaNullLbl.setFixedWidth(90)
        self.areaAiTempLyt.addWidget(self.areaNullLbl, 0, 0)
        self.areaTempChk = QtWidgets.QCheckBox('Use Color Temperature')
        self.areaAiTempLyt.addWidget(self.areaTempChk, 0, 1)

        self.areaAiBoxLyt = QtWidgets.QGridLayout()
        self.areaAiLyt.addLayout(self.areaAiBoxLyt)

        self.areaTempLbl = QtWidgets.QLabel('Temperature')
        self.areaTempLbl.setFixedWidth(90)
        self.areaTempLbl.setAlignment(QtCore.Qt.AlignRight)
        self.areaAiBoxLyt.addWidget(self.areaTempLbl, 1, 0)

        self.areaTempLed = QtWidgets.QLineEdit()
        self.areaTempLed.setFixedWidth(75)
        self.areaTempValidator = QtGui.QDoubleValidator()
        self.areaTempValidator.setDecimals(3)
        self.areaTempLed.setValidator(self.areaTempValidator)
        self.areaAiBoxLyt.addWidget(self.areaTempLed, 1, 1)

        self.areaTempSld = QtWidgets.QSlider()
        self.areaTempSld.setOrientation(QtCore.Qt.Horizontal)
        self.areaTempSld.setRange(0, 1000)
        self.areaAiBoxLyt.addWidget(self.areaTempSld, 1, 2)

        #        line = QtWidgets.QFrame()
        #        areaAiBoxLyt.addWidget(line,2,0)

        self.areaExpLbl = QtWidgets.QLabel('Exposure')
        self.areaExpLbl.setFixedWidth(90)
        self.areaExpLbl.setAlignment(QtCore.Qt.AlignRight)
        self.areaAiBoxLyt.addWidget(self.areaExpLbl, 3, 0)

        self.areaExpLed = QtWidgets.QLineEdit()
        self.areaExpLed.setFixedWidth(75)
        self.areaExpValidator = QtGui.QDoubleValidator()
        self.areaExpValidator.setDecimals(3)
        self.areaExpLed.setValidator(self.areaExpValidator)
        self.areaAiBoxLyt.addWidget(self.areaExpLed, 3, 1)

        self.areaExpSld = QtWidgets.QSlider()
        self.areaExpSld.setOrientation(QtCore.Qt.Horizontal)
        self.areaExpSld.setRange(0, 1000)
        self.areaAiBoxLyt.addWidget(self.areaExpSld, 3, 2)

        self.areaSmpLbl = QtWidgets.QLabel('Samples')
        self.areaSmpLbl.setFixedWidth(90)
        self.areaSmpLbl.setAlignment(QtCore.Qt.AlignRight)
        self.areaAiBoxLyt.addWidget(self.areaSmpLbl, 4, 0)

        self.areaSmpLed = QtWidgets.QLineEdit()
        self.areaSmpLed.setFixedWidth(75)
        self.areaSmpValidator = QtGui.QDoubleValidator()
        self.areaSmpValidator.setDecimals(3)
        self.areaSmpLed.setValidator(self.areaSmpValidator)
        self.areaAiBoxLyt.addWidget(self.areaSmpLed, 4, 1)

        self.areaSmpSld = QtWidgets.QSlider()
        self.areaSmpSld.setOrientation(QtCore.Qt.Horizontal)
        self.areaSmpSld.setRange(0, 1000)
        self.areaAiBoxLyt.addWidget(self.areaSmpSld, 4, 2)

        self.areaSprLbl = QtWidgets.QLabel('Spread')
        self.areaSprLbl.setFixedWidth(90)
        self.areaSprLbl.setAlignment(QtCore.Qt.AlignRight)
        self.areaAiBoxLyt.addWidget(self.areaSprLbl, 5, 0)

        self.areaSprLed = QtWidgets.QLineEdit()
        self.areaSprLed.setFixedWidth(75)
        self.areaSprValidator = QtGui.QDoubleValidator()
        self.areaSprValidator.setDecimals(3)
        self.areaSprLed.setValidator(self.areaSprValidator)
        self.areaAiBoxLyt.addWidget(self.areaSprLed, 5, 1)

        self.areaSprSld = QtWidgets.QSlider()
        self.areaSprSld.setOrientation(QtCore.Qt.Horizontal)
        self.areaSprSld.setRange(0, 1000)
        self.areaAiBoxLyt.addWidget(self.areaSprSld, 5, 2)

        self.areaBncLbl = QtWidgets.QLabel('Bounces')
        self.areaBncLbl.setFixedWidth(90)
        self.areaBncLbl.setAlignment(QtCore.Qt.AlignRight)
        self.areaAiBoxLyt.addWidget(self.areaBncLbl, 6, 0)

        self.areaBncLed = QtWidgets.QLineEdit()
        self.areaBncLed.setFixedWidth(75)
        self.areaAiBoxLyt.addWidget(self.areaBncLed, 6, 1)

        self.areaLgLyt = QtWidgets.QGridLayout()
        self.areaAiLyt.addLayout(self.areaLgLyt)

        self.areaLgLbl = QtWidgets.QLabel('AOV Light Group')
        self.areaLgLbl.setFixedWidth(90)
        self.areaLgLbl.setAlignment(QtCore.Qt.AlignRight)
        self.areaLgLyt.addWidget(self.areaLgLbl, 0, 0)
        self.areaLgLed = QtWidgets.QLineEdit('RGBA_')
        self.areaLgLyt.addWidget(self.areaLgLed, 0, 1)

class domeLightUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(domeLightUI,self).__init__(parent)
        self.domeAttrUI()

    def domeAttrUI(self):
        self.domeAttrLyt = QtWidgets.QVBoxLayout(self)
        self.domeAttrLyt.setContentsMargins(0,0,0,0)

        self.domeAttrBox = QtWidgets.QGroupBox('Ai Sky Dome Light Attributes')
        self.domeAttrLyt.addWidget(self.domeAttrBox)
        self.domeCommonLyt = QtWidgets.QVBoxLayout(self.domeAttrBox)

        self.domeAttrBoxLyt = QtWidgets.QGridLayout()
        self.domeCommonLyt.addLayout(self.domeAttrBoxLyt)

        self.domeClrLbl = QtWidgets.QLabel('Color')
        self.domeClrLbl.setFixedWidth(90)
        self.domeClrLbl.setAlignment(QtCore.Qt.AlignRight)
        self.domeAttrBoxLyt.addWidget(self.domeClrLbl, 0, 0)

        self.domeClrBtn = QtWidgets.QPushButton()
        self.domeClrBtn.setFixedSize(74,15)
        self.domeClrBtn.setStyleSheet('background-color: rgb(255,255,255)')
        self.domeAttrBoxLyt.addWidget(self.domeClrBtn,0,1)

        self.domeClrSld = QtWidgets.QSlider()
        self.domeClrSld.setOrientation(QtCore.Qt.Horizontal)
        self.domeAttrBoxLyt.addWidget(self.domeClrSld,0,2)

        self.domeIntLbl = QtWidgets.QLabel('Intensity')
        self.domeIntLbl.setFixedWidth(90)
        self.domeIntLbl.setAlignment(QtCore.Qt.AlignRight)
        self.domeAttrBoxLyt.addWidget(self.domeIntLbl, 1, 0)

        self.domeIntLed = QtWidgets.QLineEdit()
        self.domeIntLed.setFixedWidth(75)
        self.domeAttrBoxLyt.addWidget(self.domeIntLed, 1, 1)

        self.domeIntSld = QtWidgets.QSlider()
        self.domeIntSld.setOrientation(QtCore.Qt.Horizontal)
        self.domeIntSld.setRange(0, 1000)
        self.domeAttrBoxLyt.addWidget(self.domeIntSld, 1, 2)

        self.domeIntLbl = QtWidgets.QLabel('Resolution')
        self.domeIntLbl.setFixedWidth(90)
        self.domeIntLbl.setAlignment(QtCore.Qt.AlignRight)
        self.domeAttrBoxLyt.addWidget(self.domeIntLbl, 2, 0)

        self.domeIntLed = QtWidgets.QLineEdit()
        self.domeIntLed.setFixedWidth(75)
        self.domeAttrBoxLyt.addWidget(self.domeIntLed, 2, 1)

        self.domeFormatLyt = QtWidgets.QFormLayout()
        self.domeFormatLyt.setContentsMargins(0,0,0,0)
        self.domeCommonLyt.addLayout(self.domeFormatLyt)

        self.domeFormatLbl = QtWidgets.QLabel('Format')
        self.domeFormatLbl.setAlignment(QtCore.Qt.AlignRight)
        self.domeFormatLbl.setFixedWidth(90)

        self.domeFormatCbx = QtWidgets.QComboBox()
        self.domeFormatCbx.setFixedWidth(95)
        self.domeFormatCbx.addItems(lightFormat.getList())
        self.domeFormatLyt.addRow(self.domeFormatLbl, self.domeFormatCbx)

        self.domeAiBox = QtWidgets.QGroupBox()
        self.domeAiBox.setContentsMargins(0,0,0,0)
        self.domeAttrLyt.addWidget(self.domeAiBox)
        self.domeAiLyt = QtWidgets.QVBoxLayout(self.domeAiBox)

        self.domeAiTempLyt = QtWidgets.QGridLayout()
        self.domeAiLyt.addLayout(self.domeAiTempLyt)

        self.domeNullLbl = QtWidgets.QLabel('')
        self.domeNullLbl.setFixedWidth(90)
        self.domeAiTempLyt.addWidget(self.domeNullLbl, 0, 0)
        self.domeTempChk = QtWidgets.QCheckBox('Use Color Temperature')
        self.domeAiTempLyt.addWidget(self.domeTempChk, 0, 1)

        self.domeAiBoxLyt = QtWidgets.QGridLayout()
        self.domeAiLyt.addLayout(self.domeAiBoxLyt)

        self.domeTempLbl = QtWidgets.QLabel('Temperature')
        self.domeTempLbl.setFixedWidth(90)
        self.domeTempLbl.setAlignment(QtCore.Qt.AlignRight)
        self.domeAiBoxLyt.addWidget(self.domeTempLbl, 1, 0)

        self.domeTempLed = QtWidgets.QLineEdit()
        self.domeTempLed.setFixedWidth(75)
        self.domeTempValidator = QtGui.QDoubleValidator()
        self.domeTempValidator.setDecimals(3)
        self.domeTempLed.setValidator(self.domeTempValidator)
        self.domeAiBoxLyt.addWidget(self.domeTempLed, 1, 1)

        self.domeTempSld = QtWidgets.QSlider()
        self.domeTempSld.setOrientation(QtCore.Qt.Horizontal)
        self.domeTempSld.setRange(0, 1000)
        self.domeAiBoxLyt.addWidget(self.domeTempSld, 1, 2)

        #        line = QtWidgets.QFrame()
        #        domeAiBoxLyt.addWidget(line,2,0)

        self.domeExpLbl = QtWidgets.QLabel('Exposure')
        self.domeExpLbl.setFixedWidth(90)
        self.domeExpLbl.setAlignment(QtCore.Qt.AlignRight)
        self.domeAiBoxLyt.addWidget(self.domeExpLbl, 3, 0)

        self.domeExpLed = QtWidgets.QLineEdit()
        self.domeExpLed.setFixedWidth(75)
        self.domeExpValidator = QtGui.QDoubleValidator()
        self.domeExpValidator.setDecimals(3)
        self.domeExpLed.setValidator(self.domeExpValidator)
        self.domeAiBoxLyt.addWidget(self.domeExpLed, 3, 1)

        self.domeExpSld = QtWidgets.QSlider()
        self.domeExpSld.setOrientation(QtCore.Qt.Horizontal)
        self.domeExpSld.setRange(0, 1000)
        self.domeAiBoxLyt.addWidget(self.domeExpSld, 3, 2)

        self.domeSmpLbl = QtWidgets.QLabel('Samples')
        self.domeSmpLbl.setFixedWidth(90)
        self.domeSmpLbl.setAlignment(QtCore.Qt.AlignRight)
        self.domeAiBoxLyt.addWidget(self.domeSmpLbl, 4, 0)

        self.domeSmpLed = QtWidgets.QLineEdit()
        self.domeSmpLed.setFixedWidth(75)
        self.domeSmpValidator = QtGui.QDoubleValidator()
        self.domeSmpValidator.setDecimals(3)
        self.domeSmpLed.setValidator(self.domeSmpValidator)
        self.domeAiBoxLyt.addWidget(self.domeSmpLed, 4, 1)

        self.domeSmpSld = QtWidgets.QSlider()
        self.domeSmpSld.setOrientation(QtCore.Qt.Horizontal)
        self.domeSmpSld.setRange(0, 1000)
        self.domeAiBoxLyt.addWidget(self.domeSmpSld, 4, 2)

        self.domeBncLbl = QtWidgets.QLabel('Bounces')
        self.domeBncLbl.setFixedWidth(90)
        self.domeBncLbl.setAlignment(QtCore.Qt.AlignRight)
        self.domeAiBoxLyt.addWidget(self.domeBncLbl, 5, 0)

        self.domeBncLed = QtWidgets.QLineEdit()
        self.domeBncLed.setFixedWidth(75)
        self.domeAiBoxLyt.addWidget(self.domeBncLed, 5, 1)

        self.domeLgLyt = QtWidgets.QGridLayout()
        self.domeAiLyt.addLayout(self.domeLgLyt)

        self.domeLgLbl = QtWidgets.QLabel('AOV Light Group')
        self.domeLgLbl.setFixedWidth(90)
        self.domeLgLbl.setAlignment(QtCore.Qt.AlignRight)
        self.domeLgLyt.addWidget(self.domeLgLbl, 0, 0)
        self.domeLgLed = QtWidgets.QLineEdit('RGBA_')
        self.domeLgLyt.addWidget(self.domeLgLed, 0, 1)

class directionalLightUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(directionalLightUI,self).__init__(parent)
        self.directionalAttrUI()

    def directionalAttrUI(self):
        self.directionalAttrLyt = QtWidgets.QVBoxLayout(self)
        self.directionalAttrLyt.setContentsMargins(0,0,0,0)

        self.directionalAttrBox = QtWidgets.QGroupBox('directional Light Attributes')
        self.directionalAttrLyt.addWidget(self.directionalAttrBox)
        self.directionalCommonLyt = QtWidgets.QVBoxLayout(self.directionalAttrBox)

        self.directionalAttrBoxLyt = QtWidgets.QGridLayout()
        self.directionalCommonLyt.addLayout(self.directionalAttrBoxLyt)

        self.directionalClrLbl = QtWidgets.QLabel('Color')
        self.directionalClrLbl.setFixedWidth(90)
        self.directionalClrLbl.setAlignment(QtCore.Qt.AlignRight)
        self.directionalAttrBoxLyt.addWidget(self.directionalClrLbl, 0, 0)

        self.directionalClrBtn = QtWidgets.QPushButton()
        self.directionalClrBtn.setFixedSize(74,15)
        self.directionalClrBtn.setStyleSheet('background-color: rgb(255,255,255)')
        self.directionalAttrBoxLyt.addWidget(self.directionalClrBtn,0,1)

        self.directionalClrSld = QtWidgets.QSlider()
        self.directionalClrSld.setOrientation(QtCore.Qt.Horizontal)
        self.directionalAttrBoxLyt.addWidget(self.directionalClrSld,0,2)

        self.directionalIntLbl = QtWidgets.QLabel('Intensity')
        self.directionalIntLbl.setFixedWidth(90)
        self.directionalIntLbl.setAlignment(QtCore.Qt.AlignRight)
        self.directionalAttrBoxLyt.addWidget(self.directionalIntLbl, 1, 0)

        self.directionalIntLed = QtWidgets.QLineEdit()
        self.directionalIntLed.setFixedWidth(75)
        self.directionalAttrBoxLyt.addWidget(self.directionalIntLed, 1, 1)

        self.directionalIntSld = QtWidgets.QSlider()
        self.directionalIntSld.setOrientation(QtCore.Qt.Horizontal)
        self.directionalIntSld.setRange(0, 1000)
        self.directionalAttrBoxLyt.addWidget(self.directionalIntSld, 1, 2)

        self.directionalDecayLyt = QtWidgets.QFormLayout()
        self.directionalCommonLyt.addLayout(self.directionalDecayLyt)

        self.directionalDecayLbl = QtWidgets.QLabel('Decay Rate')
        self.directionalDecayLbl.setAlignment(QtCore.Qt.AlignRight)
        self.directionalDecayLbl.setFixedWidth(90)

        self.directionalDecayCbx = QtWidgets.QComboBox()
        self.directionalDecayCbx.setFixedWidth(95)
        self.directionalDecayCbx.addItems(lightDecay.getList())
        self.directionalDecayLyt.addRow(self.directionalDecayLbl, self.directionalDecayCbx)

        self.directionalAiBox = QtWidgets.QGroupBox('Arnold')
        self.directionalAttrLyt.addWidget(self.directionalAiBox)
        self.directionalAiLyt = QtWidgets.QVBoxLayout(self.directionalAiBox)

        self.directionalAiTempLyt = QtWidgets.QGridLayout()
        self.directionalAiLyt.addLayout(self.directionalAiTempLyt)

        self.directionalNullLbl = QtWidgets.QLabel('')
        self.directionalNullLbl.setFixedWidth(90)
        self.directionalAiTempLyt.addWidget(self.directionalNullLbl, 0, 0)
        self.directionalTempChk = QtWidgets.QCheckBox('Use Color Temperature')
        self.directionalAiTempLyt.addWidget(self.directionalTempChk, 0, 1)

        self.directionalAiBoxLyt = QtWidgets.QGridLayout()
        self.directionalAiLyt.addLayout(self.directionalAiBoxLyt)

        self.directionalTempLbl = QtWidgets.QLabel('Temperature')
        self.directionalTempLbl.setFixedWidth(90)
        self.directionalTempLbl.setAlignment(QtCore.Qt.AlignRight)
        self.directionalAiBoxLyt.addWidget(self.directionalTempLbl, 1, 0)

        self.directionalTempLed = QtWidgets.QLineEdit()
        self.directionalTempLed.setFixedWidth(75)
        self.directionalTempValidator = QtGui.QDoubleValidator()
        self.directionalTempValidator.setDecimals(3)
        self.directionalTempLed.setValidator(self.directionalTempValidator)
        self.directionalAiBoxLyt.addWidget(self.directionalTempLed, 1, 1)

        self.directionalTempSld = QtWidgets.QSlider()
        self.directionalTempSld.setOrientation(QtCore.Qt.Horizontal)
        self.directionalTempSld.setRange(0, 1000)
        self.directionalAiBoxLyt.addWidget(self.directionalTempSld, 1, 2)

        #        line = QtWidgets.QFrame()
        #        directionalAiBoxLyt.addWidget(line,2,0)

        self.directionalExpLbl = QtWidgets.QLabel('Exposure')
        self.directionalExpLbl.setFixedWidth(90)
        self.directionalExpLbl.setAlignment(QtCore.Qt.AlignRight)
        self.directionalAiBoxLyt.addWidget(self.directionalExpLbl, 3, 0)

        self.directionalExpLed = QtWidgets.QLineEdit()
        self.directionalExpLed.setFixedWidth(75)
        self.directionalExpValidator = QtGui.QDoubleValidator()
        self.directionalExpValidator.setDecimals(3)
        self.directionalExpLed.setValidator(self.directionalExpValidator)
        self.directionalAiBoxLyt.addWidget(self.directionalExpLed, 3, 1)

        self.directionalExpSld = QtWidgets.QSlider()
        self.directionalExpSld.setOrientation(QtCore.Qt.Horizontal)
        self.directionalExpSld.setRange(0, 1000)
        self.directionalAiBoxLyt.addWidget(self.directionalExpSld, 3, 2)

        self.directionalSmpLbl = QtWidgets.QLabel('Samples')
        self.directionalSmpLbl.setFixedWidth(90)
        self.directionalSmpLbl.setAlignment(QtCore.Qt.AlignRight)
        self.directionalAiBoxLyt.addWidget(self.directionalSmpLbl, 4, 0)

        self.directionalSmpLed = QtWidgets.QLineEdit()
        self.directionalSmpLed.setFixedWidth(75)
        self.directionalSmpValidator = QtGui.QDoubleValidator()
        self.directionalSmpValidator.setDecimals(3)
        self.directionalSmpLed.setValidator(self.directionalSmpValidator)
        self.directionalAiBoxLyt.addWidget(self.directionalSmpLed, 4, 1)

        self.directionalSmpSld = QtWidgets.QSlider()
        self.directionalSmpSld.setOrientation(QtCore.Qt.Horizontal)
        self.directionalSmpSld.setRange(0, 1000)
        self.directionalAiBoxLyt.addWidget(self.directionalSmpSld, 4, 2)

        self.directionalSprLbl = QtWidgets.QLabel('Spread')
        self.directionalSprLbl.setFixedWidth(90)
        self.directionalSprLbl.setAlignment(QtCore.Qt.AlignRight)
        self.directionalAiBoxLyt.addWidget(self.directionalSprLbl, 5, 0)

        self.directionalSprLed = QtWidgets.QLineEdit()
        self.directionalSprLed.setFixedWidth(75)
        self.directionalSprValidator = QtGui.QDoubleValidator()
        self.directionalSprValidator.setDecimals(3)
        self.directionalSprLed.setValidator(self.directionalSprValidator)
        self.directionalAiBoxLyt.addWidget(self.directionalSprLed, 5, 1)

        self.directionalSprSld = QtWidgets.QSlider()
        self.directionalSprSld.setOrientation(QtCore.Qt.Horizontal)
        self.directionalSprSld.setRange(0, 1000)
        self.directionalAiBoxLyt.addWidget(self.directionalSprSld, 5, 2)

        self.directionalBncLbl = QtWidgets.QLabel('Bounces')
        self.directionalBncLbl.setFixedWidth(90)
        self.directionalBncLbl.setAlignment(QtCore.Qt.AlignRight)
        self.directionalAiBoxLyt.addWidget(self.directionalBncLbl, 6, 0)

        self.directionalBncLed = QtWidgets.QLineEdit()
        self.directionalBncLed.setFixedWidth(75)
        self.directionalAiBoxLyt.addWidget(self.directionalBncLed, 6, 1)

        self.directionalLgLyt = QtWidgets.QGridLayout()
        self.directionalAiLyt.addLayout(self.directionalLgLyt)

        self.directionalLgLbl = QtWidgets.QLabel('AOV Light Group')
        self.directionalLgLbl.setFixedWidth(90)
        self.directionalLgLbl.setAlignment(QtCore.Qt.AlignRight)
        self.directionalLgLyt.addWidget(self.directionalLgLbl, 0, 0)
        self.directionalLgLed = QtWidgets.QLineEdit('RGBA_')
        self.directionalLgLyt.addWidget(self.directionalLgLed, 0, 1)

class pointLightUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(pointLightUI,self).__init__(parent)
        self.pointAttrUI()

    def pointAttrUI(self):
        self.pointAttrLyt = QtWidgets.QVBoxLayout(self)
        self.pointAttrLyt.setContentsMargins(0,0,0,0)

        self.pointAttrBox = QtWidgets.QGroupBox('point Light Attributes')
        self.pointAttrLyt.addWidget(self.pointAttrBox)
        self.pointCommonLyt = QtWidgets.QVBoxLayout(self.pointAttrBox)

        self.pointAttrBoxLyt = QtWidgets.QGridLayout()
        self.pointCommonLyt.addLayout(self.pointAttrBoxLyt)

        self.pointClrLbl = QtWidgets.QLabel('Color')
        self.pointClrLbl.setFixedWidth(90)
        self.pointClrLbl.setAlignment(QtCore.Qt.AlignRight)
        self.pointAttrBoxLyt.addWidget(self.pointClrLbl, 0, 0)

        self.pointClrBtn = QtWidgets.QPushButton()
        self.pointClrBtn.setFixedSize(74,15)
        self.pointClrBtn.setStyleSheet('background-color: rgb(255,255,255)')
        self.pointAttrBoxLyt.addWidget(self.pointClrBtn,0,1)

        self.pointClrSld = QtWidgets.QSlider()
        self.pointClrSld.setOrientation(QtCore.Qt.Horizontal)
        self.pointAttrBoxLyt.addWidget(self.pointClrSld,0,2)

        self.pointIntLbl = QtWidgets.QLabel('Intensity')
        self.pointIntLbl.setFixedWidth(90)
        self.pointIntLbl.setAlignment(QtCore.Qt.AlignRight)
        self.pointAttrBoxLyt.addWidget(self.pointIntLbl, 1, 0)

        self.pointIntLed = QtWidgets.QLineEdit()
        self.pointIntLed.setFixedWidth(75)
        self.pointAttrBoxLyt.addWidget(self.pointIntLed, 1, 1)

        self.pointIntSld = QtWidgets.QSlider()
        self.pointIntSld.setOrientation(QtCore.Qt.Horizontal)
        self.pointIntSld.setRange(0, 1000)
        self.pointAttrBoxLyt.addWidget(self.pointIntSld, 1, 2)

        self.pointDecayLyt = QtWidgets.QFormLayout()
        self.pointCommonLyt.addLayout(self.pointDecayLyt)

        self.pointDecayLbl = QtWidgets.QLabel('Decay Rate')
        self.pointDecayLbl.setAlignment(QtCore.Qt.AlignRight)
        self.pointDecayLbl.setFixedWidth(90)

        self.pointDecayCbx = QtWidgets.QComboBox()
        self.pointDecayCbx.setFixedWidth(95)
        self.pointDecayCbx.addItems(lightDecay.getList())
        self.pointDecayLyt.addRow(self.pointDecayLbl, self.pointDecayCbx)

        self.pointAiBox = QtWidgets.QGroupBox('Arnold')
        self.pointAttrLyt.addWidget(self.pointAiBox)
        self.pointAiLyt = QtWidgets.QVBoxLayout(self.pointAiBox)

        self.pointAiTempLyt = QtWidgets.QGridLayout()
        self.pointAiLyt.addLayout(self.pointAiTempLyt)

        self.pointNullLbl = QtWidgets.QLabel('')
        self.pointNullLbl.setFixedWidth(90)
        self.pointAiTempLyt.addWidget(self.pointNullLbl, 0, 0)
        self.pointTempChk = QtWidgets.QCheckBox('Use Color Temperature')
        self.pointAiTempLyt.addWidget(self.pointTempChk, 0, 1)

        self.pointAiBoxLyt = QtWidgets.QGridLayout()
        self.pointAiLyt.addLayout(self.pointAiBoxLyt)

        self.pointTempLbl = QtWidgets.QLabel('Temperature')
        self.pointTempLbl.setFixedWidth(90)
        self.pointTempLbl.setAlignment(QtCore.Qt.AlignRight)
        self.pointAiBoxLyt.addWidget(self.pointTempLbl, 1, 0)

        self.pointTempLed = QtWidgets.QLineEdit()
        self.pointTempLed.setFixedWidth(75)
        self.pointTempValidator = QtGui.QDoubleValidator()
        self.pointTempValidator.setDecimals(3)
        self.pointTempLed.setValidator(self.pointTempValidator)
        self.pointAiBoxLyt.addWidget(self.pointTempLed, 1, 1)

        self.pointTempSld = QtWidgets.QSlider()
        self.pointTempSld.setOrientation(QtCore.Qt.Horizontal)
        self.pointTempSld.setRange(0, 1000)
        self.pointAiBoxLyt.addWidget(self.pointTempSld, 1, 2)

        #        line = QtWidgets.QFrame()
        #        pointAiBoxLyt.addWidget(line,2,0)

        self.pointExpLbl = QtWidgets.QLabel('Exposure')
        self.pointExpLbl.setFixedWidth(90)
        self.pointExpLbl.setAlignment(QtCore.Qt.AlignRight)
        self.pointAiBoxLyt.addWidget(self.pointExpLbl, 3, 0)

        self.pointExpLed = QtWidgets.QLineEdit()
        self.pointExpLed.setFixedWidth(75)
        self.pointExpValidator = QtGui.QDoubleValidator()
        self.pointExpValidator.setDecimals(3)
        self.pointExpLed.setValidator(self.pointExpValidator)
        self.pointAiBoxLyt.addWidget(self.pointExpLed, 3, 1)

        self.pointExpSld = QtWidgets.QSlider()
        self.pointExpSld.setOrientation(QtCore.Qt.Horizontal)
        self.pointExpSld.setRange(0, 1000)
        self.pointAiBoxLyt.addWidget(self.pointExpSld, 3, 2)

        self.pointSmpLbl = QtWidgets.QLabel('Samples')
        self.pointSmpLbl.setFixedWidth(90)
        self.pointSmpLbl.setAlignment(QtCore.Qt.AlignRight)
        self.pointAiBoxLyt.addWidget(self.pointSmpLbl, 4, 0)

        self.pointSmpLed = QtWidgets.QLineEdit()
        self.pointSmpLed.setFixedWidth(75)
        self.pointSmpValidator = QtGui.QDoubleValidator()
        self.pointSmpValidator.setDecimals(3)
        self.pointSmpLed.setValidator(self.pointSmpValidator)
        self.pointAiBoxLyt.addWidget(self.pointSmpLed, 4, 1)

        self.pointSmpSld = QtWidgets.QSlider()
        self.pointSmpSld.setOrientation(QtCore.Qt.Horizontal)
        self.pointSmpSld.setRange(0, 1000)
        self.pointAiBoxLyt.addWidget(self.pointSmpSld, 4, 2)

        self.pointSprLbl = QtWidgets.QLabel('Spread')
        self.pointSprLbl.setFixedWidth(90)
        self.pointSprLbl.setAlignment(QtCore.Qt.AlignRight)
        self.pointAiBoxLyt.addWidget(self.pointSprLbl, 5, 0)

        self.pointSprLed = QtWidgets.QLineEdit()
        self.pointSprLed.setFixedWidth(75)
        self.pointSprValidator = QtGui.QDoubleValidator()
        self.pointSprValidator.setDecimals(3)
        self.pointSprLed.setValidator(self.pointSprValidator)
        self.pointAiBoxLyt.addWidget(self.pointSprLed, 5, 1)

        self.pointSprSld = QtWidgets.QSlider()
        self.pointSprSld.setOrientation(QtCore.Qt.Horizontal)
        self.pointSprSld.setRange(0, 1000)
        self.pointAiBoxLyt.addWidget(self.pointSprSld, 5, 2)

        self.pointBncLbl = QtWidgets.QLabel('Bounces')
        self.pointBncLbl.setFixedWidth(90)
        self.pointBncLbl.setAlignment(QtCore.Qt.AlignRight)
        self.pointAiBoxLyt.addWidget(self.pointBncLbl, 6, 0)

        self.pointBncLed = QtWidgets.QLineEdit()
        self.pointBncLed.setFixedWidth(75)
        self.pointAiBoxLyt.addWidget(self.pointBncLed, 6, 1)

        self.pointLgLyt = QtWidgets.QGridLayout()
        self.pointAiLyt.addLayout(self.pointLgLyt)

        self.pointLgLbl = QtWidgets.QLabel('AOV Light Group')
        self.pointLgLbl.setFixedWidth(90)
        self.pointLgLbl.setAlignment(QtCore.Qt.AlignRight)
        self.pointLgLyt.addWidget(self.pointLgLbl, 0, 0)
        self.pointLgLed = QtWidgets.QLineEdit('RGBA_')
        self.pointLgLyt.addWidget(self.pointLgLed, 0, 1)

class spotLightUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(spotLightUI,self).__init__(parent)
        self.spotAttrUI()

    def spotAttrUI(self):
        self.spotAttrLyt = QtWidgets.QVBoxLayout(self)
        self.spotAttrLyt.setContentsMargins(0,0,0,0)

        self.spotAttrBox = QtWidgets.QGroupBox('spot Light Attributes')
        self.spotAttrLyt.addWidget(self.spotAttrBox)
        self.spotCommonLyt = QtWidgets.QVBoxLayout(self.spotAttrBox)

        self.spotAttrBoxLyt = QtWidgets.QGridLayout()
        self.spotCommonLyt.addLayout(self.spotAttrBoxLyt)

        self.spotClrLbl = QtWidgets.QLabel('Color')
        self.spotClrLbl.setFixedWidth(90)
        self.spotClrLbl.setAlignment(QtCore.Qt.AlignRight)
        self.spotAttrBoxLyt.addWidget(self.spotClrLbl, 0, 0)

        self.spotClrBtn = QtWidgets.QPushButton()
        self.spotClrBtn.setFixedSize(74,15)
        self.spotClrBtn.setStyleSheet('background-color: rgb(255,255,255)')
        self.spotAttrBoxLyt.addWidget(self.spotClrBtn,0,1)

        self.spotClrSld = QtWidgets.QSlider()
        self.spotClrSld.setOrientation(QtCore.Qt.Horizontal)
        self.spotAttrBoxLyt.addWidget(self.spotClrSld,0,2)

        self.spotIntLbl = QtWidgets.QLabel('Intensity')
        self.spotIntLbl.setFixedWidth(90)
        self.spotIntLbl.setAlignment(QtCore.Qt.AlignRight)
        self.spotAttrBoxLyt.addWidget(self.spotIntLbl, 1, 0)

        self.spotIntLed = QtWidgets.QLineEdit()
        self.spotIntLed.setFixedWidth(75)
        self.spotAttrBoxLyt.addWidget(self.spotIntLed, 1, 1)

        self.spotIntSld = QtWidgets.QSlider()
        self.spotIntSld.setOrientation(QtCore.Qt.Horizontal)
        self.spotIntSld.setRange(0, 1000)
        self.spotAttrBoxLyt.addWidget(self.spotIntSld, 1, 2)

        self.spotDecayLyt = QtWidgets.QFormLayout()
        self.spotCommonLyt.addLayout(self.spotDecayLyt)

        self.spotDecayLbl = QtWidgets.QLabel('Decay Rate')
        self.spotDecayLbl.setAlignment(QtCore.Qt.AlignRight)
        self.spotDecayLbl.setFixedWidth(90)

        self.spotDecayCbx = QtWidgets.QComboBox()
        self.spotDecayCbx.setFixedWidth(95)
        self.spotDecayCbx.addItems(lightDecay.getList())
        self.spotDecayLyt.addRow(self.spotDecayLbl, self.spotDecayCbx)

        self.spotAiBox = QtWidgets.QGroupBox('Arnold')
        self.spotAttrLyt.addWidget(self.spotAiBox)
        self.spotAiLyt = QtWidgets.QVBoxLayout(self.spotAiBox)

        self.spotAiTempLyt = QtWidgets.QGridLayout()
        self.spotAiLyt.addLayout(self.spotAiTempLyt)

        self.spotNullLbl = QtWidgets.QLabel('')
        self.spotNullLbl.setFixedWidth(90)
        self.spotAiTempLyt.addWidget(self.spotNullLbl, 0, 0)
        self.spotTempChk = QtWidgets.QCheckBox('Use Color Temperature')
        self.spotAiTempLyt.addWidget(self.spotTempChk, 0, 1)

        self.spotAiBoxLyt = QtWidgets.QGridLayout()
        self.spotAiLyt.addLayout(self.spotAiBoxLyt)

        self.spotTempLbl = QtWidgets.QLabel('Temperature')
        self.spotTempLbl.setFixedWidth(90)
        self.spotTempLbl.setAlignment(QtCore.Qt.AlignRight)
        self.spotAiBoxLyt.addWidget(self.spotTempLbl, 1, 0)

        self.spotTempLed = QtWidgets.QLineEdit()
        self.spotTempLed.setFixedWidth(75)
        self.spotTempValidator = QtGui.QDoubleValidator()
        self.spotTempValidator.setDecimals(3)
        self.spotTempLed.setValidator(self.spotTempValidator)
        self.spotAiBoxLyt.addWidget(self.spotTempLed, 1, 1)

        self.spotTempSld = QtWidgets.QSlider()
        self.spotTempSld.setOrientation(QtCore.Qt.Horizontal)
        self.spotTempSld.setRange(0, 1000)
        self.spotAiBoxLyt.addWidget(self.spotTempSld, 1, 2)

        #        line = QtWidgets.QFrame()
        #        spotAiBoxLyt.addWidget(line,2,0)

        self.spotExpLbl = QtWidgets.QLabel('Exposure')
        self.spotExpLbl.setFixedWidth(90)
        self.spotExpLbl.setAlignment(QtCore.Qt.AlignRight)
        self.spotAiBoxLyt.addWidget(self.spotExpLbl, 3, 0)

        self.spotExpLed = QtWidgets.QLineEdit()
        self.spotExpLed.setFixedWidth(75)
        self.spotExpValidator = QtGui.QDoubleValidator()
        self.spotExpValidator.setDecimals(3)
        self.spotExpLed.setValidator(self.spotExpValidator)
        self.spotAiBoxLyt.addWidget(self.spotExpLed, 3, 1)

        self.spotExpSld = QtWidgets.QSlider()
        self.spotExpSld.setOrientation(QtCore.Qt.Horizontal)
        self.spotExpSld.setRange(0, 1000)
        self.spotAiBoxLyt.addWidget(self.spotExpSld, 3, 2)

        self.spotSmpLbl = QtWidgets.QLabel('Samples')
        self.spotSmpLbl.setFixedWidth(90)
        self.spotSmpLbl.setAlignment(QtCore.Qt.AlignRight)
        self.spotAiBoxLyt.addWidget(self.spotSmpLbl, 4, 0)

        self.spotSmpLed = QtWidgets.QLineEdit()
        self.spotSmpLed.setFixedWidth(75)
        self.spotSmpValidator = QtGui.QDoubleValidator()
        self.spotSmpValidator.setDecimals(3)
        self.spotSmpLed.setValidator(self.spotSmpValidator)
        self.spotAiBoxLyt.addWidget(self.spotSmpLed, 4, 1)

        self.spotSmpSld = QtWidgets.QSlider()
        self.spotSmpSld.setOrientation(QtCore.Qt.Horizontal)
        self.spotSmpSld.setRange(0, 1000)
        self.spotAiBoxLyt.addWidget(self.spotSmpSld, 4, 2)

        self.spotSprLbl = QtWidgets.QLabel('Spread')
        self.spotSprLbl.setFixedWidth(90)
        self.spotSprLbl.setAlignment(QtCore.Qt.AlignRight)
        self.spotAiBoxLyt.addWidget(self.spotSprLbl, 5, 0)

        self.spotSprLed = QtWidgets.QLineEdit()
        self.spotSprLed.setFixedWidth(75)
        self.spotSprValidator = QtGui.QDoubleValidator()
        self.spotSprValidator.setDecimals(3)
        self.spotSprLed.setValidator(self.spotSprValidator)
        self.spotAiBoxLyt.addWidget(self.spotSprLed, 5, 1)

        self.spotSprSld = QtWidgets.QSlider()
        self.spotSprSld.setOrientation(QtCore.Qt.Horizontal)
        self.spotSprSld.setRange(0, 1000)
        self.spotAiBoxLyt.addWidget(self.spotSprSld, 5, 2)

        self.spotBncLbl = QtWidgets.QLabel('Bounces')
        self.spotBncLbl.setFixedWidth(90)
        self.spotBncLbl.setAlignment(QtCore.Qt.AlignRight)
        self.spotAiBoxLyt.addWidget(self.spotBncLbl, 6, 0)

        self.spotBncLed = QtWidgets.QLineEdit()
        self.spotBncLed.setFixedWidth(75)
        self.spotAiBoxLyt.addWidget(self.spotBncLed, 6, 1)

        self.spotLgLyt = QtWidgets.QGridLayout()
        self.spotAiLyt.addLayout(self.spotLgLyt)

        self.spotLgLbl = QtWidgets.QLabel('AOV Light Group')
        self.spotLgLbl.setFixedWidth(90)
        self.spotLgLbl.setAlignment(QtCore.Qt.AlignRight)
        self.spotLgLyt.addWidget(self.spotLgLbl, 0, 0)
        self.spotLgLed = QtWidgets.QLineEdit('RGBA_')
        self.spotLgLyt.addWidget(self.spotLgLed, 0, 1)


def run():
    global mainWindow

    if not mainWindow or not cmds.window(mainWindow, q=True, e=True):
        mainWindow = lightingTool(parent=getMainWindow())
    mainWindow.show()
    mainWindow.raise_()

