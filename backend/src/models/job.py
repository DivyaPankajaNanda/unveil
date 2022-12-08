from pydantic import Field,BaseModel
from typing import List,Optional
from uuid import uuid4,UUID
from datetime import datetime

class Company(BaseModel):
    name : str
    address : str
    logo : str

class Job(BaseModel):
    id : UUID = Field(default_factory = uuid4, alias = "_id")
    title : str = Field(...)
    description : str = Field(...)
    company : Optional[Company]
    min_experience : Optional[str]
    job_location : str = Field(...)
    type : str = Field(...)
    skills :List[str] = Field(...)
    tags : Optional[List[str]]
    created_by : Optional[UUID]
    created_at: datetime = datetime.now()
    status : Optional[int] = 0

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example" : {
                "id" : "ad873efc-f559-4fb2-b546-283c4d9f8436",
                "title" : "Software Engineer",
                "description" : "This is a dummy job post.",
                "company" : {
                    "name" : "Unveil",
                    "address" : "India",
                    "logo" : "logo image url"
                },
                "min_experience" : "3-5 years",
                "job_location" : "Remote",
                "type" : "Full Time",
                "skills" : ["Python","Fastapi","MongoDb","Svelte"],
                "tags" : ["Senior","Remote","HR","Recruitment"],
                "status" : 0
            }
        }
