#!/bin/bash

#update and install necessary packages
sudo yum update -y
yum install -y git

# Clones the repository and cd's into it
git clone https://github.com/cs399f24/Checkers.git && cd Checkers

# Creates the virtual environment and installs the requirements
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# # Source environment variables from .evn file
# if [-f .env]; then
#     export $(cat .env | xargs)
# fi

# Runs the app.py
python app.py
