import re, os, sys, datetime, time
import pandas

# if data & logs folders don't exist, create them
if not os.path.exists('./data/'):
    os.makedirs('./data')

if not os.path.exists('./data/train-model/'):
    os.makedirs('./data/train-model')

if not os.path.exists('./data/logs/'):
    os.makedirs('./data/logs')

# initialize api key
# TODO: add to start.sh & start-local.sh
#gcs_creds = os.environ['GCS_DEVELOPER_KEY']
#gcs_project = os.environ['GCS_CX']



 
if __name__ == '__main__':
    print("main")