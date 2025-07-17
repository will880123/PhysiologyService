import uuid
from typing import List, Optional
from model.physiology_model import PhysiologyRecord
from repository.google_sheets_repo import GoogleSheetsRepository

class PhysiologyService:
    def __init__(self, repo: GoogleSheetsRepository):
        self.repo = repo

    def get_all_records(self) -> List[PhysiologyRecord]:
        return self.repo.get_all()

    def create_record(self, date: str, blood_pressure: str, blood_sugar: float) -> PhysiologyRecord:
        new_id = str(uuid.uuid4())
        record = PhysiologyRecord(id=new_id, date=date, blood_pressure=blood_pressure, blood_sugar=blood_sugar)
        self.repo.insert(record)
        return record

    def update_record(self, record_id: str, date: str, blood_pressure: str, blood_sugar: float) -> Optional[PhysiologyRecord]:
        record = self.repo.find_by_id(record_id)
        if not record:
            return None
        record.date = date
        record.blood_pressure = blood_pressure
        record.blood_sugar = blood_sugar
        updated = self.repo.update(record)
        if updated:
            return record
        else:
            return None

    def delete_record(self, record_id: str) -> bool:
        return self.repo.delete(record_id)

    def get_record_by_id(self, record_id: str) -> Optional[PhysiologyRecord]:
        return self.repo.find_by_id(record_id)
