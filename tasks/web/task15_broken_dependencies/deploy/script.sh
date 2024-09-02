#!/usr/bin/env bash

cd service

python -m venv venv
source venv/bin/activate
python -m pip install --index-url http://pypi:8080/simple/ -r requirements.txt --trusted-host pypi && python service.py
deactivate
rm -rf venv