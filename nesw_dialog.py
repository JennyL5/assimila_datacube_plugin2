# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nesw_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!


from qgis.core import *
from qgis.PyQt import uic
from qgis.PyQt import QtNetwork
from qgis.PyQt.QtCore import pyqtSlot,  Qt,  QUrl,  QFileInfo
from qgis.PyQt.QtGui import QIntValidator
from qgis.PyQt.QtWidgets import *

from PyQt5 import QtCore, QtGui, QtWidgets
from qgis.PyQt.QtCore import pyqtSlot
import math,  os,  tempfile

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'nesw_dialog.ui'))

class Ui_NESW_Dialog(QDialog, FORM_CLASS):
    
    def setupUi(self, NESW_Dialog):
        NESW_Dialog.setObjectName("NESW_Dialog")
        NESW_Dialog.resize(546, 492)
        self.buttonBox = QtWidgets.QDialogButtonBox(NESW_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(160, 420, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.W_spinBox = QtWidgets.QDoubleSpinBox(NESW_Dialog)
        self.W_spinBox.setGeometry(QtCore.QRect(130, 250, 81, 41))
        self.W_spinBox.setMinimum(-180.0)
        self.W_spinBox.setMaximum(180.0)
        self.W_spinBox.setObjectName("W_spinBox")
        self.E_spinBox = QtWidgets.QDoubleSpinBox(NESW_Dialog)
        self.E_spinBox.setGeometry(QtCore.QRect(330, 250, 81, 41))
        self.E_spinBox.setMinimum(-180.0)
        self.E_spinBox.setMaximum(180.0)
        self.E_spinBox.setProperty("value", 10.0)
        self.E_spinBox.setObjectName("E_spinBox")
        self.N_spinBox = QtWidgets.QDoubleSpinBox(NESW_Dialog)
        self.N_spinBox.setGeometry(QtCore.QRect(230, 200, 81, 41))
        self.N_spinBox.setMinimum(-90.0)
        self.N_spinBox.setMaximum(90.0)
        self.N_spinBox.setProperty("value", 10.05)
        self.N_spinBox.setObjectName("N_spinBox")
        self.label_5 = QtWidgets.QLabel(NESW_Dialog)
        self.label_5.setGeometry(QtCore.QRect(230, 180, 91, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(NESW_Dialog)
        self.label_6.setGeometry(QtCore.QRect(240, 280, 91, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(NESW_Dialog)
        self.label_7.setGeometry(QtCore.QRect(130, 230, 91, 16))
        self.label_7.setObjectName("label_7")
        self.S_spinBox = QtWidgets.QDoubleSpinBox(NESW_Dialog)
        self.S_spinBox.setGeometry(QtCore.QRect(230, 300, 81, 41))
        self.S_spinBox.setMinimum(-90.0)
        self.S_spinBox.setMaximum(90.0)
        self.S_spinBox.setObjectName("S_spinBox")
        self.label_9 = QtWidgets.QLabel(NESW_Dialog)
        self.label_9.setGeometry(QtCore.QRect(60, 30, 401, 101))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(":/plugins/assimila_datacube/assimila_namelogo.png"))
        self.label_9.setScaledContents(True)
        self.label_9.setObjectName("label_9")
        self.Description = QtWidgets.QLabel(NESW_Dialog)
        self.Description.setGeometry(QtCore.QRect(170, 110, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Description.setFont(font)
        self.Description.setObjectName("Description")

        self.retranslateUi(NESW_Dialog)
        self.buttonBox.accepted.connect(NESW_Dialog.accept)
        self.buttonBox.rejected.connect(NESW_Dialog.reject)
        #self.buttonBox.accepted.connect(self.on_buttonBox_accepted)
        #self.buttonBox.rejected.connect(self.on_buttonBox_rejected)

        QtCore.QMetaObject.connectSlotsByName(NESW_Dialog)

    def retranslateUi(self, NESW_Dialog):
        _translate = QtCore.QCoreApplication.translate
        NESW_Dialog.setWindowTitle(_translate("NESW_Dialog", "Dialog"))
        self.label_5.setText(_translate("NESW_Dialog", "North"))
        self.label_6.setText(_translate("NESW_Dialog", "South"))
        self.label_7.setText(_translate("NESW_Dialog", "West"))
        self.Description.setText(_translate("NESW_Dialog", "A QGIS plugin to visualise a datacube"))
    
    
    def get_values(self):   

        n = self.N_spinBox.value()
        e = self.E_spinBox.value()
        s = self.S_spinBox.value()
        w = self.W_spinBox.value()
        return n,e,s,w
    
    if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        NESW_Dialog = QtWidgets.QDialog()
        ui = Ui_NESW_Dialog()
        ui.setupUi(NESW_Dialog)
        #NESW_Dialog.show()
        #Dialog_exec_()
        sys.exit(app.exec_())
