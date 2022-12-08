from fastapi import APIRouter,Request,status,HTTPException,Depends
from fastapi.encoders import jsonable_encoder
from src.models.application import Application
from src.core.oauth2 import get_current_user
from typing import List
from uuid import UUID


application = APIRouter()

@application.get("/user", response_description = "Get all user applications", response_model = List[Application], status_code = status.HTTP_200_OK)
async def get_all_user_applications(request : Request,limit : int = 10, skip : int = 0, orderby : str = "created_at", current_user = Depends(get_current_user)):
    cursor = request.app.db.application.find({"$query":{"applicant_id" : current_user["_id"]},"$orderby" : {orderby:-1}}).skip(skip).limit(limit)
    applications = [doc async for doc in cursor]

    return applications

@application.get("/job/{job_id}", response_description = "Get all applications for a job", response_model = List[Application], status_code = status.HTTP_200_OK)
async def get_all_job_applications(request : Request, job_id : str,limit : int = 10, skip : int = 0, orderby : str = "created_at", current_user = Depends(get_current_user)):
    cursor = request.app.db.application.find({"$query":{"job_id" : job_id},"$orderby" : {orderby:-1}}).skip(skip).limit(limit)
    applications = [doc async for doc in cursor]

    return applications

@application.get("/{id}", response_description = "Get application by id", response_model = Application, status_code = status.HTTP_200_OK)
async def get_application(id : str , request : Request, current_user = Depends(get_current_user)):
    application = await request.app.db.application.find_one({"_id":id})

    return application

@application.post("/", response_description = "Post an application", response_model = Application, status_code = status.HTTP_201_CREATED)
async def post_job(application : Application , request : Request, current_user = Depends(get_current_user)):
    application = jsonable_encoder(application)
    if (application["applicant_id"] != current_user["_id"]):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Forbidden application.")

    application_exists = await request.app.db.application.find_one({ "$and": [{"applicant_id":application["applicant_id"]},{"job_id":application["job_id"]}]})

    if not application_exists:
        new_application = await request.app.db.application.insert_one(application)
        id = new_application.inserted_id
        created_application = await request.app.db.application.find_one({"_id":id})
        return created_application
    else:
        raise HTTPException(status_code = status.HTTP_208_ALREADY_REPORTED, detail = "Already applied")


@application.put("/{application_id}", response_description = "Update application status", response_model = Application, status_code = status.HTTP_200_OK)
async def update_application(application_id : UUID, application : Application , request : Request, current_user = Depends(get_current_user)):
    application = jsonable_encoder(application)
    application_exists = await request.app.db.application.find_one({"_id":application["_id"]})

    applied_job = await request.app.db.job.find_one({"_id":application["job_id"]})
    applied_job = jsonable_encoder(applied_job)
    
    if not applied_job:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Job doesn't exists.")
    
    if not application_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Application doesn't exists.")
    
    if(application["applicant_id"] != current_user["_id"] and applied_job["created_by"] != current_user["_id"]):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Request.")
    
    update_status = await request.app.db.application.update_one({"_id": application["_id"]}, {"$set": application})
    updated_application = await request.app.db.application.find_one({"_id": application["_id"]})
    return updated_application


@application.delete("/{id}", response_description = "Delete application by id", status_code = status.HTTP_200_OK)
async def delete_application(id : str , request : Request, current_user = Depends(get_current_user)):
    application = await request.app.db.application.find_one({"_id":id})
    application = jsonable_encoder(application)

    if(current_user["_id"] == application["applicant_id"]):
        delete_status = await request.app.db.application.delete_one({"_id":id})
        if(delete_status.deleted_count == 1):
            return 
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Couldn't be deleted.")
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Request.")