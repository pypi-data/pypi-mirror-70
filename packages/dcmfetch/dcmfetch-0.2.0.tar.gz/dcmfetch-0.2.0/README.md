# DICOM Server Access

Dcmfetch is a python package for retrieving images from a [DICOM](http://medical.nema.org/) server. The package does not provide a DICOm trnasport itself but wraps either the command line utilies from  [dcm4che3](https://sourceforge.net/projects/dcm4che/files/dcm4che3/) or the native python library[pynetdicom](https://github.com/pydicom/pynetdicom). In addition, bundled standalone versions of the required dcm4che3 tools are included so the only mandatory external (non-python) dependency for the dcm4che3 option is a working java runtime. Further details on installation and use are available [here](docs/dcmfetch.md).

The DICOM server must support the dicom `c-find` and `c-get` protocols (not just `c-move`).
This is the case for the
[dcm4chee](https://sourceforge.net/projects/dcm4che/files/dcm4chee/) server, though several other common servers do not as yet support `c-get`. In addition though, `dcmfetch` supports access to servers such as [orthanc](http://www.orthanc-server.com/) using the `QIDO-RS` and `WADO-RS` web *REST* APIs instead.

DICOM servers are identified by keys in the configuration file `dcmnodes.cf`. This file encodes the server details (AET, most, port) together with a string representing facilities supported by the server (including the web API if available). This file is typically installed to the directory `/etc` on a unix system.

As well as the python package `dcmfetch` two utilities are provided: `dcmfetch` a command line program to retrieve series and `dcmfetchtool` a [PyQt](https://riverbankcomputing.com/software/pyqt/intro) based graphical tool.

## Licences

This package is made available under the [MIT](LICENCE) licence. The included dcm4che3 programs are distributed under the [Mozilla](https://github.com/dcm4che/dcm4che/blob/master/LICENSE.txt) public licence; the only modification here has been to bundle them into single executables.
 