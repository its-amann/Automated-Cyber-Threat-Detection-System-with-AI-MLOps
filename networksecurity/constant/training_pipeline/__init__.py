import os
import sys
import pandas as pd
import numpy as np

'''
TRAINING PIPELINE related constants
'''
FILE_NAME:str="phishingData.csv"
TARGET_COLUMN:str = "Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "Artifacts"
TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"


'''
DATA Ingestion retaled constants starts with 'DATA INGESTION' Var name
'''

DATA_INGESTION_COLLECTION_NAME:str = "NetworkData"
DATA_INGESTION_DATABASE_NAME:str = "NetworkSecurity"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR :str = "feature_store"
DATA_INGESTION_INGESTED_DIR :str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_FRACTION:float = 0.2
