from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from service.physiology_service import PhysiologyService
from repository.google_sheets_repo import GoogleSheetsRepository
from config import SPREADSHEET_ID, SHEET_NAME, CREDS_JSON_PATH

app = FastAPI()

# 初始化 Repo & Service
repo = GoogleSheetsRepository(SPREADSHEET_ID, SHEET_NAME, CREDS_JSON_PATH)
service = PhysiologyService(repo)

# Pydantic 模型用於資料驗證
class PhysiologyRequest(BaseModel):
    date: str
    blood_pressure: str
    blood_sugar: float

class PhysiologyResponse(PhysiologyRequest):
    id: str

@app.get("/records", response_model=List[PhysiologyResponse])
def get_all_records():
    return service.get_all_records()

@app.get("/records/{record_id}", response_model=PhysiologyResponse)
def get_record(record_id: str):
    record = service.get_record_by_id(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@app.post("/records", response_model=PhysiologyResponse)
def create_record(record_req: PhysiologyRequest):
    record = service.create_record(record_req.date, record_req.blood_pressure, record_req.blood_sugar)
    return record

@app.put("/records/{record_id}", response_model=PhysiologyResponse)
def update_record(record_id: str, record_req: PhysiologyRequest):
    record = service.update_record(record_id, record_req.date, record_req.blood_pressure, record_req.blood_sugar)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@app.delete("/records/{record_id}")
def delete_record(record_id: str):
    success = service.delete_record(record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"detail": "Record deleted"}
