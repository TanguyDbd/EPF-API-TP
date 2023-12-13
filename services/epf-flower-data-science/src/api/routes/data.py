from fastapi import APIRouter
from src.services.data import download_dataset, load_dataset, process_dataset, split_dataset

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