#!/bin/bash

# bash dependencies for mac
brew install mysql
export PATH=$PATH:/usr/local/mysql/bin

curr_dir=`pwd`
venv="venv"
full_path="$curr_dir/$venv"

if [ ! -d "$full_path" ]; then
  python3 -m venv venv
  echo "Please run the following command if working in your local environment: source venv/bin/activate'"
  echo ""
  exit
fi

# ensure working ina virtual env
if [ ! -z "${VIRTUAL_ENV}" ]; then
  echo "Downloading dependencies"
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "Please type 'source venv/bin/activate' first"
  exit
fi

# ensure google cloud credentials are available
if [ -z "$GOOGLE_CLOUD_CREDENTIALS" ]
then 
  "Visit rapidapi.com and get the API key, then add this line to your bashrc/bash_profile file:"
  "export GOOGLE_CLOUD_CREDENTIALS='<insert key here>'"
else 
  continue 
fi 

# run the file
python main.py