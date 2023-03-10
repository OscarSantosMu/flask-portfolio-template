#!/bin/env bash

# cd into project folder
cd "${PROJECTPATH}" || exit
# Update code from GitHub repo
git fetch && git reset origin/main --hard
# Enter the python virtual environment and install python dependencies.
# python -m venv python3-virtualenv
# source python3-virtualenv/bin/activate
# pip install -r requirements.txt
# Spin containers down to prevent out of memory issues on our VPS
docker compose -f docker-compose.prod.yml down
# Spin up the containers
docker compose -f docker-compose.prod.yml up -d --build
# copy example.env to project folder as .env
cd ../
cp example.env "${PROJECTPATH}/.env"
# Restart service
# systemctl restart myportfolio