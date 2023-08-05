#!/usr/bin/env python3


#############################################################################
##
## Copyright (C) 2014 Riverbank Computing Limited.
## Copyright (C) 2014 Digia Plc
## All rights reserved.
## For any questions to Digia, please use contact form at http://qt.digia.com
##
## This file is part of the QtDataVisualization module.
##
## Licensees holding valid Qt Enterprise licenses may use this file in
## accordance with the Qt Enterprise License Agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and Digia.
##
## If you have questions regarding the use of this file, please use
## contact form at http://qt.digia.com
##
#############################################################################


import math

from PyQt5.QtCore import pyqtSignal, QObject, QSize, Qt
from PyQt5.QtDataVisualization import (Q3DCamera, Q3DTheme, Q3DScatter,
        QAbstract3DGraph, QAbstract3DSeries, QScatter3DSeries,
        QScatterDataItem, QScatterDataProxy)
from PyQt5.QtGui import QFont, QVector3D
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QFontComboBox,
        QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget)


class ScatterDataModifier(QObject):

    numberOfItems = 3600
    curveDivider = 3.0
    lowerNumberOfItems = 900
    lowerCurveDivider = 0.75

    backgroundEnabledChanged = pyqtSignal(bool)
    gridEnabledChanged = pyqtSignal(bool)
    shadowQualityChanged = pyqtSignal(int)
    fontChanged = pyqtSignal(QFont)

    def __init__(self, scatter):
        super(ScatterDataModifier, self).__init__()

        self.m_graph = scatter
        self.m_fontSize = 40.0
        self.m_style = QAbstract3DSeries.MeshSphere
        self.m_smooth = True
        self.m_itemCount = self.lowerNumberOfItems
        self.m_curveDivider = self.lowerCurveDivider

        self.m_graph.activeTheme().setType(Q3DTheme.ThemeEbony)
        font = self.m_graph.activeTheme().font()
        font.setPointSize(self.m_fontSize)
        self.m_graph.activeTheme().setFont(font)
        self.m_graph.setShadowQuality(QAbstract3DGraph.ShadowQualitySoftLow)
        self.m_graph.scene().activeCamera().setCameraPreset(
                Q3DCamera.CameraPresetFront)

        proxy = QScatterDataProxy()
        series = QScatter3DSeries(proxy)
        series.setItemLabelFormat(
                "@xTitle: @xLabel @yTitle: @yLabel @zTitle: @zLabel")
        series.setMeshSmooth(self.m_smooth)
        self.m_graph.addSeries(series)

        self.addData()

    def addData(self):
        self.m_graph.axisX().setTitle("X")
        self.m_graph.axisY().setTitle("Y")
        self.m_graph.axisZ().setTitle("Z")

        dataArray = []

        limit = math.sqrt(self.m_itemCount) / 2.0
        i = -limit
        while i < limit:
            j = -limit
            while j < limit:
                itm = QScatterDataItem(
                        QVector3D(i + 0.5,
                                math.cos(
                                        math.radians((i * j) / self.m_curveDivider)),
                                j + 0.5))
                dataArray.append(itm)
                j += 1.0

            i += 1.0

        self.m_graph.seriesList()[0].dataProxy().resetArray(dataArray)

    def changeStyle(self, style):
        comboBox = self.sender()
        if isinstance(comboBox, QComboBox):
            self.m_style = QAbstract3DSeries.Mesh(comboBox.itemData(style))
            self.m_graph.seriesList()[0].setMesh(self.m_style)

    def setSmoothDots(self, smooth):
        self.m_smooth = bool(smooth)
        self.m_graph.seriesList()[0].setMeshSmooth(self.m_smooth)

    def changeTheme(self, theme):
        currentTheme = self.m_graph.activeTheme()
        currentTheme.setType(Q3DTheme.Theme(theme))
        self.backgroundEnabledChanged.emit(currentTheme.isBackgroundEnabled())
        self.gridEnabledChanged.emit(currentTheme.isGridEnabled())
        self.fontChanged.emit(currentTheme.font())

    preset = int(Q3DCamera.CameraPresetFrontLow)

    def changePresetCamera(self):
        self.m_graph.scene().activeCamera().setCameraPreset(
                Q3DCamera.CameraPreset(self.preset))

        self.preset += 1

        if self.preset > Q3DCamera.CameraPresetDirectlyBelow:
            self.preset = int(Q3DCamera.CameraPresetFrontLow)

    def changeLabelStyle(self):
        self.m_graph.activeTheme().setLabelBackgroundEnabled(
                not self.m_graph.activeTheme().isLabelBackgroundEnabled())

    def changeFont(self, font):
        newFont = QFont(font)
        newFont.setPointSizeF(self.m_fontSize)
        self.m_graph.activeTheme().setFont(newFont)

    def shadowQualityUpdatedByVisual(self, sq):
        self.shadowQualityChanged.emit(int(sq))

    def changeShadowQuality(self, quality):
        sq = QAbstract3DGraph.ShadowQuality(quality)
        self.m_graph.setShadowQuality(sq)

    def setBackgroundEnabled(self, enabled):
        self.m_graph.activeTheme().setBackgroundEnabled(enabled)

    def setGridEnabled(self, enabled):
        self.m_graph.activeTheme().setGridEnabled(enabled)

    def toggleItemCount(self):
        if self.m_itemCount == self.numberOfItems:
            self.m_itemCount = self.lowerNumberOfItems
            self.m_curveDivider = self.lowerCurveDivider
        else:
            self.m_itemCount = self.numberOfItems
            self.m_curveDivider = self.curveDivider

        self.m_graph.seriesList()[0].dataProxy().resetArray(None)
        self.addData()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    graph = Q3DScatter()
    container = QWidget.createWindowContainer(graph)

    screenSize = graph.screen().size()
    container.setMinimumSize(
            QSize(screenSize.width() / 2, screenSize.height() / 1.5))
    container.setMaximumSize(screenSize)
    container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    container.setFocusPolicy(Qt.StrongFocus)

    widget = QWidget()
    hLayout = QHBoxLayout(widget)
    vLayout = QVBoxLayout()
    hLayout.addWidget(container, 1)
    hLayout.addLayout(vLayout)

    widget.setWindowTitle("A Cosine Wave")

    themeList = QComboBox()
    themeList.addItem("Qt")
    themeList.addItem("Primary Colors")
    themeList.addItem("Digia")
    themeList.addItem("Stone Moss")
    themeList.addItem("Army Blue")
    themeList.addItem("Retro")
    themeList.addItem("Ebony")
    themeList.addItem("Isabelle")
    themeList.setCurrentIndex(6)

    labelButton = QPushButton("Change label style")

    smoothCheckBox = QCheckBox("Smooth dots", checked=True)

    itemStyleList = QComboBox()
    itemStyleList.addItem("Sphere", QAbstract3DSeries.MeshSphere)
    itemStyleList.addItem("Cube", QAbstract3DSeries.MeshCube)
    itemStyleList.addItem("Minimal", QAbstract3DSeries.MeshMinimal)
    itemStyleList.addItem("Point", QAbstract3DSeries.MeshPoint)
    itemStyleList.setCurrentIndex(0)

    cameraButton = QPushButton("Change camera preset")

    itemCountButton = QPushButton("Toggle item count")

    backgroundCheckBox = QCheckBox("Show background", checked=True)

    gridCheckBox = QCheckBox("Show grid", checked=True)

    shadowQuality = QComboBox()
    shadowQuality.addItem("None")
    shadowQuality.addItem("Low")
    shadowQuality.addItem("Medium")
    shadowQuality.addItem("High")
    shadowQuality.addItem("Low Soft")
    shadowQuality.addItem("Medium Soft")
    shadowQuality.addItem("High Soft")
    shadowQuality.setCurrentIndex(4)

    fontList = QFontComboBox()
    fontList.setCurrentFont(QFont('Arial'))

    vLayout.addWidget(labelButton, 0, Qt.AlignTop)
    vLayout.addWidget(cameraButton, 0, Qt.AlignTop)
    vLayout.addWidget(itemCountButton, 0, Qt.AlignTop)
    vLayout.addWidget(backgroundCheckBox)
    vLayout.addWidget(gridCheckBox)
    vLayout.addWidget(smoothCheckBox, 0, Qt.AlignTop)
    vLayout.addWidget(QLabel("Change dot style"))
    vLayout.addWidget(itemStyleList)
    vLayout.addWidget(QLabel("Change theme"))
    vLayout.addWidget(themeList)
    vLayout.addWidget(QLabel("Adjust shadow quality"))
    vLayout.addWidget(shadowQuality)
    vLayout.addWidget(QLabel("Change font"))
    vLayout.addWidget(fontList, 1, Qt.AlignTop)

    modifier = ScatterDataModifier(graph)

    cameraButton.clicked.connect(modifier.changePresetCamera)
    labelButton.clicked.connect(modifier.changeLabelStyle)
    itemCountButton.clicked.connect(modifier.toggleItemCount)

    backgroundCheckBox.stateChanged.connect(modifier.setBackgroundEnabled)
    gridCheckBox.stateChanged.connect(modifier.setGridEnabled)
    smoothCheckBox.stateChanged.connect(modifier.setSmoothDots)

    modifier.backgroundEnabledChanged.connect(backgroundCheckBox.setChecked)
    modifier.gridEnabledChanged.connect(gridCheckBox.setChecked)
    itemStyleList.currentIndexChanged.connect(modifier.changeStyle)

    themeList.currentIndexChanged.connect(modifier.changeTheme)

    shadowQuality.currentIndexChanged.connect(modifier.changeShadowQuality)

    modifier.shadowQualityChanged.connect(shadowQuality.setCurrentIndex)
    graph.shadowQualityChanged.connect(modifier.shadowQualityUpdatedByVisual)

    fontList.currentFontChanged.connect(modifier.changeFont)

    modifier.fontChanged.connect(fontList.setCurrentFont)

    widget.show()
    sys.exit(app.exec_())
