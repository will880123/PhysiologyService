from pydantic import BaseModel

# 輸入資料（不含 id）
class PhysiologyRequest(BaseModel):
    date: str
    blood_pressure: str
    blood_sugar: float

# 回傳資料（含 id）
class PhysiologyResponse(PhysiologyRequest):
    id: str
