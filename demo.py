## This is the demo file to test pipelines

import sys
from logging import exception
from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging

def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        raise HousingException(e,sys) from e

if __name__ == "__main__":
    main()