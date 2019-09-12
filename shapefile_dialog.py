# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shapefile_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.core import *
from qgis.core import QgsProject, Qgis, QgsPointXY, QgsGeometry, QgsPoint, \
    QgsVectorLayer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply,  \
    QNetworkAccessManager
from PyQt5.QtWidgets import *
from qgis.PyQt import uic
from PyQt5.QtWidgets import QFileDialog
import os.path
from os.path import expanduser
import numpy as np
import tempfile

class Ui_shapefile_Dialog(object):
    def setupUi(self, Dialog, iface):
        Dialog.setObjectName("Dialog")
        Dialog.resize(505, 530)
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(20, 30, 401, 101))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(":/plugins/assimila_datacube2/"
                                             "img/assimila_namelogo.png"))
        self.label_9.setScaledContents(True)
        self.label_9.setObjectName("label_9")
        self.S_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.S_spinBox.setGeometry(QtCore.QRect(200, 410, 81, 41))
        self.S_spinBox.setMinimum(-90.0)
        self.S_spinBox.setMaximum(90.0)
        self.S_spinBox.setObjectName("S_spinBox")
        self.Description = QtWidgets.QLabel(Dialog)
        self.Description.setGeometry(QtCore.QRect(130, 110, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Description.setFont(font)
        self.Description.setObjectName("Description")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(210, 390, 91, 16))
        self.label_6.setObjectName("label_6")
        self.N_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.N_spinBox.setGeometry(QtCore.QRect(200, 310, 81, 41))
        self.N_spinBox.setMinimum(-90.0)
        self.N_spinBox.setMaximum(90.0)
        self.N_spinBox.setProperty("value", 0.0)
        self.N_spinBox.setObjectName("N_spinBox")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(140, 470, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox
                                          .Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(200, 290, 91, 16))
        self.label_5.setObjectName("label_5")
        self.E_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.E_spinBox.setGeometry(QtCore.QRect(300, 360, 81, 41))
        self.E_spinBox.setMinimum(-180.0)
        self.E_spinBox.setMaximum(180.0)
        self.E_spinBox.setProperty("value", 0.0)
        self.E_spinBox.setObjectName("E_spinBox")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(100, 340, 91, 16))
        self.label_7.setObjectName("label_7")
        self.lineEdit = QgsFilterLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(100, 190, 271, 21))
        self.lineEdit.setProperty("qgisRelation", "")
        self.lineEdit.setObjectName("lineEdit")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(300, 340, 91, 16))
        self.label_8.setObjectName("label_8")
        self.W_spinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.W_spinBox.setGeometry(QtCore.QRect(100, 360, 81, 41))
        self.W_spinBox.setMinimum(-180.0)
        self.W_spinBox.setMaximum(180.0)
        self.W_spinBox.setObjectName("W_spinBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(100, 160, 351, 31))
        self.label.setObjectName("label")
        self.btn_browse_shapefile = QtWidgets.QToolButton(Dialog)
        self.btn_browse_shapefile.setGeometry(QtCore.QRect(380, 190, 31, 31))
        self.btn_browse_shapefile.setObjectName("btn_browse_shapefile")
        self.feature_comboBox = QtWidgets.QComboBox(Dialog)
        self.feature_comboBox.setGeometry(QtCore.QRect(210, 240, 171, 22))
        self.feature_comboBox.setObjectName("feature_comboBox")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(110, 230, 131, 31))
        self.label_2.setObjectName("label_2")

        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.btn_browse_shapefile.clicked.connect(self.on_btn_browse_shapefile_clicked)
        self.iface = iface
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Description.setText(_translate("Dialog", "A QGIS plugin to "
                                                      "visualise a datacube"))
        self.label_6.setText(_translate("Dialog", "South"))
        self.label_5.setText(_translate("Dialog", "North"))
        self.label_7.setText(_translate("Dialog", "West"))
        self.label_8.setText(_translate("Dialog", "East"))
        self.label.setText(_translate("Dialog", "Browse to import shape file."))
        self.btn_browse_shapefile.setText(_translate("Dialog", "..."))
        self.label_2.setText(_translate("Dialog", "Select feature:"))
    
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('AssimilaDatacCube', message)

    def on_btn_browse_shapefile_clicked(self, iface):
        """
        This is triggered when the shapefile browse button is clicked. This
        will allow the user to select location of directory of the shapefile.
        """
        # Gets directory for the keyfile - default: /users/{user_name}/Documents
        self.dir = QFileDialog.getOpenFileName(None,
                                               self.tr("Open File"),
                                                    # os.path.dirname(__file__),
                                               os.path.join(expanduser("~"),
                                                            "Documents"),
                                                            ("(*.shp)"))

        # Displays in lineEdit                             
        self.lineEdit.setText(self.dir.__getitem__(0))   

        # Open file to get features for the drop down menu
        import shapefile
        shape = shapefile.Reader(self.dir.__getitem__(0))

        shp = shape.__geo_interface__["features"]

        ID_list= []

        for pos, ch in enumerate(shape):
            #print(pos)
            #feature = shape.shapeRecords()

            #shp = shape.__geo_interface__["features"]
            ID = (shp[pos].__getitem__('properties').__getitem__('DeletionFlag'))
            ID_list.append(str(ID))
    
        # Adds ID list to combo box
        self.feature_comboBox.addItems(ID_list) 

        # Change boundaries everytime a new ID is selected
        self.feature_comboBox.currentTextChanged\
            .connect(lambda: self.ID_selectionchange(shape, shp, ID_list))
        
        # Adds the vector layer to QGIS
        self.iface.addVectorLayer(self.dir.__getitem__(0),
                                  "Vector Layer: ", "ogr")


    def ID_selectionchange(self,shape, shp, ID_list):
        """
        Updates the feature ID combo box to give a list of IDs
        of the selected feature from the shapefile.
        :return:
        """
        import shapefile

        shapes = shape.shapes()

        for pos, ch in enumerate(ID_list):
            if ID_list[pos] == self.feature_comboBox.currentText():
                #print("same pos")
                if shapes[pos].shapeType == shapefile.POLYGON:
                    #print (shape.bbox)  
                    # bbox (west, south, east, north)
                    north = shapes[pos].bbox[3]
                    east = shapes[pos].bbox[2]
                    south = shapes[pos].bbox[1]
                    west = shapes[pos].bbox[0] 
                    #print(north)
                    #print(east)
                    #print(south) 
                    #print(west)
                    self.N_spinBox.setValue(north)
                    self.E_spinBox.setValue(east)
                    self.S_spinBox.setValue(south)
                    self.W_spinBox.setValue(west)


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


from qgsfilterlineedit import QgsFilterLineEdit
