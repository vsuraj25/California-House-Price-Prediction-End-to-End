# This file be used to store hardcoded variables

import os 
from datetime import datetime

ROOT_DIR = os.getcwd()

CONFIG_DIR = 'config'
CONFIG_FILE_NAME = 'config.yaml'
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR, CONFIG_FILE_NAME)

CURRRNT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

# Training Pipeline related varibles
TRAINING_PIPELINE_CONFIG_KEY = 'training_pipeline_config'
TRAINING_PIPELINE_ARTIFACT_DIR = 'artifact_dir'
TRAINING_PIPELINE_NAME_KEY = 'pipeline_name'

# Data Ingestion related constants
DATA_INGESTION_CONFIG_KEY = 'data_ingestion_config'
DATA_INGESTION_ARTIFACT_DIR = 'data_ingestion'
DATA_INGESTION_DOWNLOAD_URL_KEY = 'dataset_download_url'
DATA_INGESTION_RAW_DATA_DIR_KEY = 'raw_data_dir'
DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY = 'tgz_download_dir'
DATA_INGESTION_DIR_NAME_KEY =  'ingested_dir'
DATA_INGESTION_TRAIN_DIR_KEY = 'ingested_train_dir'
DATA_INGESTION_TEST_DIR_KEY = 'ingested_test_dir'

#step2
# Data Validation related constants

DATA_VALIDATION_CONFIG_KEY = 'data_validation_config'
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = 'schema_file_name'
DATA_VALIDATION_SCHEMA_DIR_KEY = 'schema_dir'
DATA_VALDATION_ARTIFACT_DIR = 'data_validation'
DATA_VALIDATION_REPORT_FILE_NAME_KEY = 'report_file_name'
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY = 'report_page_file_name'

# Data validation check variables
DOMAIN_KEY = 'domain_value'
DOMAIN_COLUMN = 'ocean_proximity'
COLUMNS = 'columns'
TARGET_COLUMN = 'target_column'

# DATA Transformation related variables

DATA_TRANSFORMATION_ARTIFACT_DIR = 'data_transformation'
DATA_TRANSFORMATION_DIR_NAME_KEY = 'transformed_dir'
DATA_TRANSFORMATION_CONFIG_KEY =  'data_transformation_config'
DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY = 'transformed_train_dir'
DATA_TRANSFORMATION_TEST_DIR_NAME_KEY = 'transformed_test_dir'
DATA_TRANSFORMATION_PREPROCESSING_DIR_NAME_KEY = 'preprocessing_dir'
DATA_TRANSFORMATION_PREPROCESSING_FILE_NAME_KEY = 'preprocessed_object_file_name'
DATA_TRANSFORMATION_ADD_BEDROOM_PER_ROOM_KEY = 'add_bedroom_per_room'