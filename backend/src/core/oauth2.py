from jose import JOSEError, jwt,JWTError
from datetime import timedelta,datetime
from src.core.config import settings
from src.models.user import Token,TokenData
from fastapi import Depends,HTTPException,status,Request
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")

def create_access_token(payload : dict):
    to_encode = payload.copy()

    expiration_time = datetime.utcnow()+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expiration_time})

    jwt_token = jwt.encode(to_encode,settings.JWT_SECRET_KEY,algorithm=settings.ALGORITHM)

    return jwt_token

async def get_current_user(request : Request,token : str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Token could not be verified.",
        headers = {"WWW-AUTHENTICATE" : "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        current_username: str = payload.get("username")
        if current_username is None:
            raise credential_exception
        token_data = TokenData(username=current_username)
    except JWTError:
        raise credential_exception
    user = await request.app.db.user.find_one({"username":current_username})
    if user is None:
        raise credential_exception
    return user