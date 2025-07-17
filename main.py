from fastapi import FastAPI, APIRouter
import uvicorn
from controller.physiology_controller import router as physiology_router

app = FastAPI()

# API v1 router
api_v1_router = APIRouter(prefix="/api/v1")

# 掛載 physiology routes 到 /api/v1/records
api_v1_router.include_router(physiology_router, prefix="/records", tags=["Physiology Records"])

# 掛載 v1 router 到主應用
app.include_router(api_v1_router)

# 主程式啟動入口
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
