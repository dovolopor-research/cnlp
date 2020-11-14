#!/usr/bin/env bash

pip uninstall cnlp -y

python setup.py clean
python setup.py install