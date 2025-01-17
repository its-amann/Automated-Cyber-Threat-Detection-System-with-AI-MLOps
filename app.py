import os
import sys

import certifi
ca=certifi.where()

from dotenv import load_dotenv

load_dotenv()

mongo_db_url=os.getenv("MONGO_DB_URL")
print(mongo_db_url)

import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response, JSONResponse
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from networksecurity.constant.training_pipeline import UPLOAD_DIR, PREDICTION_BUCKET_NAME


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
       # Step 1: Save the uploaded file temporarily
        print("Reading uploaded CSV file...")
        df = pd.read_csv(file.file)
        print("CSV file loaded successfully.")

        # Step 2: Upload file to S3
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # Upload the file to S3 prediction bucket using AWS CLI sync
        upload_command = f"aws s3 sync {UPLOAD_DIR} s3://{PREDICTION_BUCKET_NAME}/input_files/"
        os.system(upload_command)
        print(f"File uploaded successfully to S3: {file.filename}")

        # print(df)
        preprocesor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        df['predicted_column'].replace(-1, 0)
        return df.to_json()
        # df.to_csv('prediction_output/output.csv')
        # table_html = df.to_html(classes='table table-striped')
        # #print(table_html)
        # return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise NetworkSecurityException(e,sys)
    
if __name__=="__main__":
    app_run(app,host="localhost",port=8000)

