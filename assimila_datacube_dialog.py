# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AssimilaDatacCubeDialog
                                 A QGIS plugin
 This plugin let's you visualise the datacube.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2019-08-07
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Assimila
        email                : jenny.lin@assimila.eu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import math,  os,  tempfile
from os.path import expanduser
from qgis.core import *
from qgis.PyQt import uic
from qgis.PyQt import QtNetwork
from qgis.PyQt.QtCore import pyqtSlot,  Qt,  QUrl,  QFileInfo
from qgis.PyQt.QtGui import QIntValidator
from qgis.PyQt.QtWidgets import *
from qgis.PyQt import QtWidgets
from qgis.core import QgsProcessingParameterString
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply,  QNetworkAccessManager
from qgis.core import *
from qgis.gui import QgsMapCanvas
from qgis.utils import iface

from .nesw_dialog import Ui_NESW_Dialog
from .canvas_dialog import Ui_canvas_Dialog
from .search_dialog import Ui_search_Dialog
from .shapefile_dialog import Ui_shapefile_Dialog

# This loads your .ui file so that PyQt can populate your plugin with the
# elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'assimila_datacube_dialog_base.ui'))


class AssimilaDatacCubeDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        super(AssimilaDatacCubeDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
    
    def add_coordinates_to_UI(self, coordinates):
        """
        This adds the north, east, south, west points to the widgets
        on the user interface.
        :param coordinates: A list with north, east, south, west bounds
        """
        # Extracting bounds from the coordinates list
        north=coordinates[0]
        east=coordinates[1]
        south=coordinates[2]
        west=coordinates[3]

        # Adds the north, east, south, west bounds into the display boxes
        self.N_spinBox.setValue(north)
        self.E_spinBox.setValue(east)
        self.S_spinBox.setValue(south)
        self.W_spinBox.setValue(west)
    
    @pyqtSlot()
    def on_btn_browse_keyfile_clicked(self):
        """
        This is triggered when the key file browse button is clicked.
        This will allow the user to select location of directory of the key file.
        """
        # Gets directory for the keyfile - default: /users/{user_name}/Documents
        self.keyfile = QFileDialog.getOpenFileName(None,
                                                   self.tr("Open File"),
                                                    # os.path.dirname(__file__),
                                                    os.path.join(expanduser("~"),
                                                                 "Documents"),
                                                    ("(*.assimila_dq)"))
        # Displays in lineEdit                             
        self.lineEdit.setText(self.keyfile.__getitem__(0))    


    @pyqtSlot()
    def on_btn_browse_rasterfile_clicked(self):
        """
        This is triggered when the save raster file browse button is clicked.
        This will allow the user to select location of directory where the
        raster file will save to.
        """
        # Gets default directory for the temporary raster file location
        self.dir = QFileDialog.getExistingDirectory(None,
                                                    self.tr("Open Directory"),
                                                    os.path.join(expanduser("~"),
                                                                 "Documents"),
                                                    QFileDialog.ShowDirsOnly 
                                                    | QFileDialog
                                                    .DontResolveSymlinks)

        # Displays in lineEdit
        self.lineEdit_2.setText(self.dir)
        