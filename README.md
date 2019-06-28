# TyTan - A JupyterLab Desktop app

JupyterLab is designed as a real IDE that is accessible from a "server" you have to launch, and needs a browser to open the UI.

TyTan is a simple Python 3 application that will:

- prepare conda environment with jupyter-lab installed + possibility to get other conda environments in Jupyter
- open the application inside a pure GTK UI, instead of using a browser

The main goal is to allow user to launch one application that will launch the service, and open the view, avoiding the usage of a browser.

## Requirements

You need to install:

- Python3
- Conda (package or MiniConda)
- webkit2gtk3

Actually, you need to have python Gtk, WebKit2 and Glib that came with `python gi` module. To check if it's ok:
```
$ python3
>>> import gi
>>> from gi.repository import Gtk, WebKit2, GLib
__main__:1: PyGIWarning: Gtk was imported without specifying a version first. Use gi.require_version('Gtk', '3.0') before import to ensure that the right version gets loaded.
__main__:1: PyGIWarning: WebKit2 was imported without specifying a version first. Use gi.require_version('WebKit2', '4.0') before import to ensure that the right version gets loaded.
>>> 
Press CTRL+D to quit
```

**You can ignore PyGIWarning. The most important is to not have any `ImportError`**.


## Installation

TODO: make a real application setup

At this time:

- download the release or git clone the repository
- make a symlink from "TyTan" to `~/.local/bin/TyTan` or `/usr/local/bin/TyTan`:
```
ln -s path/to/TyTan ~/.local/bin/TyTan
```

Put the `tytan.desktop` file in `~/.local/share/applications/`
