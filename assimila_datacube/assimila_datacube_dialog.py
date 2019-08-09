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

import os, tempfile

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'assimila_datacube_dialog.ui'))


class AssimilaDatacCubeDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(AssimilaDatacCubeDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.dir = tempfile.gettempdir()



    @pyqtSlot()
    def on_btn_extent_clicked(self):
        """
        Slot documentation goes here.
        """
        crsDest = QgsCoordinateReferenceSystem(4326)  # WGS84
        crsSrc =self.iface.mapCanvas().mapSettings().destinationCrs()
        xform = QgsCoordinateTransform()
        xform.setSourceCrs(crsSrc)
        xform.setDestinationCrs(crsDest)
            
        extent = xform.transform(self.iface.mapCanvas().extent())        

        self.lne_west.setText(str(int(math.floor(extent.xMinimum()))))
        self.lne_east.setText(str(math.ceil(extent.xMaximum())))
        self.lne_south.setText(str(int(math.floor(extent.yMinimum()))))
        self.lne_north.setText(str(math.ceil(extent.yMaximum())))
        print('set canvas')


    def coordinates_valid(self,  text):
        
        if self.lne_west.text() != '' and self.lne_east.text() != '' and self.lne_south.text() != '' and self.lne_north.text() != '':
            self.btn_download.setEnabled(True)
        else:
            self.btn_download.setEnabled(False)
    
    @pyqtSlot()
    def on_btn_browse_keyfile_clicked(self):
        print('get directory')
        from os.path import expanduser
        home = expanduser("~")
        self.dir = QFileDialog.getExistingDirectory(None, self.tr("Open Directory"),
                                                    "/Users/Jenny/Downloads",
                                                    QFileDialog.ShowDirsOnly 
                                                    | QFileDialog.DontResolveSymlinks)

        self.lineEdit.setText(self.dir)   