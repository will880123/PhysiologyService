from fastapi import APIRouter, HTTPException
from typing import List
from model.physiology_model import PhysiologyRecord
from service.physiology_service import PhysiologyService
from repository.google_sheets_repo import GoogleSheetsRepository
from config import SPREADSHEET_ID, SHEET_NAME, CREDS_JSON_PATH

router = APIRouter()

# 初始化
repo = GoogleSheetsRepository(SPREADSHEET_ID, SHEET_NAME, CREDS_JSON_PATH)
service = PhysiologyService(repo)

@router.get("/", response_model=List[PhysiologyRecord])
def get_all_records():
    return service.get_all_records()

@router.get("/{record_id}", response_model=PhysiologyRecord)
def get_record(record_id: str):
    record = service.get_record_by_id(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.post("/", response_model=PhysiologyRecord)
def create_record(record_req: PhysiologyRecord):
    return service.create_record(record_req.date, record_req.blood_pressure, record_req.blood_sugar)

@router.put("/{record_id}", response_model=PhysiologyRecord)
def update_record(record_id: str, record_req: PhysiologyRecord):
    record = service.update_record(record_id, record_req.date, record_req.blood_pressure, record_req.blood_sugar)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.delete("/{record_id}")
def delete_record(record_id: str):
    success = service.delete_record(record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"detail": "Record deleted"}
