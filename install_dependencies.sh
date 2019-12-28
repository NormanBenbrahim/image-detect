#!/bin/bash

curr_dir=`pwd`
env_python="env_python"
full_path="$curr_dir/$env_python"

if [ ! -d "$full_path" ]; then
  echo "Please run the command './setup_env.sh' first"
  echo "Then run the command 'source env_python/bin/activate'"
  echo ""
  exit
fi

if [ ! -z "${VIRTUAL_ENV}" ]; then
  pip install --upgrade pip
  pip install --upgrade gcloud
  pip install --upgrade google-cloud-storage
  pip install -r requirements.txt
else
  echo "Please type 'source env_python/bin/activate' before installing depencencies"
  exit
fi
