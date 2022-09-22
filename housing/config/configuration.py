from logging import exception
import housing
from housing.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, \
     ModelEvaluationConfig, ModelPusherConfig, ModelTrainerConfig, TrainingPipelineConfig
from housing.util.util import read_yaml_file
from housing.constant import *
import os,sys
from housing.exception import HousingException
from housing.logger import logging

ROOT_DIR = os.getcwd() # to get current working directory

class Configuration:

    def __init__(self, config_file_path = CONFIG_FILE_PATH,
                      current_time_stamp:str = CURRRNT_TIME_STAMP) -> None:
        self.config_info = read_yaml_file(filepath = CONFIG_FILE_PATH)
        self.training_pipeline_config = self.get_training_pipeline_config()
        self.time_stamp = current_time_stamp

        


    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            # Creating dictionary for data ingestion info in artifact folder
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir = os.path.join(artifact_dir,
            DATA_INGESTION_ARTIFACT_DIR,
            self.time_stamp)

            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]

            dataset_download_url =data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]

            tgz_download_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY]
            )

            raw_data_dir =os.path.join(
                data_ingestion_artifact_dir, 
                data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )

            ingested_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_DIR_NAME_KEY]
                )

            train_dir =os.path.join(
                ingested_dir, 
                data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY]
            )


            test_dir = os.path.join(
                ingested_dir,
                data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY]
                )

            # Data ingestion config variable to initialize all the keys from DataIngestionConfig Entity
            data_ingestion_config = DataIngestionConfig(
                dataset_download_url = dataset_download_url,
                tgz_download_dir= tgz_download_dir,
                raw_data_dir= raw_data_dir,
                train_dir=train_dir,
                test_dir=test_dir
                )

            logging.info(f"Data Ingestion Config :{data_ingestion_config}")
            return data_ingestion_config
        except exception as e:
            raise HousingException(e, sys) from e


    def get_data_validation_config(self) -> DataValidationConfig:
        pass

    def get_data_transformation_config(self) -> DataTransformationConfig:
        pass

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        pass

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        pass

    def get_model_pusher_config(self) -> ModelPusherConfig:
        pass

    #1
    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            # getting training pipleine information from config.yaml using variables from constant.py 
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            # creating a path for artifact 
            artifact_dir = os.path.join(ROOT_DIR, 
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR])
            # This will Create 'c:\\Users\\User\\Machine-Learning-Project\\housing\\artifact'

            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)

            #logging
            logging.info(f"Training Pipeline Config: {training_pipeline_config}")
            return training_pipeline_config

        except Exception as e:
            raise HousingException(e, sys) from e


