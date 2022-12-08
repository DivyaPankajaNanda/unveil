from fastapi import APIRouter
from src.api.v1.handlers.job import job
from src.api.v1.handlers.user import user
from src.api.v1.handlers.auth import auth
from src.api.v1.handlers.application import application

router = APIRouter()

router.include_router(auth,prefix="/auth",tags=["Authentication"])
router.include_router(job,prefix="/job",tags=["Job"])
router.include_router(user,prefix="/user",tags=["User"])
router.include_router(application,prefix="/application",tags=["Application"])


