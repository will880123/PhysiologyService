import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Optional
from model.physiology_model import PhysiologyRecord


class GoogleSheetsRepository:
    def __init__(self, spreadsheet_id: str, sheet_name: str, creds_json_path: str):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json_path, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(spreadsheet_id).worksheet(sheet_name)

    def safe_float(self, value, default=0.0) -> float:
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    def get_all(self) -> List[PhysiologyRecord]:
        records = self.sheet.get_all_records()
        result = []

        for r in records:
            result.append(PhysiologyRecord(
                id=str(r.get('id') or "").strip(),
                date=str(r.get('date') or "").strip(),
                blood_pressure=str(r.get('blood_pressure') or "").strip(),
                blood_sugar=self.safe_float(r.get('blood_sugar'))
            ))

        return result

    def insert(self, record: PhysiologyRecord) -> None:
        self.sheet.append_row([
            record.id or "",
            record.date or "",
            record.blood_pressure or "",
            record.blood_sugar if record.blood_sugar is not None else 0.0
        ])

    def update(self, record: PhysiologyRecord) -> bool:
        all_records = self.sheet.get_all_records()
        for idx, r in enumerate(all_records, start=2):  # Row 1 = header
            if str(r.get('id', '')).strip() == record.id:
                self.sheet.update(f'A{idx}:D{idx}', [[
                    record.id or "",
                    record.date or "",
                    record.blood_pressure or "",
                    record.blood_sugar if record.blood_sugar is not None else 0.0
                ]])
                return True
        return False

    def delete(self, record_id: str) -> bool:
        all_records = self.sheet.get_all_records()
        for idx, r in enumerate(all_records, start=2):
            if str(r.get('id', '')).strip() == record_id:
                self.sheet.delete_row(idx)
                return True
        return False

    def find_by_id(self, record_id: str) -> Optional[PhysiologyRecord]:
        all_records = self.sheet.get_all_records()
        for r in all_records:
            if str(r.get('id', '')).strip() == record_id:
                return PhysiologyRecord(
                    id=str(r.get('id') or "").strip(),
                    date=str(r.get('date') or "").strip(),
                    blood_pressure=str(r.get('blood_pressure') or "").strip(),
                    blood_sugar=self.safe_float(r.get('blood_sugar'))
                )
        return None
