from src.schemas.message import MessageResponse
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import kaggle
import os
import json
from joblib import dump
from src.services.firestroreClient import FirestoreClient

def download_dataset():
    """Download the data"""
    kaggle.api.authenticate()
    dataset_name = "uciml/iris"
    save_dir = "services\epf-flower-data-science\src\data" 
    kaggle.api.dataset_download_files(dataset_name, path=save_dir, unzip=True)
    return MessageResponse(message="Dataset download !")

def load_dataset():
    """Load the data"""
    df = pd.read_csv("services/epf-flower-data-science/src/data/Iris.csv")
    return df.to_json(orient="records")

def process_dataset():
    """Process the data"""
    data = pd.read_json(load_dataset())
    data = data.drop("Id", axis=1)
    data['Species'] = data['Species'].map({'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2})
    return data.to_json(orient="records")

def split_dataset():
    """Split the data"""
    data = pd.read_json(process_dataset())
    train, test = train_test_split(data, test_size=0.2)
    return train.to_json(orient="records"), test.to_json(orient="records")

def train_dataset():
    """Store the model's parameters into src/config/model_parameters.json and train the data"""
    train_data = pd.read_json(split_dataset()[0])
    X_train = train_data.drop("Species", axis=1)
    y_train = train_data["Species"]
    model = LogisticRegression()

    # Save the model's parameters into src/config/model_parameters.json
    params = model.get_params()
    os.makedirs("services/epf-flower-data-science/src/config", exist_ok=True)
    params_path = "services/epf-flower-data-science/src/config/model_parameters.json"
    with open(params_path, "w") as f:
        json.dump(params, f)

    # Save the model in src/models folder
    os.makedirs("services/epf-flower-data-science/src/models/", exist_ok=True)
    model_path = os.path.join("services/epf-flower-data-science/src/models/model.joblib")
    dump(model, model_path)

    # Train the data
    model.fit(X_train, y_train)
    return MessageResponse(message="Model trained and saved"), model

def predict():
    """Make predictions form the trained model."""
    model = train_dataset()[1]
    test_data = pd.read_json(split_dataset()[1])
    X_test = test_data.drop("Species", axis=1)
    y_pred = pd.DataFrame(model.predict(X_test))
    return y_pred.to_json(orient="records")

def retreive_firestore():
    """Retreive parameters from Firestone"""
    client = FirestoreClient()
    params = client.get(collection_name="parameters", document_id="parameters")
    return params

def update_firestore():
    """Update and Add parameters on our Firestone database"""
    client = FirestoreClient()
    parameters_ref = client.client.collection("parameters").document("parameters")
    origin_params = client.get(collection_name="parameters", document_id="parameters")
    origin_params['n_estimators'] = 100
    origin_params['criterion'] = "gini"
    parameters_ref.set(origin_params)
    return origin_params