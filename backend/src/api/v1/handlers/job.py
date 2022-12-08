from fastapi import APIRouter,Request,status,HTTPException,Depends
from fastapi.encoders import jsonable_encoder
from src.models.job import Job
from src.core.oauth2 import get_current_user
from typing import List
from uuid import UUID


job = APIRouter()

@job.get("/", response_description = "Get all jobs", response_model = List[Job], status_code = status.HTTP_200_OK)
async def get_all_jobs(request : Request,limit : int = 10, skip : int = 0, orderby : str = "created_at"):
    cursor = request.app.db.job.find({"$query":{}, "$orderby":{orderby:-1}}).skip(skip).limit(limit)
    jobs = [doc async for doc in cursor]

    return jobs

@job.get("/{id}", response_description = "Get job by id", response_model = Job, status_code = status.HTTP_200_OK)
async def get_job(id : str , request : Request, current_user = Depends(get_current_user)):
    job = await request.app.db.job.find_one({"_id":id})
    
    return job

@job.post("/", response_description = "Post a job", response_model = Job, status_code = status.HTTP_201_CREATED)
async def post_job(job : Job , request : Request, current_user = Depends(get_current_user)):
    job = jsonable_encoder(job)
    job["created_by"] = current_user["_id"]
    new_job = await request.app.db.job.insert_one(job)
    id = new_job.inserted_id
    created_job = await request.app.db.job.find_one({"_id":id})

    return created_job

@job.put("/{job_id}", response_description = "Update a job", response_model = Job, status_code = status.HTTP_200_OK)
async def update_job(job_id : UUID, job : Job , request : Request, current_user = Depends(get_current_user)):
    job = jsonable_encoder(job)
    
    job_exists = await request.app.db.job.find_one({"_id":job["_id"]})
    if not job_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Job doesn't exists.")
    elif(job["created_by"] != current_user["_id"]):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Request.")
    else:
        update_status = await request.app.db.job.update_one({"_id": job["_id"]}, {"$set": job})
        updated_job = await request.app.db.job.find_one({"_id": job["_id"]})
        return updated_job

@job.delete("/{id}", response_description = "Delete job by id", status_code = status.HTTP_200_OK)
async def delete_job(id : str , request : Request, current_user = Depends(get_current_user)):
    job = await request.app.db.job.find_one({"_id":id})
    job = jsonable_encoder(job)

    if(current_user["_id"] == job["created_by"]):
        delete_status = await request.app.db.job.delete_one({"_id":id})
        if(delete_status.deleted_count == 1):
            return 
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Couldn't be deleted.")
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Request.")