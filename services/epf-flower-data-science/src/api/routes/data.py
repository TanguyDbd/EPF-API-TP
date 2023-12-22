from fastapi import APIRouter
from src.services.data import download_dataset, load_dataset, process_dataset, split_dataset, train_dataset, predict, retreive_firestore, update_firestore

router = APIRouter()

@router.get("/download_data")
def download_dataset_router():
    return download_dataset()

@router.get("/load_data")
def load_data_router():
    return load_dataset()

@router.get("/process_data")
def process_data_router():
    return process_dataset()

@router.get("/split_data")
def split_dataset_router():
    return split_dataset()

@router.get("/train_data")
def train_dataset_router():
    return train_dataset()

@router.get("/predictions")
def predict_router():
    return predict()

@router.get("/retreive_firestone_params")
def retreive_firestone_router():
    return retreive_firestore()

@router.get("/update_firestone_params")
def update_firestone_router():
    return update_firestore()