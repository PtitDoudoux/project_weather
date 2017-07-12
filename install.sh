#!/usr/bin/env bash
pip3 install --user PyQt5 && pip3 install --user pytest;
pytest tests/;
pip3 setup.py install;