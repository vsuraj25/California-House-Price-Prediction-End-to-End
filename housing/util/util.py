import yaml
import os, sys
import numpy as np
import dill
from housing.exception import HousingException
import numpy as np
import pandas as pd
from housing.constant import *

# Writing the information in the yaml file
def write_yaml_file(file_path:str,data:dict=None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise HousingException(e,sys)

# Reading the information from the yaml file
def read_yaml_file(filepath)-> dict:
    '''
    Reads yaml file and returns content of the yaml file as dictionary.
    '''

    try:
        with open(filepath, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e,sys) from e


def save_numpy_array_data(file_path: str, array : np.array):
    """
    Save numpy array into file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise HousingException(e,sys) from e

def load_numpy_array_data(file_path: str) -> np.array:
    """
    Loads array data from a fle
    file_path: str location where file object is located
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e

def save_object(file_path:str, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e

def load_object(file_path:str):
    try:
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e

# to load data and to configure data through schema file
def load_data(file_path : str, schema_file_path: str):
    try:
        # Reading dataset schema file
        dataset_schema = read_yaml_file(filepath=schema_file_path)

        schema = dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]

        dataframe = pd.read_csv(file_path)

        error_message = ''

        # Checking if dataset column names matches the schema columns
        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])
            else:
                error_message = f'Column : [{column}] is not present in schema'

        if len(error_message) > 0:
            raise Exception(error_message)

        return dataframe

    except Exception as e:
        raise HousingException(e,sys) from e


