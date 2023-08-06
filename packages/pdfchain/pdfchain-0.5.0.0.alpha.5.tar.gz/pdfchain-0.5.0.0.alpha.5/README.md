PDF Chain
=========

A graphical user interface for the PDF Toolkit (PDFtk).
The GUI is intended to offer the functions of the command line program `pdftk` to all users in a easy way.

![Title Image](https://pdfchain.sourceforge.io/images/screenshots/0.5.0/pdfchain-menu.png)

PDF Chain generates a command for the PDF Toolkit from the GUI settings and executes it on the system.  Therefore the PDF Toolkit must be already installed on the system.

This version is a is a completely new implementation of PDF Chain in Python with a more modern interface design.

PDF Chain comes without any warranty!


Requires
--------

- Python3
    - Python-GObject


### External Dependency ###

- [PDF Toolkit](https://www.pdflabs.com/t/pdftk/)
    - [PDF Toolkit - Manual](https://www.pdflabs.com/docs/pdftk-man-page/)


Alternatively

- [PDFtk Java](https://gitlab.com/pdftk-java/pdftk)


Installation
------------

### Install/Update Required Tools ###

Tools for __installing__

- `pip`: The PyPA recommended tool for installing Python packages

```shell
$ pacman -S python-pip
$ apt install python3-pip
```


Tools for __packaging__

- `setuptools`: Easily download, build, install, upgrade, and uninstall Python packages
- `wheel`: A built-package format for Python

```shell
$ pacman -S python-setuptools python-wheel
$ apt install python3-setuptools python3-wheel
$ pip3 install --user --upgrade setuptools wheel
```


### Installing From PyPI.org Repository

```shell
$ pip3 install --user --upgrade pdfchain
$ pip3 uninstall pdfchain
```


### Packaging and Installing From Git Repository ###

```shell
$ git clone git://git.code.sf.net/p/pdfchain/neo pdfchain-neo
```

```shell
$ make dist
$ make install
$ make uninstall
$ make clean
```

Target directories

- Dist directory: `~/.local/lib/python3.x/site-packages/pdfchain/`
- Data directory: `~/.local/share/`
- Exec directory: `~/.local/bin/`


There is also a Arch Linux build script in the `scripts/AUR` directory.


Usage
-----

### Starting the Program ###

```shell
$ pdfchain
```

Command line options are not working yet!


### User Documentation ###

There is a [User Documentation](https://pdfchain.sourceforge.io/documentation.html) for the previous version.


---

[![Downloads](https://pepy.tech/badge/pdfchain)](https://pepy.tech/project/pdfchain)
