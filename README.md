# Image Detection App

Repo for an image detection app built with Flask that makes use of the Vision API provided by Google, and hosted on Google Cloud Platform.

Youtube Tutorial: [INSERT LINK WHEN CREATED]

# First Time Usage

Make sure you have created a project in GCP, then

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstarts), create a new project on Google Cloud and enable the Cloud APIs. **Make sure you move the `cloud-sdk` folder to your home directory** before you install it with the `install.sh` script provided by Google

2. Follow [this guide](https://www.notion.so/normandatascience/Setup-Service-Account-For-Google-Vision-API-0972a21b2ce44630b7aee1466eb2b613) to setup a service account for Google Vision API 

3. Type the following commands in your shell


```
git clone https://github.com/NormanBenbrahim/image-detect.git

cd image-detect

# this makes the scripts executable
chmod u+x setup_env.sh
chmod u+x install_dependencies.sh

# run the first script to create the virtual environment
./setup_env.sh

# start the virtual environment
source env_python/bin/activate

# install dependencies inside the virtual environment
./install_dependencies.sh
```

4. Deploy the app using `gcloud app deploy`

# Usage Going Forward

Just make sure to not delete the `env_python` folder and run `source env_python/bin/activate` before working

If you delete the folder just type the commands in step 3 again