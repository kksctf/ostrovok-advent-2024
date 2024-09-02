#!/usr/bin/env bash

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade build
python -m build
pip install --upgrade twine
python -m twine upload dist/* --repository-url http://localhost:8080 -u 1 -p 1
deactivate
