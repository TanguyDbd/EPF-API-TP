from src.schemas.message import MessageResponse
from sklearn.model_selection import train_test_split
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

def process_dataset():
    """Process the data"""
    data = pd.read_csv("src\data\Iris.csv")
    data = data.drop("Id", axis=1)
    data['Species'] = data['Species'].map({'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2})
    return data.to_json(orient="records")

def split_dataset():
    """Split the data"""
    data = pd.read_csv("src/data/Iris.csv")
    data = data.drop("Id", axis=1)
    data['Species'] = data['Species'].map({'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2})
    x_train, x_test, y_train, y_test = train_test_split(data.drop("Species", axis=1), data["Species"], test_size=0.2)
    train = pd.concat([x_train, y_train], axis=1)
    test = pd.concat([x_test, y_test], axis=1)
    train_json = train.to_json(orient="records")
    test_json = test.to_json(orient="records")
    train.to_csv("src/data/train.csv", index=False)
    test.to_csv("src/data/test.csv", index=False)
    return train_json, test_json