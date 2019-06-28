VERSION:=$(shell cat version.txt)

build: TyTan.spec $(wildcard *.py *.glade)
	pyinstaller TyTan.spec	

TyTan.spec:
	pyinstaller --add-data tytan-ui.glade:. --onefile TyTan

.PHONY: dist
dist: build
	cp tytan-ui.glade dist/
	cp activate install.sh uninstall.sh dist/
	cp -r dist tytan-$(VERSION)
	tar cfz tytan-$(VERSION).tgz tytan-$(VERSION)
	rm -rf tytan-$(VERSION)

.ONESHELL:
install:


