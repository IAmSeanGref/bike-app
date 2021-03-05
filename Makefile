PYTHON=python3
PIP=pip3

install: 
	$(PIP) install imutils opencv-python numpy image

run:
	$(PYTHON) main.py