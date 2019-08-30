# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search_dialog.ui'
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

from .DQTools.DQTools import Search, Dataset 
from .DQTools.DQTools.regions import get_bounds

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'search_dialog.ui'))

class Ui_search_Dialog(QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Ui_search_Dialog, self).__init__(parent)
        self.setupUi(self)
        #self.iface = iface
        #self.buttonBox.toggled.connect(self.on_btn_search_tile_clicked)

    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(549, 490)
        self.Description = QtWidgets.QLabel(Dialog)
        self.Description.setGeometry(QtCore.QRect(160, 120, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Description.setFont(font)
        self.Description.setObjectName("Description")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(50, 40, 401, 101))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(":/plugins/assimila_datacube/assimila_namelogo.png"))
        self.label_9.setScaledContents(True)
        self.label_9.setObjectName("label_9")
        self.N_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.N_spinBox.setGeometry(QtCore.QRect(240, 240, 81, 41))
        self.N_spinBox.setMinimum(-90.0)
        self.N_spinBox.setMaximum(90.0)
        self.N_spinBox.setProperty("value", 10.05)
        self.N_spinBox.setObjectName("N_spinBox")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(240, 220, 91, 16))
        self.label_5.setObjectName("label_5")
        self.W_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.W_spinBox.setGeometry(QtCore.QRect(140, 290, 81, 41))
        self.W_spinBox.setMinimum(-180.0)
        self.W_spinBox.setMaximum(180.0)
        self.W_spinBox.setObjectName("W_spinBox")
        self.S_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.S_spinBox.setGeometry(QtCore.QRect(240, 340, 81, 41))
        self.S_spinBox.setMinimum(-90.0)
        self.S_spinBox.setMaximum(90.0)
        self.S_spinBox.setObjectName("S_spinBox")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(150, 430, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(140, 270, 91, 16))
        self.label_7.setObjectName("label_7")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(250, 320, 91, 16))
        self.label_6.setObjectName("label_6")
        self.E_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.E_spinBox.setGeometry(QtCore.QRect(340, 290, 81, 41))
        self.E_spinBox.setMinimum(-180.0)
        self.E_spinBox.setMaximum(180.0)
        self.E_spinBox.setProperty("value", 10.0)
        self.E_spinBox.setObjectName("E_spinBox")
        self.search_tile = QgsFilterLineEdit(Dialog)
        self.search_tile.setGeometry(QtCore.QRect(170, 180, 181, 21))
        self.search_tile.setProperty("qgisRelation", "")
        self.search_tile.setObjectName("search_tile")
        self.btn_search_tile = QtWidgets.QPushButton(Dialog)
        self.btn_search_tile.setGeometry(QtCore.QRect(370, 180, 51, 31))
        self.btn_search_tile.setObjectName("btn_search_tile")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.search_tile.setText("Please enter a country e.g. Ghana")

        self.buttonBox.accepted.connect(self.on_buttonBox_accepted)
        self.buttonBox.rejected.connect(self.on_buttonBox_rejected)
        self.btn_search_tile.clicked.connect(self.on_btn_search_tile_clicked)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Description.setText(_translate("Dialog", "A QGIS plugin to visualise a datacube"))
        self.label_5.setText(_translate("Dialog", "North"))
        self.label_7.setText(_translate("Dialog", "West"))
        self.label_6.setText(_translate("Dialog", "South"))
        self.btn_search_tile.setText(_translate("Dialog", "Search"))
    

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
    
    def on_btn_search_tile_clicked(self):
        print("searching for tile...")
        print(self.search_tile.displayText())
         
        coordinates = self.find_tile()
        print(coordinates)
        self.add_coordinates_to_UI(coordinates)
   
 
    def find_tile(self):

        tile_name = self.search_tile.displayText()
        if tile_name=="":
            raise Exception("no tile name entered")
        elif tile_name:
            print("tile selected" + tile_name)
            bounds = get_bounds(tile_name.lower())._asdict()
            coordinates = list(bounds.values())
        else:
            raise Exception("Tile unavailable")

            
        return coordinates

       
    def add_coordinates_to_UI(self, coordinates):
        #get_bounds outputs a dictionary coordinates = [north, south, east, west]
        north=coordinates[0]
        east=coordinates[2]
        south=coordinates[1]
        west=coordinates[3]
        self.N_spinBox.setValue(north)
        self.E_spinBox.setValue(east)
        self.S_spinBox.setValue(south)
        self.W_spinBox.setValue(west)
    
        
    def get_values(self):   
        n = self.N_spinBox.value()
        e = self.E_spinBox.value()
        s = self.S_spinBox.value()
        w = self.W_spinBox.value()
        return n,e,s,w


from qgsfilterlineedit import QgsFilterLineEdit



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_search_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

