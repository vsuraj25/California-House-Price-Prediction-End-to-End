from tkinter.tix import COLUMN

from evidently import dashboard
from housing.constant import COLUMNS, DOMAIN_COLUMN, DOMAIN_KEY
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection 
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import os,sys
import pandas as pd
import numpy as np
import yaml
import json


class DataValidation():

    def __init__(self, data_validation_config:DataValidationConfig,
        data_ingestion_artifact :DataIngestionArtifact):  ## DataIngestionArtifact to retrieve results from Data Ingestion
        
        try:
            logging.info(f"{'>>'*20}Data Validation log started{'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_train_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            return train_df,test_df
        except Exception as e:
            raise HousingException(e,sys) from e

    ## To check if the train test file is available after Data Ingestion
    def check_train_test_file_exists(self)-> bool:
        
        try:
            logging.info("Checking if train and test file is available")
            is_train_file_exists = False
            is_test_file_exists = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exists = os.path.exists(train_file_path)
            is_test_file_exists = os.path.exists(test_file_path)
            
            is_available =  is_train_file_exists and is_test_file_exists
            logging.info(f"Train and Test split avalability : {is_available}")

            if not is_available:
                train_file_path = self.data_ingestion_artifact.train_file_path
                test_file_path = self.data_ingestion_artifact.test_file_path
                message = f"Training file : [{train_file_path}] and Testing file : [{test_file_path}] not available or not present"
                raise Exception(message)

            return is_available

        except Exception as e:
            raise HousingException(e,sys) from e
    
    ## To check if dataset is validated
    def validate_dataset_schema(self)->bool:
        try:
            validation_status = False

            # retrieving the train data as a dataframe
            train_df,_ = self.get_train_test_df()       
            # getting information from train data
            train_no_of_col = len(train_df.columns)  ## train data no of columns
            train_col_names = list(np.sort(train_df.columns))
            train_dom_values = list(np.sort(train_df[DOMAIN_COLUMN].unique()))

            # Fetching schema.yaml file
            schema_file_path = self.data_validation_config.schema_file_path

            with open(schema_file_path, 'r') as read_schema_file:
                schema_file = yaml.safe_load(read_schema_file)
            
            # Getting information from schema.yaml file
            schema_no_of_col = len(schema_file[COLUMNS].keys())
            schema_col_names = list(np.sort(list(schema_file[COLUMNS].keys())))
            schema_dom_values = []
            l_dom = [schema_dom_values.append(x) for i in schema_file[DOMAIN_KEY].values() for x in i]
            schema_dom_values = list(np.sort(schema_dom_values))
            
            # Checking data validation
            if train_col_names == schema_col_names and train_no_of_col == schema_no_of_col and train_dom_values == schema_dom_values:
                validation_status=True
                logging.info("Data Validation Successfull!")
            else:
                logging.info(f"Train col names - {train_col_names} : schema col names- {schema_col_names}"
                f"Train col length - {train_no_of_col} : schema col length- {schema_no_of_col}"
                f"Train domain values - {train_dom_values} : schema domain values - {schema_dom_values}")
                validation_status=  False

            return validation_status

        except Exception as e:
            raise HousingException(e,sys) from e

    def save_data_drift_report(self):
        try:

            profile = Profile(sections=[DataDriftProfileSection()]) ## creates a data drift report json

            # Retrieving train test dataframe from get_train_test_df()
            train_df, test_df = self.get_train_test_df()

            profile.calculate(train_df,test_df)
            profile.json()

            report = json.loads(profile.json()) # returning json as dict

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir, exist_ok=True)
            # Saving json file in report_file_path
            with open(report_file_path, 'w') as report_file:
                json.dump(report, report_file, indent=6)
 
            logging.info("Drift Report Saved.")
            return report

        except Exception as e:
            raise HousingException(e,sys) from e


    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df, test_df = self.get_train_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir, exist_ok=True)

            dashboard.save(report_page_file_path) #
            logging.info("Drift Report page file saved.")

        except Exception as e:
            raise HousingException(e,sys) from e


    def is_data_drift_present(self)-> bool:
        try:
            report = self.save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise HousingException(e,sys) from e

    

    # Initialize Data Validation
    def initiate_data_validation(self)-> DataValidationArtifact:
        try:

            self.check_train_test_file_exists()
            is_valid = self.validate_dataset_schema()
            self.is_data_drift_present()

            data_validation_artifact = DataValidationArtifact(schema_file_path=self.data_validation_config.schema_file_path,
                                        report_file_path= self.data_validation_config.report_file_path,
                                        report_page_file_path=self.data_validation_config.report_page_file_path,
                                        is_validated= is_valid,message="Data Validation Completed Successfully.")
            logging.info(f"Data Validation Artifact : {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e

    
    def __del__(self):
        logging.info(f"{'>>'*20}Data Valdaition log completed.{'<<'*20} \n\n")


