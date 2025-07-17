from fastapi import APIRouter, HTTPException
from typing import List
from model.physiology_model import PhysiologyRequest, PhysiologyResponse
from service.physiology_service import PhysiologyService
from repository.google_sheets_repo import GoogleSheetsRepository
from dotenv import load_dotenv
import os

# 載入 .env 檔案
load_dotenv()

# 讀取環境變數
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")
CREDS_JSON_PATH = os.getenv("CREDS_JSON_PATH")

router = APIRouter()

# 初始化
repo = GoogleSheetsRepository(SPREADSHEET_ID, SHEET_NAME, CREDS_JSON_PATH)
service = PhysiologyService(repo)

@router.get("/", response_model=List[PhysiologyResponse])
def get_all_records():
    return service.get_all_records()

@router.get("/{record_id}", response_model=PhysiologyResponse)
def get_record(record_id: str):
    record = service.get_record_by_id(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.post("/", response_model=PhysiologyResponse)
def create_record(record_req: PhysiologyRequest):
    record = service.create_record(
        record_req.date,
        record_req.blood_pressure,
        record_req.blood_sugar
    )
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.put("/{record_id}", response_model=PhysiologyResponse)
def update_record(record_id: str, record_req: PhysiologyRequest):
    record = service.update_record(
        record_id, record_req.date,
        record_req.blood_pressure,
        record_req.blood_sugar
    )
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.delete("/{record_id}")
def delete_record(record_id: str):
    success = service.delete_record(record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"detail": "Record deleted"}
