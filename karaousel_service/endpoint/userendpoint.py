from fastapi import APIRouter, Body, Request, status, HTTPException, Depends
from typing import List
from models.user import *
import service.userservice as users
from service.oauth2 import AuthJWT, require_user


router = APIRouter(prefix="/user",
    tags=["User"])
    

@router.get("/", response_description="List users", response_model=List[User])
def list_users(request: Request):
    user_list = users.list_users(100)
    return user_list

@router.post("/create", response_description="Create a new user", status_code=status.HTTP_201_CREATED)
def create_user(request: Request, user: User = Body(...)):  
    return users.create_user(user)

@router.get("/{id}", response_description="Get a single user by id")
def find_user(request: Request, id: int, user_id: str = Depends(require_user)):    
    return users.find_user(id)

@router.delete("/{id}", response_description="Delete a user")
def delete_user(request: Request, id:str):
    return users.delete_user(request, id)

@router.put("/update/{id}", response_description="Update a user", response_model=User)
def update_user(request: Request, id: int, user: UpdateUser):
    return users.update_user(request, id, user)

@router.post("/login", response_description="Authentication")
def login(request: Request, user: TokenRequest = Body(...), Authorize: AuthJWT = Depends()):   
    if user.email is None or user.password is None :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    else:    
        return users.authenticate(user, Authorize)