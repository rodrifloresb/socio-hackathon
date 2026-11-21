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

graph_vul:
	$(PYTHON) scripts/graph_vul.py

map_vul:
	.venv/bin/python scripts/map_vul.py

map_informalidad:
	.venv/bin/python scripts/map_informalidad.py

apilado:
	.venv/bin/python scripts/ind_vul_apilado.py

clean:
	rm -rf $(VENV)