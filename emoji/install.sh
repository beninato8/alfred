#!/usr/bin/env bash

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 export_alfred.py

# Open the .alfredsnippets file to install it in Alfred
open emoji.alfredsnippets