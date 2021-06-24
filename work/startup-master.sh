#!/bin/bash

cd /home/jovyan/work
pip3 install --upgrade pip
pip3 install pyspark
python3 /home/jovyan/work/insert_data.py
chmod +x /master.sh && /master.sh
