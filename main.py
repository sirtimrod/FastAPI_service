import uvicorn
from fastapi import (
    APIRouter,
    FastAPI,
)
from api.handlers import user_router


app = FastAPI(title="study-service")

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
