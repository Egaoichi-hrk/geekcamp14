from fastapi import APIRouter, HTTPException, Depends,Header, UploadFile
from backend.app.core.config import settings
import qrcode
from fastapi.responses import StreamingResponse
from io import BytesIO


router = APIRouter()
"""
base_url=settings.BASE_URL
"""
@router.get("/cards/{card_id}/qrcode")
async def generate_qrcode(card_id: str):
    """カード閲覧ページのQRコードを生成して返す"""
    card_url = f"https://localhost:3000/cards/view/{card_id}"

    # === QRコード生成 ===
    qr = qrcode.make(card_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
