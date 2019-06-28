# TyTan - A JupyterLab Desktop app

JupyterLab is designed as a real IDE that is accessible from a "server" you have to launch, and needs a browser to open the UI.

TyTan is a simple Python 3 application that will:

- prepare conda environment with jupyter-lab installed + possibility to get other conda environments in Jupyter
- open the application inside a pure GTK UI, instead of using a browser

The main goal is to allow user to launch one application that will launch the service, and open the view, avoiding the usage of a browser.


## Installation

First, please, install Conda via package or using MiniConda.

Then:

- Download latest releas from https://github.com/metal3d/tytan/releases.
- Unpack the tarball and launch installation with `sudo`:

```
version='0.0.1'
tar zxf tytan-${version}.tgz
cd titan-${version}
sudo ./install.sh
```

You can uninstall with `sudo ./uninstall.sh`

The installation create a desktop icon and put binary in `/usr/local/bin`.

The binary is named "TyTan".

## Conda on Fedora

Conda on fedora needs "activate" script to make `nb_conda_kernels` to work properly. That's why the current installation script is putting it on `/usr/bin/activate`. If you're using Anaconda or Miniconda, you probably dont need that activation script. The install script detects if the file exists and do not overwrite it.
