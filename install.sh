#!/bin/bash

echo "Checking conda installation..."
which conda 2>&1 1>/dev/null
if [ "$?" != 0 ]; then
    echo "Conda seems to not be installed. Please install Miniconda, or conda package and try again"
    exit 1
fi
echo "done"

echo "Copying TyTan binary in /usr/local/bin/TyTan ..."
cp TyTan /usr/local/bin/TyTan
echo "done"

echo "Copying desktop information file in /usr/local/share/applications/tytant.desktop ..."
cp tytan.desktop /usr/local/share/applications/
echo "done"

echo "Analyzing if activate script exists on your system..."
wich activate 1>&2 2>/dev/null
if [ "$?" != 0 ]; then
    echo "activate conda script is not found, you're probably using Fedora conda package, I will put activate script in /usr/bin"
    cp activate /usr/bin/activate
fi
echo "done"

echo 
echo "You can now call TyTan from your desktop or through a terminal"

