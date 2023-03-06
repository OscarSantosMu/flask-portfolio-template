#!/bin/env bash

cd "${PROJECTPATH}" || exit
python3-virtualenv/bin/python -m unittest discover -v tests/