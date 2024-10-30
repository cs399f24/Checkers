#!/bin/bash

#update and install necessary packages
sudo yum update -y

yum install -y git
git clone https://github.com/cs399f24/Checkers.git
cd Checkers
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
