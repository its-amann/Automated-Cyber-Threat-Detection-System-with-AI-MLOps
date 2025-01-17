import os
import sys
import pandas as pd
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import load_object
from datetime import datetime
from networksecurity.constant.training_pipeline import PREDICTION_DIR
from networksecurity.constant.training_pipeline import FINAL_MODEL_DIR

print(PREDICTION_DIR)

def start_batch_prediction(input_file_path):
    try:
        # Ensure the prediction directory exists
        os.makedirs(PREDICTION_DIR, exist_ok=True)
        
        # Log the model loading process
        logging.info(f"Loading model and preprocessor from {FINAL_MODEL_DIR}")
        
        # Load the model and preprocessor from the final_model directory
        model_path = os.path.join(FINAL_MODEL_DIR, "model.pkl")  # Assuming your model is saved as model.pkl
        preprocessor_path = os.path.join(FINAL_MODEL_DIR, "preprocessor.pkl")  # Assuming your preprocessor is saved as preprocessor.pkl
        
        # Load the model and preprocessor (adjust if needed based on your saving process)
        model = load_object(file_path=model_path)
        preprocessor = load_object(file_path=preprocessor_path)
        
        # Initialize the NetworkModel with the loaded preprocessor and model
        network_model = NetworkModel(preprocessor=preprocessor, model=model)
        
        # Read the input data (CSV)
        logging.info(f"Reading input file: {input_file_path}")
        df = pd.read_csv(input_file_path)
        
        # Perform batch prediction
        logging.info("Performing batch prediction...")
        predictions = network_model.predict(df.values)  # Pass the data to our model for prediction
        
        # Add predictions to the dataframe
        df["prediction"] = predictions
        
        # Save the predictions to a new file
        prediction_file_name = os.path.basename(input_file_path).replace(".csv", f"_{datetime.now().strftime('%m%d%Y_%H%M%S')}.csv")
        prediction_file_path = os.path.join(PREDICTION_DIR, prediction_file_name)
        df.to_csv(prediction_file_path, index=False)
        
        logging.info(f"Predictions saved to {prediction_file_path}")
        
        return prediction_file_path
    except Exception as e:
        logging.error(f"Error in batch prediction: {str(e)}")
        raise NetworkSecurityException(e)