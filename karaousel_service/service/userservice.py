from fastapi import Body, Request, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from models.user import *
from bson import ObjectId
from database import UserDoc
import hashlib
import utils
from service.oauth2 import AuthJWT
from config import settings
from datetime import datetime, timedelta

ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN

def get_collection_users():
  return UserDoc

def create_user(user: User = Body(...)):
    user = jsonable_encoder(user)
    user['password'] = hashlib.sha256(user['password'].encode()).hexdigest()
    new_user = get_collection_users().insert_one(user)
    created_user = get_collection_users().find_one({"_id": new_user.inserted_id})
    respose = {}
    respose['message'] = f"User successfully created with id {created_user['id']}"
    return respose
  
def list_users(limit: int):
    # users = get_collection_users(request)
    users = list(get_collection_users().find(limit = limit))
    return users
  
def find_user(id: int):
    if (user := get_collection_users().find_one({"id": id},{"_id":0,"password":0})):
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

def authenticate(user: TokenRequest = Body(...), Authorize: AuthJWT = Depends()):
    response = {}
    user = jsonable_encoder(user)
    # Check if the user exist
    db_user = get_collection_users().find_one({'email': user['email']})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email')
    # Check if the password is valid   
    user['password'] = hashlib.sha256(user['password'].encode()).hexdigest()
    
    if not utils.verify_password(db_user['password'], user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Password')
        
    access_token = Authorize.create_access_token(
        subject=str(user["email"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    
    # Create refresh token
    refresh_token = Authorize.create_refresh_token(
        subject=str(user["email"]), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))
    

    response["access_token"] = access_token
    response["refresh_token"] = refresh_token
    response["msg"] = "Success"
    return response
    