from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya import cmds as cmds

try:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance
except ImportError:
    from PySide import QtCore, QtGui, QtWidgets
    from shiboken import wrapInstance

mainWindow = None
__title__ = 'Lighting Toolkit'
__version__ = '1.2.5'

print ' '
print ' > {} {}.'.format(__title__,__version__)
print ' > by Jorge Sanchez Salcedo (2019)'
print ' > www.jorgesanchez-da.com'
print ' > jorgesanchez.da@gmail.com'
print ' '

def getMayaWindow():
    ptr = omui.MQtUtil.mainWindow()
    mainWindow = wrapInstance(long(ptr),QtWidgets.QWidget)
    return mainWindow

class LgtToolkit():
    def getLightType(self):
        lightTypes = ['aiSkyDomeLight',
                      'areaLight',
                      'directionalLight',
                      'pointLight',
                      'spotLight',
                      'aiMeshLight',
                      'aiPhotometricLight',
                      'aiLightPortal',
                      'aiPhysicalSky']

        return lightTypes

    def getLightName(self):
        sceneLights = []
        lightTypes = self.getLightType()
        sceneLights = cmds.listRelatives(cmds.ls(typ=lightTypes), p=True)
        return sceneLights

    def getFilterType(self):
        filterTypes = ['aiGobo',
                      'aiBarndoor',
                      'aiLightBlocker',
                      'aiLightDecay']

        return filterTypes

    def getFilterName(self):
        sceneFilters = []
        filterTypes = self.getFilterType()
        sceneFilters = cmds.ls(typ=filterTypes)
        return sceneFilters

