#!/bin/env bash

if [ "$1" == "Windows" ]; then
    # Windows
    VENV_PATH="python3-virtualenv/Scripts/python.exe"
else
    # Linux (default)
    VENV_PATH="python3-virtualenv/bin/python"
fi

cd "${PROJECTPATH}" || exit
"${VENV_PATH}" -m unittest discover -v tests/