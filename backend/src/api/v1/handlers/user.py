from fastapi import APIRouter,Request,status,HTTPException,Depends
from fastapi.encoders import jsonable_encoder
from src.models.user import UserOut,UserIn
from src.core.oauth2 import get_current_user
from typing import List
from uuid import UUID


user = APIRouter()

@user.get("/me", response_description = "Get current user", response_model = UserOut, status_code = status.HTTP_200_OK)
async def get_current_user_profile(request : Request, current_user = Depends(get_current_user)):
    user = await request.app.db.user.find_one({"_id":current_user["_id"]})
    
    return user

@user.get("/{id}", response_description = "Get user by id", response_model = UserOut, status_code = status.HTTP_200_OK)
async def get_user(id : str , request : Request, current_user = Depends(get_current_user)):
    user = await request.app.db.user.find_one({"_id":id})
    
    return user

@user.put("/{id}", response_description = "Update user profile", response_model = UserOut, status_code = status.HTTP_200_OK)
async def update_job(id : UUID, user : UserOut , request : Request, current_user = Depends(get_current_user)):
    user = jsonable_encoder(user)
    user_exists = await request.app.db.user.find_one({"_id":user["_id"]})
    
    if not user_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="User doesn't exists.")

    if (user["_id"] != current_user["_id"]):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Request.")

    modified_user = dict()
    modified_user["_id"] = user_exists["_id"]
    modified_user["name"] = user_exists["name"]
    modified_user["email"] = user_exists["email"]
    modified_user["username"] = user_exists["username"]
    modified_user["password"] = user_exists["password"]
    modified_user["links"] = user["links"]
    modified_user["projects"] = user["projects"]
    modified_user["blogs"] = user["blogs"]
    modified_user["education"] = user["education"]
    modified_user["experience"] = user["experience"]



    update_status = await request.app.db.user.update_one({"_id": user["_id"]}, {"$set": modified_user})
    updated_user = await request.app.db.user.find_one({"_id": user["_id"]})

    return updated_user

