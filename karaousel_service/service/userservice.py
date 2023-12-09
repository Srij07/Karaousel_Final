from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models.user import User,UpdateUser
from bson import ObjectId
from database import UserDoc

def get_collection_users():
  return UserDoc

def create_user(user: User = Body(...)):
    user = jsonable_encoder(user)
    new_user = get_collection_users().insert_one(user)
    created_user = get_collection_users().find_one({"_id": new_user.inserted_id})
    respose = {}
    respose['message'] = f"User successfully created with id {created_user['id']}"
    return respose
  
def list_users(limit: int):
    # users = get_collection_users(request)
    users = list(get_collection_users().find(limit = limit))
    for user_data in users:
        print (user_data["id"])
    return users
  
def find_user(id: int):
    if (user := get_collection_users().find_one({"id": id})):
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found!")
  
def delete_user(id: str):
    deleted_user = get_collection_users().delete_one({"_id": ObjectId(id)})

    if deleted_user.deleted_count == 1:
        return f"User with id {id} deleted sucessfully"

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found!")
  
def update_user(id: str, user: UpdateUser):
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        update_result = get_collection_users().update_one({"id": id}, {"$set": user})

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found!")

    if (existing_book := get_collection_users().find_one({"id": id})) is not None:
        return existing_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found!")