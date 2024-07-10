#!/bin/bash

rm -r .env

python3 -m pip install --upgrade pip

python3 -m venv .env

. .env/bin/activate

python3 -m pip --no-cache-dir install -r requirements.txt

deactivate

echo ""
echo "To activate the virtualenv and run the program, run:"
echo "    source .env/bin/activate"
echo ""
