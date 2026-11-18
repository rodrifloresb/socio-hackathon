VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

.PHONY: venv install dim1 dim2 dim3 clean

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install -r requirements.txt

dim1:
	$(PYTHON) scripts/ind_dim1.py

dim2:
	$(PYTHON) scripts/ind_dim2.py

dim3:
	$(PYTHON) scripts/ind_dim3.py

clean:
	rm -rf $(VENV)