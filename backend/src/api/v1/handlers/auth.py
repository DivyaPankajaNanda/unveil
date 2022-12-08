from fastapi import APIRouter,Request,HTTPException,status,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.models.user import UserIn,UserOut
from src.core.utility import get_password_hash,verify_password
from fastapi.security import OAuth2PasswordRequestForm
from src.core.oauth2 import create_access_token
from src.models.user import Token,TokenData


auth = APIRouter()

@auth.post("/signup", response_description = "Signup a user", response_model = UserOut, status_code = status.HTTP_201_CREATED)
async def signup(request : Request, user : UserIn):
    user = jsonable_encoder(user)

    email_exists = await request.app.db.user.find_one({"email":user["email"]})
    username_exists = await request.app.db.user.find_one({"username":user["username"]})
    
    if email_exists:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Email is already exists.")

    if username_exists:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Username is already taken.")

    user["password"] = get_password_hash(user["password"])

    new_user = await request.app.db.user.insert_one(user)
    created_user = await request.app.db.user.find_one({"email":user["email"]})

    return created_user

@auth.post("/signin", response_description = "Signin a user", response_model = Token, status_code = status.HTTP_200_OK)
async def signin(request : Request,credentials : OAuth2PasswordRequestForm = Depends()):
    
    user = await request.app.db.user.find_one({ "$or": [{"email":credentials.username},{"username":credentials.username}]})

    if user and verify_password(credentials.password,user["password"]):
        access_token = create_access_token({"username":user["username"]})
        return {"access_token":access_token,"token_type":"bearer"}
    else:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, details = "Invalid credentials")





