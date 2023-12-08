from fastapi import APIRouter, Body, Request, status
from typing import List
from app.models.user import User,UpdateUser
import app.service.userservice as users


router = APIRouter(prefix="/user",
    tags=["User"])
    

@router.get("/", response_description="List users", response_model=List[User])
def list_users(request: Request):
    user_list = users.list_users(request, 100)
    return user_list

@router.post("/create", response_description="Create a new user", status_code=status.HTTP_201_CREATED)
def create_user(request: Request, user: User = Body(...)):  
    return users.create_user(request,user)

@router.get("/{id}", response_description="Get a single user by id", response_model=User)
def find_user(request: Request, id: int):    
    return users.find_user(request, id)

@router.delete("/{id}", response_description="Delete a user")
def delete_user(request: Request, id:str):
    return users.delete_user(request, id)

@router.put("/update/{id}", response_description="Update a user", response_model=User)
def update_user(request: Request, id: int, user: UpdateUser):
    return users.update_user(request, id, user)