# Assimila datacube plugin

I have created a QGIS Plugin to visualise Assimila's datacube. A data cube is used to represent data, it is a multi-dimensional ("n-D") array of values. I used the Plugin builder to build a template for the plugin. Quantum Geographic Information System is a free open-source cross-platform desktop application that supports viewing, editing, and analysis of geospatial data. I used the Plugin builder to build a template for the plugin. Quantum Geographic Information System is a free open-source cross-platform desktop application that supports viewing, editing, and analysis of geospatial data.

## Getting Started

### Pre-requisites
* Python 3.7 (or any Python version 3 +)
* QGIS 3.8
* Qt Designer 5.13

### Installing

A step by step series of examples that tell you how to get a development env running. </b>

In order to install relevant modules:

```
python -m ensurepip --default-pip 
py3_env
```

The modules required:

```
python -m pip install numpy
python -m pip install xarray==0.10.4
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
* [Qt Designer 5.13](https://doc.qt.io/qt-5/qtdesigner-manual.html) 
* [Qgis-Plugin-Builder](https://g-sherman.github.io/Qgis-Plugin-Builder/) - Plugin for building a plugin in QGIS

## Authors

* **Jenny Lin** - *Initial work* - [JennyL5](https://github.com/jennyl5)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* SRTM Downloader
* QGIS Plugin Builder 