class LgtToolkitUI(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(LgtToolkitUI, self).__init__(parent)
        self.setWindowTitle('{} {}'.format(__title__, __version__))
        self.setMinimumHeight(350)
        self.setMinimumWidth(285)
        self.toolkit = LgtToolkit()
        self.createUI()

    def createUI(self):
        tabWidget = QtWidgets.QTabWidget()

        ###############################################################

        lightsTab = QtWidgets.QWidget()

        lightsTabLayout = QtWidgets.QVBoxLayout(lightsTab)
        lightsTabLayout.setContentsMargins(0,0,0,0)
        lightsTabLayout.setAlignment(QtCore.Qt.AlignTop)

        lightsTabSplitter = QtWidgets.QSplitter(orientation=QtCore.Qt.Vertical)

        lightsTopWidget = QtWidgets.QWidget()
        lightsTopLayout = QtWidgets.QVBoxLayout(lightsTopWidget)
        lightsTopLayout.setContentsMargins(0,0,0,0)

        lightListLabels = ['Name', 'I', 'E', 'S', 'B']
        self.lightListWidget = QtWidgets.QTableWidget()
        self.lightListWidget.horizontalHeader().setVisible(True)
        self.lightListWidget.verticalHeader().setVisible(False)
        self.lightListWidget.setColumnCount(len(lightListLabels))
        self.lightListWidget.resizeColumnsToContents()
        self.lightListWidget.setColumnWidth(0,135)
        self.lightListWidget.setColumnWidth(1, 30)
        self.lightListWidget.setColumnWidth(2, 30)
        self.lightListWidget.setColumnWidth(3, 30)
        self.lightListWidget.setColumnWidth(4, 30)
        self.lightListWidget.setHorizontalHeaderLabels(lightListLabels)
        self.lightListWidget.setAlternatingRowColors(True)
        self.lightListWidget.setSortingEnabled(True)
        self.lightListWidget.setShowGrid(False)

        self.lightListWidget.itemClicked.connect(self.selectLights)

        lightsTopLayout.addWidget(self.lightListWidget)

        lightsButtonWidget = QtWidgets.QWidget()
        lightsButtonLayout = QtWidgets.QHBoxLayout(lightsButtonWidget)
        lightsTopLayout.addWidget(lightsButtonWidget)

        isolateButton = QtWidgets.QPushButton('Isolate')
        isolateButton.setCheckable(True)
        self.isolateStatus = False
        lightsButtonLayout.addWidget(isolateButton)
        isolateButton.clicked.connect(self.isolateLights)

        deleteLightButton = QtWidgets.QPushButton('Delete')
        lightsButtonLayout.addWidget(deleteLightButton)
        deleteLightButton.clicked.connect(self.deleteLights)

        lightsTabSplitter.addWidget(lightsTopWidget)

        lightAttrWidget = QtWidgets.QWidget()

        lightAttrLayout = QtWidgets.QVBoxLayout(lightAttrWidget)

        #lightsTabSplitter.addWidget(lightAttrWidget)

        lightsTabLayout.addWidget(lightsTabSplitter)

        tabWidget.addTab(lightsTab, 'Lights')

        ###############################################################

        filtersTab = QtWidgets.QWidget()

        filtersTabLayout = QtWidgets.QVBoxLayout(filtersTab)
        filtersTabLayout.setContentsMargins(0, 0, 0, 0)
        filtersTabLayout.setAlignment(QtCore.Qt.AlignTop)

        filtersTabSplitter = QtWidgets.QSplitter(orientation=QtCore.Qt.Vertical)

        filtersTopWidget = QtWidgets.QWidget()
        filtersTopLayout = QtWidgets.QVBoxLayout(filtersTopWidget)
        filtersTopLayout.setContentsMargins(0, 0, 0, 0)

        filterListLabels = ['Name']
        self.filterListWidget = QtWidgets.QTableWidget()
        self.filterListWidget.horizontalHeader().setVisible(True)
        self.filterListWidget.verticalHeader().setVisible(False)
        self.filterListWidget.setColumnCount(len(filterListLabels))
        self.filterListWidget.resizeColumnsToContents()
        self.filterListWidget.setColumnWidth(0, 265)
        self.filterListWidget.setHorizontalHeaderLabels(filterListLabels)
        self.filterListWidget.setAlternatingRowColors(True)
        self.filterListWidget.setSortingEnabled(True)
        self.filterListWidget.setShowGrid(False)

        self.filterListWidget.itemClicked.connect(self.selectFilters)

        filtersTopLayout.addWidget(self.filterListWidget)

        filtersButtonWidget = QtWidgets.QWidget()
        filtersButtonLayout = QtWidgets.QHBoxLayout(filtersButtonWidget)
        filtersTopLayout.addWidget(filtersButtonWidget)

        selectFilterLightsButton = QtWidgets.QPushButton('Select Filter Lights')
        filtersButtonLayout.addWidget(selectFilterLightsButton)
        selectFilterLightsButton.clicked.connect(self.selectFilterLights)

        filtersTabSplitter.addWidget(filtersTopWidget)

        filterAttrWidget = QtWidgets.QWidget()

        filterAttrLayout = QtWidgets.QVBoxLayout(filterAttrWidget)

        #filtersTabSplitter.addWidget(filterAttrWidget)

        filtersTabLayout.addWidget(filtersTabSplitter)

        tabWidget.addTab(filtersTab, 'Filters')

        ###############################################################

        toolkitTab = QtWidgets.QWidget()

        toolkitTabLayout = QtWidgets.QVBoxLayout(toolkitTab)
        toolkitTabLayout.setAlignment(QtCore.Qt.AlignTop)

        lgtToolkitBox = QtWidgets.QGroupBox('Lights')
        lgtToolkitLayout = QtWidgets.QVBoxLayout(lgtToolkitBox)

        self.selectLightType = QtWidgets.QComboBox()
        self.selectLightType.addItems(self.toolkit.getLightType())
        lgtToolkitLayout.addWidget(self.selectLightType)

        createLightButton = QtWidgets.QPushButton('Create')
        createLightButton.clicked.connect(self.createLight)
        lgtToolkitLayout.addWidget(createLightButton)

        createLightViewButton = QtWidgets.QPushButton('Create from view')
        createLightViewButton.clicked.connect(self.createLightView)
        lgtToolkitLayout.addWidget(createLightViewButton)

        createLightObjectButton = QtWidgets.QPushButton('Create from object')
        createLightObjectButton.clicked.connect(self.createLightObject)
        lgtToolkitLayout.addWidget(createLightObjectButton)

        toolkitTabLayout.addWidget(lgtToolkitBox)

        fltToolkitBox = QtWidgets.QGroupBox('Filters')
        fltToolkitLayout = QtWidgets.QVBoxLayout(fltToolkitBox)

        self.selectFilterType = QtWidgets.QComboBox()
        self.selectFilterType.addItems(self.toolkit.getFilterType())
        fltToolkitLayout.addWidget(self.selectFilterType)

        createFilterButton = QtWidgets.QPushButton('Create')
        createFilterButton.clicked.connect(self.createFilter)
        fltToolkitLayout.addWidget(createFilterButton)

        createFilterObjectButton = QtWidgets.QPushButton('Create from object')
        createFilterObjectButton.clicked.connect(self.createFilterObject)
        fltToolkitLayout.addWidget(createFilterObjectButton)

        toolkitTabLayout.addWidget(fltToolkitBox)

        tabWidget.addTab(toolkitTab, 'Tools')

        ###############################################################

        self.setCentralWidget(tabWidget)

        self.populateLights()

    def createLight(self):
        type = self.selectLightType.currentText()
        name = type + 'Shape'
        cmds.shadingNode(type, n=name, al=True)
        print 'You have created', name, 'successfully.'
        self.populateLights()

    def createLightView(self):
        selectedCam = cmds.ls(sl=True)

        transform = {
            'translateX': '',
            'translateY': '',
            'translateZ': '',
            'rotateX': '',
            'rotateY': '',
            'rotateZ': ''
        }

        try:
            for i in selectedCam:
                panel = cmds.getPanel(wf=True)
                camera = cmds.modelPanel(panel, q=True, cam=True)
                cameraShape = cmds.listRelatives(camera, ad=True)

                if cmds.ls(cameraShape, st=True)[1] == 'camera':
                    for k, v in transform.iteritems():
                        attr = i + '.' + k
                        val = cmds.getAttr(attr)
                        transform[k] = val

                    type = self.selectLightType.currentText()
                    name = type + 'Shape'
                    newLight = cmds.shadingNode(type, n=name, al=True)
                    print 'You have created', name, 'from', camera, 'successfully.'

                    for k, v in transform.iteritems():
                        attr = newLight + '.' + k
                        cmds.setAttr(attr, transform[k])

                    cmds.lookThru(newLight, panel)

                    self.populateLights()

                else:
                    print 'First, you have to select a camera.'

        except RuntimeError:
            print 'First, you have to select a camera.'

    def createLightObject(self):
        selectedMesh = cmds.ls(sl=True)

        transform = {
            'translateX': '',
            'translateY': '',
            'translateZ': '',
            'rotateX': '',
            'rotateY': '',
            'rotateZ': ''
        }

        for i in sorted(selectedMesh):
            type = self.selectLightType.currentText()
            name = type + 'Shape'
            newLight = cmds.shadingNode(type, n=name, al=True)
            print 'You have created', newLight, 'on', i, 'successfully.'

            for k, v in transform.iteritems():
                attr = i + '.' + k
                val = cmds.getAttr(attr)
                transform[k] = val
                attr = newLight + '.' + k
                cmds.setAttr(attr, transform[k])

            cmds.parentConstraint(i, newLight, mo=True, w=1)

        self.populateLights()

    def createFilter(self):
        lightType = self.toolkit.getLightType()
        lightSelection = cmds.ls(sl=True, dag=True, typ=lightType)
        sceneSets = cmds.ls(set=True)

        if 'defaultFilterSet' in sceneSets:
            pass
        else:
            cmds.sets(n='defaultFilterSet', em=True)

        type = self.selectFilterType.currentText()
        name = type + 'Shape'
        newFilter = cmds.shadingNode(type, n=name, al=True)

        cmds.sets(newFilter, rm='defaultLightSet')
        cmds.sets(newFilter, add='defaultFilterSet')

        print 'You have created', newFilter, 'succesfully.'

        for light in sorted(lightSelection):
            for i in range(10):
                checkConnections = cmds.connectionInfo(light + '.aiFilters[' + str(i) + ']', ied=True)

                if checkConnections == True:
                    continue
                else:
                    filterConnection = newFilter + '.message'
                    freeSlot = light + '.aiFilters[' + str(i) + ']'

                    cmds.connectAttr(filterConnection, freeSlot)
                    print '   > You just connect:'
                    print '     ', newFilter, 'to', freeSlot
                    break

        self.populateFilters()

    def createFilterObject(self):
        lightType = self.toolkit.getLightType()
        lightSelection = cmds.ls(sl=True, dag=True, typ=lightType)
        meshSelection = cmds.listRelatives(cmds.ls(sl=True, dag=True, type='mesh'), p=True)
        sceneSets = cmds.ls(set=True)

        if 'defaultFilterSet' in sceneSets:
            pass
        else:
            cmds.sets(n='defaultFilterSet', em=True)

        for i in sorted(meshSelection):
            transform = cmds.xform(i, q=True, bb=True, a=True, ws=True)

            sizeX = transform[3] - transform[0]
            sizeY = transform[4] - transform[1]
            sizeZ = transform[5] - transform[2]

            posX = sizeX / 2 + transform[0]
            posY = sizeY / 2 + transform[1]
            posZ = sizeZ / 2 + transform[2]

            type = self.selectFilterType.currentText()
            name = type + 'Shape'
            newFilter = cmds.shadingNode(type, n=name, al=True)

            cmds.sets(newFilter, rm='defaultLightSet')
            cmds.sets(newFilter, add='defaultFilterSet')

            cmds.xform(newFilter, t=(posX, posY, posZ), s=(sizeX, sizeY, sizeZ))

            print 'You have created', newFilter, 'succesfully.'

            for light in lightSelection:
                for i in range(10):
                    checkConnection = cmds.connectionInfo(light + '.aiFilters[' + str(i) + ']', ied=True)

                    if checkConnection == True:
                        continue
                    else:
                        filterConnection = newFilter + '.message'
                        freeSlot = light + '.aiFilters[' + str(i) + ']'

                        cmds.connectAttr(filterConnection, freeSlot)
                        print '   > You just connect:'
                        print '     ', newFilter, 'to', freeSlot
                        break

        self.populateFilters()

    def populateLights(self):
        self.lightListWidget.clearContents()
        self.lightListWidget.setRowCount(0)
        sceneLights = self.toolkit.getLightName()

        try:
            for light in sorted(sceneLights):
                itemName = QtWidgets.QTableWidgetItem(light)

                intensity = str(cmds.getAttr(light + '.intensity'))
                itemInt = QtWidgets.QTableWidgetItem(intensity)
                itemInt.setFlags(QtCore.Qt.ItemIsEnabled)
                itemInt.setTextAlignment(QtCore.Qt.AlignCenter)

                exposure = str(cmds.getAttr(light + '.aiExposure'))
                itemExp = QtWidgets.QTableWidgetItem(exposure)
                itemExp.setFlags(QtCore.Qt.ItemIsEnabled)
                itemExp.setTextAlignment(QtCore.Qt.AlignCenter)

                samples = str(cmds.getAttr(light + '.aiSamples'))
                itemSamples = QtWidgets.QTableWidgetItem(samples)
                itemSamples.setFlags(QtCore.Qt.ItemIsEnabled)
                itemSamples.setTextAlignment(QtCore.Qt.AlignCenter)

                bounces = str(cmds.getAttr(light + '.aiMaxBounces'))
                itemBounces = QtWidgets.QTableWidgetItem(bounces)
                itemBounces.setFlags(QtCore.Qt.ItemIsEnabled)
                itemBounces.setTextAlignment(QtCore.Qt.AlignCenter)

                row = self.lightListWidget.rowCount()
                rowNum = 0 + row

                self.lightListWidget.insertRow(rowNum)
                self.lightListWidget.setItem(rowNum, 0, itemName)
                self.lightListWidget.setItem(rowNum, 1, itemInt)
                self.lightListWidget.setItem(rowNum, 2, itemExp)
                self.lightListWidget.setItem(rowNum, 3, itemSamples)
                self.lightListWidget.setItem(rowNum, 4, itemBounces)

        except TypeError:
            pass

        self.populateFilters()

    def selectLights(self):
        try:
            items = self.lightListWidget.selectedItems()
            lights = [light.text() for light in items]
            cmds.select(lights)
            return lights
        except TypeError:
            pass

    def isolateLights(self):
        sceneLights = self.toolkit.getLightName()

        if self.isolateStatus == False:
            self.isolateStatus = True
            for light in sceneLights:
                visAttr = light + '.visibility'
                visibility = cmds.getAttr(visAttr)
                selectedLights = cmds.ls(sl = True)
                try:
                    if light not in selectedLights:
                        cmds.setAttr(visAttr, 0)
                    else:
                        cmds.setAttr(visAttr, 1)
                except TypeError:
                    if visibility == True:
                        cmds.setAttr(visAttr, 0)
                    else:
                        cmds.setAttr(visAttr, 1)
        else:
            self.isolateStatus = False
            for light in sceneLights:
                visAttr = light + '.visibility'
                cmds.setAttr(visAttr, 1)

    def deleteLights(self):
        selectedLights = self.selectLights()
        cmds.delete(selectedLights)
        self.populateLights()

    def populateFilters(self):
        self.filterListWidget.clearContents()
        self.filterListWidget.setRowCount(0)
        sceneFilters = self.toolkit.getFilterName()

        try:
            for filter in sorted(sceneFilters):
                itemName = QtWidgets.QTableWidgetItem(filter)

                row = self.filterListWidget.rowCount()
                rowNum = 0 + row

                self.filterListWidget.insertRow(rowNum)
                self.filterListWidget.setItem(rowNum, 0, itemName)

        except TypeError:
            pass

    def selectFilters(self):
        try:
            items = self.filterListWidget.selectedItems()
            filters = [filter.text() for filter in items]
            cmds.select(filters)
            return filters
        except TypeError:
            pass

    def selectFilterLights(self):
        selectedFilter = self.selectFilters()[-1]
        selectedFilter = cmds.listRelatives(selectedFilter, p=True)
        for filter in selectedFilter:
            lights = cmds.listConnections(filter)
            lights.remove('defaultFilterSet')
            cmds.select(lights, add=True)

def run():
    global mainWindow
    if not mainWindow or not cmds.window(mainWindow, q=True, e=True):
        mainWindow = LgtToolkitUI(parent=getMayaWindow())
    mainWindow.show(dockable=True)
