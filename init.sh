#/bin/bash

echo Start initial script

# install system packages
echo Install system packages

apt update -y && apt upgrade -y
apt install -y python3-venv

# set environment variables
echo Set environment variables

export $(cat .env | xargs)

# install python packages
echo Install python packages

python3 -m venv venv
venv/bin/python -m pip install --upgrade pip
venv/bin/python -m pip install -r requirements.txt

venv/bin/python bot/bot.py

echo Initial script finished