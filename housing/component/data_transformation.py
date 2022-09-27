from housing.constant import CATEGORICAL_COLUMNS_KEY, DATASET_SCHEMA_COLUMNS_KEY, NUMERICAL_COLUMNS_KEY
from housing.exception import HousingException
from housing.logger import logging
from housing.entity.config_entity import DataTransformationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact
from housing.util.util import read_yaml_file, save_object, save_numpy_array_data, load_data
from housing.constant import *
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer 
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline

import os, sys
import numpy as np
import pandas as pd



# Columns from which additional features can be created

class FeatureGenerator(BaseEstimator,TransformerMixin):
    
    def __init__(self, add_bedrooms_per_room = True,
                total_rooms_ix = 3,
                total_bedrooms_ix = 4,
                population_ix = 5,
                households_ix = 6,columns = None):
        """
        FeatureGenerator Initialization
        add_bedrooms_per_room: bool
        total_rooms_ix: int index number of total rooms columns
        population_ix: int index number of total population columns
        households_ix: int index number of  households columns
        total_bedrooms_ix: int index number of bedrooms columns
        """

        try:
            self.columns = columns
            # assigning index from data.columns
            if self.columns is not None:
                total_rooms_ix = self.columns.index(COLUMN_TOTAL_ROOMS)
                total_bedrooms_ix = self.columns.index(COLUMN_TOTAL_BEDROOMS)
                households_ix = self.columns.index(COLUMN_HOUSEHOLD)
                population_ix = self.columns.index(COLUMN_POPULATION)

            self.add_bedrooms_per_room = add_bedrooms_per_room
            self.total_rooms_ix = total_rooms_ix
            self.total_bedrooms_ix = total_bedrooms_ix
            self.households_ix = households_ix
            self.population_ix = population_ix

        except Exception as e:
            raise e

    def fit(self, X, y = None):
        return self

    def transform(self,X, y = None):
        try:
            # Creating new columns 
            room_per_household = X[:, self.total_rooms_ix] / X[:, self.households_ix]
            population_per_household =  X[:, self.population_ix] / X[:, self.households_ix]

            # if add_bedroom_per_feature = True
            if self.add_bedrooms_per_room:
                bedroom_per_room = X[:, self.total_bedrooms_ix] / X[:, self.total_rooms_ix]

                generated_features = np.c_[X, bedroom_per_room, room_per_household, population_per_household]

            else: 
                generated_features = np.c_[X, room_per_household, population_per_household]

            return generated_features
            
        except Exception as e:
            raise e


class DataTransformation:

    def __init__(self, data_transformation_config = DataTransformationConfig,
                data_ingestion_artfact = DataIngestionArtifact,
                data_validation_artifact = DataValidationArtifact):
        
        try:
            logging.info(f"{'>'*20} Data Transformation Started {'<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artfact
            self.data_validation_artifact = data_validation_artifact

        except Exception as e:
            raise HousingException(e,sys) from e


    # to load data and to configure data through schema file
    @staticmethod
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

    # Preparing Data Transformation pickle object
    def get_data_transformer_object(self)->ColumnTransformer:
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path

            schema = read_yaml_file(schema_file_path)

            numerical_cols = schema[NUMERICAL_COLUMNS_KEY]
            categorical_cols = schema[CATEGORICAL_COLUMNS_KEY]
             
            # Numerical Feature Pipeline
            numerical_feature_pipeline = Pipeline(steps=[
            ('imputer',SimpleImputer(strategy='median')),
            ('feature_generator', FeatureGenerator(
                add_bedrooms_per_room= self.data_transformation_config.add_bedroom_per_room,
                columns=numerical_cols
            )),
            ('scaling', StandardScaler())])

            # Categorical Feature Pipeline
            categorical_feature_pipeline = Pipeline(steps=[
            ('imputer',SimpleImputer(strategy='most_frequent')),
            ('onehotencoder', OneHotEncoder()),
            ('scaling', StandardScaler(with_mean=False))])

            logging.info(f'Categorical Column : {categorical_cols}')
            logging.info(f'Numerical Column : {numerical_cols}')

            final_preprocessing = ColumnTransformer([
            ('numerical_feature_pipeline',numerical_feature_pipeline,numerical_cols),
            ('categorical_feature_pipeline',categorical_feature_pipeline,categorical_cols)])

            return final_preprocessing


        except Exception as e:
            raise HousingException(e,sys) from e

    def initialize_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info(f"Obtaining Preprocessing object")
            preprocessing_obj = self.get_data_transformer_object()

            logging.info(f"Obtaining Training and Testing file")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            logging.info(f"Fetching Schema File")
            schema_file_path = self.data_validation_artifact.schema_file_path


            # Loading the data with respect to the schema file
            logging.info(f"Loading the data with respect to the schema file")
            train_df = load_data(file_path=train_file_path, schema_file_path=schema_file_path)
            test_df = load_data(file_path=test_file_path, schema_file_path=schema_file_path)

            # Reading the schema file
            logging.info(f"Reading the schema file")
            schema = read_yaml_file(schema_file_path)

            #Target column name
            target_col = schema[TARGET_COLUMN_KEY]

            # Input and Target features for train data 
            logging.info(f"Splitting Input and Target features for train data ")
            input_feature_train_df = train_df.drop(columns=[target_col], axis=1)
            target_feature_train_df = train_df[target_col]

            # Input and Target features for train data 
            logging.info(f"Splitting Input and Target features for test data ")
            input_feature_test_df = test_df.drop(columns=[target_col], axis=1)
            target_feature_test_df = test_df[target_col]

            logging.info(f"Obtaining result array object for input test and train data")
            input_feature_train_arr =  preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr =  preprocessing_obj.transform(input_feature_test_df)

            logging.info(f"Concatinating the input array object and target array")
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace('.csv', '.npz')
            test_file_name = os.path.basename(test_file_path).replace('.csv', '.npz') 

            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)

            logging.info(f"Saving Numpy array for transformed train data in [{transformed_train_file_path}] and \
                        transformed test data in [{transformed_test_file_path}]")
            save_numpy_array_data(transformed_train_file_path,train_arr)
            save_numpy_array_data(transformed_test_file_path,test_arr)

            preprocessed_obj_file_path = self.data_transformation_config.preprocessed_file_object_path

            logging.info(f"Saving Preprocessing object in [{preprocessed_obj_file_path}]")
            save_object(file_path=preprocessed_obj_file_path, obj=preprocessing_obj)
            
            logging.info(f"Creating Data Transformation Artifact")
            data_transformation_artifact = DataTransformationArtifact(is_transformed = True,
                        message="Data Transformation Completed",
                        transformed_train_file_path = transformed_train_file_path,
                        transformed_test_file_path= transformed_test_file_path,
                        processed_object_file_path=preprocessed_obj_file_path
                        )
            logging.info(f"Data Transformation Artifact : {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise HousingException(e,sys) from e
