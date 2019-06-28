#!/bin/bash

which conda 2>&1 1>/dev/null
if [ "$?" != 0 ]; then
    echo "Conda seems to not be installed. Please install Miniconda, or conda package and try again"
    exit 1
fi

cp TyTan /usr/local/bin/TyTan
cp tytan.desktop /usr/local/share/application/

wich activate 1>&2 2>/dev/null
if [ "$?" != 0 ]; then
    echo "activate conda script is not found, you're probably using Fedora conda package, I will put activate script in /usr/bin"
    cp activate /usr/bin/activate
fi

