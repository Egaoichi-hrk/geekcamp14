from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import auth_router
from backend.app.routers import cardlink_create_router
from backend.app.routers import qrcode_router
from backend.app.core.config import settings
 


app=FastAPI(title="Hackathon Backend API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # ここに許可するオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
app.include_router(cardlink_create_router.router, prefix="/api/cardlink",tags=["cardlink"])
app.include_router(qrcode_router.router, prefix="/api/qrcode",tags=["qrcode"])
#FastAPIのルーティングの仕方を調べろ！


#uvicorn main:app --reload    で起動