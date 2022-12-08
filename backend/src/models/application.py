from pydantic import Field,BaseModel
from typing import Optional
from uuid import uuid4,UUID
from datetime import datetime

class Application(BaseModel):
    id : UUID = Field(default_factory = uuid4, alias = "_id")
    job_id : UUID = Field(...)
    applicant_id : UUID = Field(...)
    status : Optional[int] = 0
    created_at : datetime = datetime.now()
    comments : Optional[str]
    
    class Config:
        validate_assignment = True
        schema_extra = {
            "example" : {
                "job_id" : "ad873efc-f559-4fb2-b546-283c4d9f8436",
                "applicant_id" : "ad873efc-f559-4fb2-b546-283c4d9f8436",
            }
        }