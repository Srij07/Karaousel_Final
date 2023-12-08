from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.models.user import User,UpdateUser
from bson import ObjectId
from app.database import UserDoc

def get_collection_users(request: Request):
  # return UserDoc.find({},{"_id":0})
  return UserDoc

def create_user(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)
    new_user = get_collection_users(request).insert_one(user)
    created_user = get_collection_users(request).find_one({"_id": new_user.inserted_id})
    respose = {}
    respose['message'] = f"User successfully created with id {created_user['id']}"
    return respose
  
def list_users(request: Request, limit: int):
    # users = get_collection_users(request)
    users = list(get_collection_users(request).find(limit = limit))
    return users
  
def find_user(request: Request, id: int):
    if (user := get_collection_users(request).find_one({"id": id})):
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found!")
  
def delete_user(request: Request, id: str):
    deleted_user = get_collection_users(request).delete_one({"_id": ObjectId(id)})

    if deleted_user.deleted_count == 1:
        return f"User with id {id} deleted sucessfully"

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found!")
  
def update_user(request: Request, id: str, user: UpdateUser):
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        update_result = get_collection_users(request).update_one({"id": id}, {"$set": user})

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found!")

    if (existing_book := get_collection_users(request).find_one({"id": id})) is not None:
        return existing_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found!")