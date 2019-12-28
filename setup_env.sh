#!/bin/bash

curr_dir=`pwd`
env_python="env_python"
full_path="$curr_dir/$env_python"

if [ ! -d "$full_path" ]; then
  python3 -m venv env_python
fi
