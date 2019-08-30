# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'canvas_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets

from qgis.core import *
from qgis.PyQt import uic
from qgis.PyQt import QtNetwork
from qgis.PyQt.QtCore import pyqtSlot,  Qt,  QUrl,  QFileInfo
from qgis.PyQt.QtGui import QIntValidator
from qgis.PyQt.QtWidgets import *

import math,  os,  tempfile

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'canvas_dialog.ui'))

class Ui_canvas_Dialog(QDialog, FORM_CLASS):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(545, 492)
        self.Description = QtWidgets.QLabel(Dialog)
        self.Description.setGeometry(QtCore.QRect(170, 120, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Description.setFont(font)
        self.Description.setObjectName("Description")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(60, 40, 401, 101))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(":/plugins/assimila_datacube/assimila_namelogo.png"))
        self.label_9.setScaledContents(True)
        self.label_9.setObjectName("label_9")
        self.btn_extent = QtWidgets.QPushButton(Dialog)
        self.btn_extent.setGeometry(QtCore.QRect(370, 320, 121, 31))
        self.btn_extent.setObjectName("btn_extent")
        self.N_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.N_spinBox.setGeometry(QtCore.QRect(150, 210, 81, 41))
        self.N_spinBox.setMinimum(-90.0)
        self.N_spinBox.setMaximum(90.0)
        self.N_spinBox.setProperty("value", 10.05)
        self.N_spinBox.setObjectName("N_spinBox")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(150, 190, 91, 16))
        self.label_5.setObjectName("label_5")
        self.W_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.W_spinBox.setGeometry(QtCore.QRect(50, 260, 81, 41))
        self.W_spinBox.setMinimum(-180.0)
        self.W_spinBox.setMaximum(180.0)
        self.W_spinBox.setObjectName("W_spinBox")
        self.S_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.S_spinBox.setGeometry(QtCore.QRect(150, 310, 81, 41))
        self.S_spinBox.setMinimum(-90.0)
        self.S_spinBox.setMaximum(90.0)
        self.S_spinBox.setObjectName("S_spinBox")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(160, 430, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(50, 240, 91, 16))
        self.label_7.setObjectName("label_7")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(160, 290, 91, 16))
        self.label_6.setObjectName("label_6")
        self.E_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.E_spinBox.setGeometry(QtCore.QRect(250, 260, 81, 41))
        self.E_spinBox.setMinimum(-180.0)
        self.E_spinBox.setMaximum(180.0)
        self.E_spinBox.setProperty("value", 10.0)
        self.E_spinBox.setObjectName("E_spinBox")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.buttonBox.accepted.connect(self.on_buttonBox_accepted)
        self.buttonBox.rejected.connect(self.on_buttonBox_rejected)
        self.btn_extent.clicked.connect(self.on_btn_extent)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Description.setText(_translate("Dialog", "A QGIS plugin to visualise a datacube"))
        self.btn_extent.setText(_translate("Dialog", "Set canvas extent"))
        self.label_5.setText(_translate("Dialog", "North"))
        self.label_7.setText(_translate("Dialog", "West"))
        self.label_6.setText(_translate("Dialog", "South"))

    @pyqtSlot()
    def on_buttonBox_accepted(self):
    
        north = self.N_spinBox.value()
        east = self.E_spinBox.value()
        south = self.S_spinBox.value()
        west = self.W_spinBox.value()
        print("north: %s east %s south: %s west %s" % (str(north), str(east), str(south), str(west)))
        self.accept()
        

    @pyqtSlot()
    def on_buttonBox_rejected(self):

        # TODO: not implemented yet
        self.reject()

    #@pyqtSlot()
    def on_btn_extent(self, iface):
        # Gets the coordinates of the extent
        crsDest = QgsCoordinateReferenceSystem(4326)  # WGS84
        crsSrc =iface.mapCanvas().mapSettings().destinationCrs()
        xform = QgsCoordinateTransform()
        xform.setSourceCrs(crsSrc)
        xform.setDestinationCrs(crsDest)
        extent = xform.transform(iface.mapCanvas().extent())

        # Sets the value to the individual widgets
        self.W_spinBox.setValue((math.floor(extent.xMinimum())))
        self.E_spinBox.setValue((math.ceil(extent.xMaximum())))
        self.S_spinBox.setValue((math.floor(extent.yMinimum())))
        self.N_spinBox.setValue((math.ceil(extent.yMaximum())))
        #print('set canvas')
    
        
    def get_values(self):   

        n = self.N_spinBox.value()
        e = self.E_spinBox.value()
        s = self.S_spinBox.value()
        w = self.W_spinBox.value()
        return n,e,s,w


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_canvas_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

