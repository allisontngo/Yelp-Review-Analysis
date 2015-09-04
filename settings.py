import os 

# Assume settings is in top level project directory
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

DATA_DIR = os.path.join(PROJECT_DIR,'yelp_dataset_challenge_academic_dataset')
DATA_DIR = os.path.abspath(DATA_DIR)

LOG_DIR = os.path.join(PROJECT_DIR, 'logging')
LOG_DIR = os.path.abspath(LOG_DIR)

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
