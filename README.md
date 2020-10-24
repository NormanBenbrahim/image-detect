# Image Detection App

Repo for an image detection app that downloads images from google images based on keywords passed as command line arguments, and performs a fully convolutional neural network on those image classes using Tensorflow

Youtube Tutorial: [INSERT LINK WHEN CREATED]

# Setup

Type the following commands in your shell (you need Python 3.7+ and node 14.1+):

```
# Step 1: clone the repo 
git clone https://github.com/NormanBenbrahim/image-detect.git
cd image-detect

# Step 2: run the first script to create the virtual environment
python3 -m venv venv
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: start the virtual environment
source env_python/bin/activate

# Step 4: install node packages
cd image-extract
npm install
```

# Usage

**Always** make sure you're working in `venv` first. If you delete the `venv` folder just type the commands in steps 2-3 again