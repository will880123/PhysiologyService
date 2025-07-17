from dataclasses import dataclass

@dataclass
class PhysiologyRecord:
    id: str          # 唯一識別碼 (uuid)
    date: str        # 日期，例如 '2025-07-16'
    blood_pressure: str  # 血壓，例如 '120/80'
    blood_sugar: float   # 血糖，例如 5.6
