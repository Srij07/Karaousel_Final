from fastapi import APIRouter, Depends
from app.endpoint import userendpoint

router = APIRouter()


# @router.get('/me', response_model=schemas.UserResponse)
# def get_me(user_id: str = Depends(oauth2.require_user)):
#     user = userResponseEntity(User.find_one({'_id': ObjectId(str(user_id))}))
#     return {"status": "success", "user": user}


router.include_router(userendpoint.router)