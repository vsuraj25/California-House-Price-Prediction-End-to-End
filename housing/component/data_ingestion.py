from ctypes.wintypes import tagSIZE
from fileinput import filename
import re
from tkinter import E
from housing.entity.config_entity  import DataIngestionConfig
from housing.exception import HousingException
from housing.logger import logging
import os, sys
from housing.entity.artifact_entity import DataIngestionArtifact
import tarfile # to extract tgz file
from six.moves import urllib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit


class DataIngestion:

    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'*'*20} Data Ingestion log Started {'*'*20}" )
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def download_housing_data(self)-> str:

        # extracting remote url to download dataset
        download_url = self.data_ingestion_config.dataset_download_url   

        # folder location to download
        tgz_download_dir = self.data_ingestion_config.tgz_download_dir
        #Check whether tgz_download_dir is present or not, delete and recreate if present, create if not.
        if os.path.exists(tgz_download_dir):
            os.remove(tgz_download_dir)

        os.makedirs(tgz_download_dir,exist_ok=True)

        # Extracting file basername from the download url
        housing_file_name = os.path.basename(download_url)

        # complete file path of location to download tgz file
        tgz_file_path = os.path.join(tgz_download_dir, housing_file_name)

        #Download the file in tgz_file_path 
        logging.info(f"Downloading file from [{download_url}] into [{tgz_file_path}] ")
        urllib.request.urlretrieve(download_url, tgz_file_path)
        logging.info(f"File Downloaded from [{download_url}] into [{tgz_file_path}] ")

        return tgz_file_path
    
    def extract_tgz_file(self, tgz_file_path:str):
        try:
            # Creating a directory for saving the extracted data from tgz_file_path
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            os.makedirs(raw_data_dir,exist_ok=True)

            #Extracting the downloaded file from tgz_file_path into raw_data_dir
            logging.info(f"Extracting the tgz file from [{tgz_file_path} into dir : [{raw_data_dir}]]")
            with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
                housing_tgz_file_obj.extractall(path=raw_data_dir)


        except Exception as e:
            raise HousingException(e,sys) from e

    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            #Getting the raw data directory
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            # geting the file name of extracted dataset
            file_name = os.listdir(raw_data_dir)

            # Creating file path of to fetch extracted dataset
            housing_file_path = os.path.join(raw_data_dir, file_name)

            # Reading csv into dataframe
            logging.info(f"Reading raw data from {housing_file_path}")
            housing_dataframe = pd.read_csv(housing_file_path)

            # For creating same kind of distribution in both testing and training dataset
            logging.info(f"Creating income_cat column for stratified train test split")
            housing_dataframe["income_cat"] = pd.cut(
                housing_dataframe['median_income'],
                bins = [0, 1.5, 3.0, 4.5, 6.0, np.inf], ## for creating categories from median_income column
                labels=[1,2,3,4,5]
            )

            # Creating stratified train and test split
            strat_train_set = None
            strat_test_set = None
            logging.info(f"Performing StratifiedShuttleSplit for equal train and test split distribution")


            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
            
            for train_index, test_index in split.split(housing_dataframe, housing_dataframe["income_cat"]):
                ## For every split creating a training and testing split and dropping the "income_cat" column
                strat_train_set = housing_dataframe.loc[train_index].drop(["income_cat"], axis=1)
                strat_test_set = housing_dataframe.loc[test_index].drop(["income_cat"], axis=1)

            logging.info(f"Successfully created stratified train test split")

            ## Creating train and test file path
            train_file_path = os.path.join(self.data_ingestion_config.train_dir, file_name)
            test_file_path = os.path.join(self.data_ingestion_config.test_dir)

            ## Creating directories to save stratified train and test splits
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.train_dir, exist_ok=True)
                logging.info(f'Exporting Training Data to file : [{train_file_path}]')
                strat_train_set.to_csv(train_file_path, index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.test_dir, exist_ok=True)
                logging.info(f'Exporting Testing Data to file : [{test_file_path}]')
                strat_test_set.to_csv(test_file_path, index=False)


            logging.info(f"Saving DataIngestionArtifact")
            ## Saving the result object as Artifact
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                  test_file_path=test_file_path,
                                  is_ingested=True,
                                  message=f"Data Ingestion Completed Successfully!")
            logging.info(f"Data Ingestion Artifact : [{data_ingestion_artifact}] ")
            logging.info(f"Data Ingestion Completed!")
            return DataIngestionArtifact
            
        except Exception as e:
            raise HousingException(e,sys) from e

    def initialize_data_ingestion(self)->DataIngestionArtifact:
        try:
            # getting the path of downloaded dataset
            tgz_file_path = self.download_housing_data()

            # Extracting file from tgz_file_path and saving into raw_data_dir
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
 
            # Splitting raw data into train test split and returning it as an Artifact
            self.split_data_as_train_test()

        except Exception as e:
            raise HousingException(e,sys) from e

    ## final execution before destroying the program.
    def __del__():
        logging.info(f"{'*'*20} Data Ingestion Log Completed! {'*'*20}")
