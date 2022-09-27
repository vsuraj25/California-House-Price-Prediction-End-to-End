## This is the demo file to test pipelines

import sys
from logging import exception
from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging
from housing.config.configuration import Configuration
from housing.component.data_transformation import DataTransformation

def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
        # data_transformation_config = Configuration().get_data_transformation_config()
        # print(data_transformation_config)
        # schema_file_path = r'C:\Users\User\Machine-Learning-Project\config\schema.yaml'
        # train_file_path = r'C:\Users\User\Machine-Learning-Project\housing\artifact\data_ingestion\2022-09-25-01-07-32\ingested_data\test\housing.csv'

        # df = DataTransformation.load_data(train_file_path, schema_file_path)
        # print(df.columns)
        # print(df.dtypes)



    except Exception as e:
        raise HousingException(e,sys) from e

if __name__ == "__main__":
    main()