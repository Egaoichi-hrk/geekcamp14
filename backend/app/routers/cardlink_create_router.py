from fastapi import APIRouter, HTTPException, Depends,Header
from pydantic import BaseModel
from uuid import uuid4
from app.db.supabase import supabase
import jwt
from app.schemas.main_schema import CardCreate
import uuid

router = APIRouter()



# JWTからユーザーIDを取得
def get_current_user_id(authorization: str = Header(...)) -> str:
    try:
        # "Bearer <token>" の形式
        token = authorization.split(" ")[1]

        # トークンデコード（署名検証なしの簡易版）
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="ユーザーIDが取得できません")
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="認証エラー")
    

#プロフィール写真の追加
def upload_photo(user_id: str, file):
    file_name = f"{user_id}/{uuid.uuid4()}.jpg"
    res = supabase.storage.from_("card_photos").upload(file_name, file)
    if res.status_code == 200:
        url = supabase.storage.from_("card_photos").get_public_url(file_name)
        return url
    return None




# カード作成
@router.post("/cards_create")
async def create_card(card: CardCreate, user_id: str = Depends(get_current_user_id)):
    card_id = str(uuid4())
    data = {
        "card_id": card_id,
        "user_id": user_id,
        "name": card.name,
        "furigana": card.furigana,
        "photo_url": card.photo_url,
        "design_id": card.design_id,
        "design_name": card.design_name,
        "job": card.job,
        "student": card.student,
        "interest": card.interest,
        "goal": card.goal,
        "hobby": card.hobby,
        "qualification": card.qualification,
        "sns_link": card.sns_link,
        "free_text": card.free_text,
        "birthday": card.birthday,
    }
    
    result = supabase.table("cards").insert(data).execute()

    if result.data is None:
        raise HTTPException(status_code=500, detail="カードの作成に失敗しました")

    # 公開共有用URL
    share_url = f"https://yourapp.com/card/{card_id}"  

    return {
        "message": "カードを作成しました",
        "card_id": card_id,
        "share_url": share_url,
    }


# カード取得（全ユーザが閲覧可能）
@router.get("/cards/{card_id}")
async def get_card(card_id: str):
    result = supabase.table("cards").select("*").eq("card_id", card_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="カードが見つかりません")
    return result.data[0]



#カードの編集（ユーザのみ）
@router.put("/cards/{card_id}")
async def update_card(
    card_id: str,
    card: CardCreate,
    user_id: str = Depends(get_current_user_id)
):
    # 対象カードを検索
    result = (
        supabase.table("cards")
        .select("*")
        .eq("card_id", card_id)
        .eq("user_id", user_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=403, detail="Not authorized or card not found")

    # 更新処理
    update_data = {
        "name": card.name,
        "message": card.message,
        "image_url": card.image_url,
        "sns_link": card.sns_link,
    }

    supabase.table("cards").update(update_data).eq("card_id", card_id).execute()
    return {"message": "Card updated successfully"}


