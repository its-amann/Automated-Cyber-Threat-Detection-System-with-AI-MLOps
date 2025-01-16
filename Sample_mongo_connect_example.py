from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import certifi
import os

# Load .env file
load_dotenv()

def connect_mongodb():
    try:
        # Get MongoDB URI from environment variable
        uri = os.getenv("MONGO_DB_URL")  # Changed to match .env file
        
        if uri is None:
            raise ValueError("MongoDB URI not found in environment variables")
            
        # Create client with SSL certificate
        client = MongoClient(
            uri,
            server_api=ServerApi('1'),
            tlsCAFile=certifi.where()
        )
        
        # Test connection
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        return None

if __name__ == "__main__":
    client = connect_mongodb()