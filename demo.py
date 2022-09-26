## This is the demo file to test pipelines

import sys
from logging import exception
from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging
from housing.config.configuration import Configuration

def main():
    try:
        # pipeline = Pipeline()
        # pipeline.run_pipeline()
        data_transformation_config = Configuration().get_data_transformation_config()
        print(data_transformation_config)

    except Exception as e:
        raise HousingException(e,sys) from e

if __name__ == "__main__":
    main()