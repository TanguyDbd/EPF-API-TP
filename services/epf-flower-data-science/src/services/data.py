from fastapi import APIRouter
from src.schemas.message import MessageResponse
import pandas as pd
import kaggle

def download_dataset():
    """Download the data"""
    kaggle.api.authenticate()
    dataset_name = "uciml/iris"
    save_dir = "src\data" 
    kaggle.api.dataset_download_files(dataset_name, path=save_dir, unzip=True)
    return MessageResponse(message="Dataset download !")

def load_dataset():
    """Load the data"""
    df = pd.read_csv("src/data/Iris.csv")
    return df.to_json(orient="records")

def process_data():
    """Process the data"""
    data = pd.read_csv("src\data\Iris.csv")
    data = data.drop("Id", axis=1)
    data['Species'] = data['Species'].map({'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2})
    return data.to_json(orient="records")