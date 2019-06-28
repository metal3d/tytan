build: TyTan.spec $(wildcard *.py *.glade)
	pyinstaller TyTan.spec	

TyTan.spec:
	pyinstaller --add-data tytan-ui.glade:. --onefile TyTan
