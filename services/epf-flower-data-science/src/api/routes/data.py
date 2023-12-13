from fastapi import APIRouter
from src.services.data import download_dataset, load_dataset, process_data

router = APIRouter()

@router.get("/download_data")
def download_dataset_router():
    return download_dataset()

@router.get("/load_data")
def load_data_router():
    return load_dataset()

@router.get("/process_data")
def process_data_router():
    return process_data()