#!/bin/bash

curr_dir=`pwd`
venv="venv"
full_path="$curr_dir/$venv"

if [ ! -d "$full_path" ]; then
  python3 -m venv venv
  echo "Please run the following command if working in your local environment: source venv/bin/activate'"
  echo ""
  exit
fi

echo "Downloading dependencies"
pip install --upgrade

if [ ! -z "${VIRTUAL_ENV}" ]; then
  pip install --upgrade pip
  pip install --upgrade gcloud
  pip install --upgrade google-cloud-storage
  pip install -r requirements.txt
else
  echo "Please type 'source venv/bin/activate' before installing depencencies"
  exit
fi
