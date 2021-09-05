#!/bin/bash

python -m venv env
source ./env/bin/activate
pip install -r requirements.txt
python ./main.py -f ~/CubeSat-ADCS-Software/build/com2
read -n 1
