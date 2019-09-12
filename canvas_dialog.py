# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'canvas_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from qgis.PyQt import uic
import os, math
from qgis.core import *
from qgis.PyQt import uic
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply, \
    QNetworkAccessManager

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'canvas_dialog.ui'))

class Ui_canvas_Dialog(object):
    def setupUi(self, iface, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(505, 450)
        self.Description = QtWidgets.QLabel(Dialog)
        self.Description.setGeometry(QtCore.QRect(150, 110, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Description.setFont(font)
        self.Description.setObjectName("Description")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(40, 30, 401, 101))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(":/plugins/assimila_datacube2/"
                                             "img/assimila_namelogo.png"))
        self.label_9.setScaledContents(True)
        self.label_9.setObjectName("label_9")
        self.btn_extent = QtWidgets.QPushButton(Dialog)
        self.btn_extent.setGeometry(QtCore.QRect(350, 310, 121, 31))
        self.btn_extent.setObjectName("btn_extent")
        self.N_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.N_spinBox.setGeometry(QtCore.QRect(160, 200, 81, 41))
        self.N_spinBox.setMinimum(-90.0)
        self.N_spinBox.setMaximum(90.0)
        self.N_spinBox.setProperty("value", 10.05)
        self.N_spinBox.setObjectName("N_spinBox")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(160, 180, 91, 16))
        self.label_5.setObjectName("label_5")
        self.W_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.W_spinBox.setGeometry(QtCore.QRect(60, 250, 81, 41))
        self.W_spinBox.setMinimum(-180.0)
        self.W_spinBox.setMaximum(180.0)
        self.W_spinBox.setObjectName("W_spinBox")
        self.S_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.S_spinBox.setGeometry(QtCore.QRect(160, 300, 81, 41))
        self.S_spinBox.setMinimum(-90.0)
        self.S_spinBox.setMaximum(90.0)
        self.S_spinBox.setObjectName("S_spinBox")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(130, 390, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox
                                          .Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(60, 230, 91, 16))
        self.label_7.setObjectName("label_7")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(160, 280, 91, 16))
        self.label_6.setObjectName("label_6")
        self.E_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.E_spinBox.setGeometry(QtCore.QRect(260, 250, 81, 41))
        self.E_spinBox.setMinimum(-180.0)
        self.E_spinBox.setMaximum(180.0)
        self.E_spinBox.setProperty("value", 10.0)
        self.E_spinBox.setObjectName("E_spinBox")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(260, 230, 91, 16))
        self.label_8.setObjectName("label_8")
        self.iface=iface
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.btn_extent.clicked.connect(self.on_btn_extent)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Description.setText(_translate("Dialog", "A QGIS plugin to "
                                                      "visualise a datacube"))
        self.btn_extent.setText(_translate("Dialog", "Set canvas extent"))
        self.label_5.setText(_translate("Dialog", "North"))
        self.label_7.setText(_translate("Dialog", "West"))
        self.label_6.setText(_translate("Dialog", "South"))
        self.label_8.setText(_translate("Dialog", "East"))

    def on_btn_extent(self, iface):
        """
        This will get the coordinates of the canvas extent, and then
        set the values to their widgets on the UI.
        """
        # Gets the coordinates of the extent
        crsDest = QgsCoordinateReferenceSystem(4326)  # WGS84
        crsSrc =self.iface.mapCanvas().mapSettings().destinationCrs()
        xform = QgsCoordinateTransform()
        xform.setSourceCrs(crsSrc)
        xform.setDestinationCrs(crsDest)
        extent = xform.transform(self.iface.mapCanvas().extent())

        # Sets the value to the individual widgets
        self.W_spinBox.setValue((math.floor(extent.xMinimum())))
        self.E_spinBox.setValue((math.ceil(extent.xMaximum())))
        self.S_spinBox.setValue((math.floor(extent.yMinimum())))
        self.N_spinBox.setValue((math.ceil(extent.yMaximum())))
        #print('set canvas')
    
        
    def get_values(self):   
        """
        Returns the values in the display boxes
        for the north, east, south, west bounds.
        """
        n = self.N_spinBox.value()
        e = self.E_spinBox.value()
        s = self.S_spinBox.value()
        w = self.W_spinBox.value()
        return n,e,s,w