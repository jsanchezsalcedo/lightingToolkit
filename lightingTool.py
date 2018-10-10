from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import QScrollArea, MayaQWidgetDockableMixin
import maya.cmds as cmds

from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance

mainWindow = None
__title__ = 'Lighting Toolkit'
__version__ = '1.1.1'

print ' '
print ' > {} {}.'.format(__title__,__version__)
print ' > by Jorge Sanchez Salcedo (2018)'
print ' > www.jorgesanchez-da.com'
print ' > jorgesanchez.da@gmail.com'
print ' '

def getMayaWindow():
    ptr = omui.MQtUtil.mainWindow()
    mainWindow = wrapInstance(long(ptr),QtWidgets.QMainWindow)
    return mainWindow

class LightingToolkitUI(MayaQWidgetDockableMixin, QScrollArea):
    def __init__(self, parent=None):
        super(LightingToolkitUI, self).__init__(parent)
        self.setMinimumHeight(335)
        self.setMinimumWidth(275)
        self.setWindowTitle('{} v{}'.format(__title__,__version__))
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.userInterface()

    def userInterface(self):
        lightType = self.getLightType()
        filterName = self.getFilterName()
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)

        lgtLayout = QtWidgets.QVBoxLayout()
        lgtGroupBox = QtWidgets.QGroupBox('Lights')
        lgtGbLayout = QtWidgets.QVBoxLayout(lgtGroupBox)
        lgtGbLayout.setAlignment(QtCore.Qt.AlignTop)
        self.lgtComboBox = QtWidgets.QComboBox()
        self.lgtComboBox.addItems(lightType)
        lgtNewLightButton = QtWidgets.QPushButton('New')
        lgtFromViewButton = QtWidgets.QPushButton('New from view')
        lgtFromObjectsButton = QtWidgets.QPushButton('New from objects')
        lgtSeparator = QtWidgets.QFrame()
        lgtIsolateButton = QtWidgets.QPushButton('Isolate')
        lgtIsolateButton.setCheckable(True)
        self.lgtIsoStatus = False

        lgtGbLayout.addWidget(self.lgtComboBox)
        lgtGbLayout.addWidget(lgtNewLightButton)
        lgtGbLayout.addWidget(lgtFromViewButton)
        lgtGbLayout.addWidget(lgtFromObjectsButton)
        lgtGbLayout.addWidget(lgtSeparator)

        lgtGbLayout.addWidget(lgtIsolateButton)

        lgtLayout.addWidget(lgtGroupBox)

        lgtNewLightButton.clicked.connect(self.createNewLight)
        lgtFromViewButton.clicked.connect(self.createFromView)
        lgtFromObjectsButton.clicked.connect(self.createFromObject)
        lgtIsolateButton.clicked.connect(self.isolateLights)

        fltLayout = QtWidgets.QVBoxLayout()
        fltGroupBox = QtWidgets.QGroupBox('Filters')
        fltGbLayout = QtWidgets.QVBoxLayout(fltGroupBox)
        fltGbLayout.setAlignment(QtCore.Qt.AlignTop)
        self.fltComboBox = QtWidgets.QComboBox()
        self.fltComboBox.addItems(filterName)
        fltAddFilterButton = QtWidgets.QPushButton('New')
        fltAddObjectButton = QtWidgets.QPushButton('New from objects')

        fltGbLayout.addWidget(self.fltComboBox)
        fltGbLayout.addWidget(fltAddFilterButton)
        fltGbLayout.addWidget(fltAddObjectButton)

        fltLayout.addWidget(fltGroupBox)

        fltAddFilterButton.clicked.connect(self.createNewFilter)
        fltAddObjectButton.clicked.connect(self.createFilterFromObject)

        mainLayout.addLayout(lgtLayout)
        mainLayout.addLayout(fltLayout)

        self.setLayout(mainLayout)

    def getLightType(self):
        lightType = [
            'aiSkyDomeLight',
            'directionalLight',
            'areaLight',
            'spotLight',
            'pointLight'
            ]

        return lightType

    def getFilterName(self):
        filterName = [
            'aiGobo',
            'aiBarndoor',
            'aiLightBlocker',
            'aiLightDecay'
            ]

        return filterName

    def createNewLight(self):
        type = self.lgtComboBox.currentText()
        name = type + 'Shape1'
        cmds.shadingNode(type, n=name, al=True)
        print 'You have created',type,', successfully.'

    def createFromView(self):

        selectedCam = cmds.ls(sl = True)

        transform = {
            'translateX': '',
            'translateY': '',
            'translateZ': '',
            'rotateX': '',
            'rotateY': '',
            'rotateZ': ''
            }

        for i in selectedCam:
            panel = cmds.getPanel(wf=True)
            camera = cmds.modelPanel(panel, q=True, cam=True)
            print camera
            cameraShape = cmds.listRelatives(camera, ad = True)
            print cameraShape

            if cmds.ls(cameraShape, st = True)[1] == 'camera':
                for k, v in transform.iteritems():
                    attr = i + '.' + k
                    val = cmds.getAttr(attr)
                    transform[k] = val

                type = self.lgtComboBox.currentText()
                name = type + 'Shape1'
                newLight = cmds.shadingNode(type, n=name, al = True)
                print 'You have created', type, 'from', i, ', successfuly.'

                for k, v in transform.iteritems():
                    attr = newLight + '.' + k
                    cmds.setAttr(attr, transform[k])

                cmds.lookThru(newLight, panel)

            else:
                print 'First, you have to select a camera.'

    def createFromObject(self):
        selectedMesh = cmds.ls(sl = True)

        transform = {
            'translateX': '',
            'translateY': '',
            'translateZ': '',
            'rotateX': '',
            'rotateY': '',
            'rotateZ': ''
            }

        for i in selectedMesh:
            type = self.lgtComboBox.currentText()
            newLight = cmds.shadingNode(type, al = True)
            name = i + 'Light'
            newLight = cmds.rename(newLight, name)
            print 'You have created', newLight, 'on', i, ', successfuly.'

            for k, v in transform.iteritems():
                attr = i + '.' + k
                val = cmds.getAttr(attr)
                transform[k] = val
                attr = newLight + '.' + k
                cmds.setAttr(attr, transform[k])

            cmds.parentConstraint(i, newLight, mo=True, w=1)

    def isolateLights(self):
        lightType = self.getLightType()
        sceneLights = cmds.ls(typ=lightType)

        if self.lgtIsoStatus == False:
            self.lgtIsoStatus = True
            for i in sceneLights:
                visAttr = i + '.visibility'
                visibility = cmds.getAttr(visAttr)
                selectedLights = cmds.listRelatives(cmds.ls(sl = True), s = True)
                try:
                    if i not in selectedLights:
                        cmds.setAttr(visAttr, 0)
                    else:
                        cmds.setAttr(visAttr, 1)
                except TypeError:
                    if visibility == True:
                        cmds.setAttr(visAttr, 0)
                    else:
                        cmds.setAttr(visAttr, 1)
        else:
            self.lgtIsoStatus = False
            for i in sceneLights:
                visAttr = i + '.visibility'
                cmds.setAttr(visAttr, 1)

    def createNewFilter(self):
        lightType = self.getLightType()
        lightSel = cmds.ls(sl=True, dag=True, typ=lightType)
        sceneSets = cmds.ls(set = True)

        if 'defaultFilterSet' in sceneSets:
            pass
        else:
            cmds.sets(n = 'defaultFilterSet', em = True)

        type = self.fltComboBox.currentText()
        self.name = type + 'Shape1'
        newFilter = cmds.shadingNode(type, n=self.name, al=True)

        cmds.sets(newFilter, rm='defaultLightSet')
        cmds.sets(newFilter, add='defaultFilterSet')

        print 'You have created', newFilter, ', succesfully.'

        for light in lightSel:
            print light
            for i in range(10):
                checkConn = cmds.connectionInfo(light + '.aiFilters[' + str(i) + ']', ied = True)

                if checkConn == True:
                    continue
                else:
                    filterConn = newFilter + '.message'
                    freeSlot = light + '.aiFilters[' + str(i) + ']'

                    cmds.connectAttr(filterConn, freeSlot)
                    print '   > You just connect:'
                    print '     ', newFilter, 'to', freeSlot
                    break

    def createFilterFromObject(self):
        lightType = self.getLightType()
        lightSel = cmds.ls(sl=True, dag=True, typ=lightType)
        meshSel = cmds.listRelatives(cmds.ls(sl=True, dag=True, type='mesh'),p=True)
        sceneSets = cmds.ls(set = True)

        if 'defaultFilterSet' in sceneSets:
            pass
        else:
            cmds.sets(n = 'defaultFilterSet', em = True)
        for i in meshSel:
            transform = cmds.xform(i, q = True, bb = True, a = True, ws = True)

            sizeX = transform[3] - transform[0]
            sizeY = transform[4] - transform[1]
            sizeZ = transform[5] - transform[2]

            posX = sizeX / 2 + transform[0]
            posY = sizeY / 2 + transform[1]
            posZ = sizeZ / 2 + transform[2]

            type = self.fltComboBox.currentText()
            self.name = type + 'Shape1'
            newFilter = cmds.shadingNode(type, n=self.name, al=True)

            cmds.sets(newFilter, rm='defaultLightSet')
            cmds.sets(newFilter, add='defaultFilterSet')

            cmds.xform(newFilter, t=(posX, posY, posZ), s=(sizeX, sizeY, sizeZ))

            print 'You have created', newFilter, ', succesfully.'

            for light in lightSel:
                print light
                for i in range(10):
                    checkConn = cmds.connectionInfo(light + '.aiFilters[' + str(i) + ']', ied=True)

                    if checkConn == True:
                        continue
                    else:
                        filterConn = newFilter + '.message'
                        freeSlot = light + '.aiFilters[' + str(i) + ']'

                        cmds.connectAttr(filterConn, freeSlot)
                        print '   > You just connect:'
                        print '     ', newFilter, 'to', freeSlot
                        break

def run():
    global mainWindow
    if not mainWindow or not cmds.window(mainWindow, q=True, e=True):
        mainWindow = LightingToolkitUI()
    mainWindow.show(dockable = True, floating = True)
