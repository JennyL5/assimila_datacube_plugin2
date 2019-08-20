# Assimila datacube plugin

I have created a QGIS Plugin to visualise Assimila's datacube. A data cube is used to represent data, it is a multi-dimensional ("n-D") array of values. I used the Plugin builder template to build the plugin. Quantum Geographic Information System is a free open-source cross-platform desktop application that supports viewing, editing, and analysis of geospatial data.  </b>

The user can enter the product, subproduct, time, north, east, south and west points into the plugin, and it will generate a raster file with the given parameters. </b>

## Getting Started

### Pre-requisites
* Python 3.7 (or any Python version 3 +)
* QGIS 3.8
* Qt Designer 5.13

### Installing

In order to install modules, open OSGeo4W shell, change to directory of plugin and run:

```
python -m ensurepip --default-pip 
py3_env
pip install numpy
pip install xarray # or xarray==0.10.4
pip install pyqt5-tools
pip install pb_tool
```

## Deployment

How to deploy this on a live system
To import pluging:
* Open QGIS, click 'Plugins' on the navigation bar and select 'Manage and install plugins'
* From the side bar, select 'Install from ZIP'
* Browse or copy and paste the zipped plugin folder
* Click 'Install Plugin' below
* After installation, select 'Installed' from the side bar, and check the plugin imported
* Click the plugin icon on the main page to run.

## Built With

* [QGIS in OSGeo4W Network Installer](https://qgis.org/en/site/forusers/download.html) - Plugin software
* [Qt Designer 5.13](https://doc.qt.io/qt-5/qtdesigner-manual.html) - Plugin's user interface
* [Qgis-Plugin-Builder](https://g-sherman.github.io/Qgis-Plugin-Builder/) - Plugin for building a plugin in QGIS

## Acknowledgments

* SRTM Downloader
* QGIS Plugin Builder 


