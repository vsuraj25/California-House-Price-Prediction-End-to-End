import yaml
import os, sys
from housing.exception import HousingException

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

