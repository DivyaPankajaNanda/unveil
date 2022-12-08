from pydantic import Field,BaseModel,EmailStr
from uuid import uuid4,UUID
from typing import Optional,Union,List

class Link(BaseModel):
    name : str
    link : str

class Projects(BaseModel):
    name : str
    description : str
    authors : Optional[List[str]]
    repository_link : Optional[str]
    deployment_link : Optional[str]

class Blogs(BaseModel):
    title : str
    link : str

class Education(BaseModel):
    degree : str
    institution : str
    tenure : str
    grade : Optional[str]

class Experience(BaseModel):
    title : str
    organization : str
    tenure : str


class UserIn(BaseModel):
    id : UUID = Field(default_factory = uuid4, alias = "_id")
    name : str = Field(...)
    email : EmailStr = Field(...)
    username : str = Field(...)
    password : str = Field(...)
    links : Optional[List[Link]] | None = None
    projects : Optional[List[Projects]] | None = None
    blogs : Optional[List[Blogs]] | None = None
    education : Optional[List[Education]] | None = None
    experience : Optional[List[Experience]] | None = None

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example" : {
                "name" : "Divya Pankaja Nanda",
                "email" : "divya.pankaja.nanda@unveil.com",
                "password" : "password",
                "username" : "DivyaPankajaNanda",
                "links" : [
                    {
                        "name" : "github",
                        "link" : "https://github.com/DivyaPankajaNanda",
                    }
                ],
                "projects" : [
                    {
                        "name" : "Unveil",
                        "description" : "Platform that helps developers to unveil themselves to the world.",
                        "authors" : ["Divya Pankaja Nanda"],
                        "repository_link" : "to be updated",
                        "deployment_link" : "to be updated",
                    }
                ],
            }
        }

class UserOut(BaseModel):
    id : UUID = Field(default_factory = uuid4, alias = "_id")
    name : str 
    email : EmailStr 
    username : str 
    links : Optional[List[Link]] | None = None
    projects : Optional[List[Projects]] | None = None
    blogs : Optional[List[Blogs]] | None = None
    education : Optional[List[Education]] | None = None
    experience : Optional[List[Experience]] | None = None

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example" : {
                "id" : "9d915f41-1854-49b4-8cfc-6d5c01db6194",
                "name" : "John Doe",
                "email" : "jdoe@example.com",
                "username" : "jdoe",
                "links" : [
                    {
                        "name" : "github",
                        "link" : "https://github.com/DivyaPankajaNanda",
                    }
                ],
                "projects" : [
                    {
                        "name" : "Unveil",
                        "description" : "Platform that helps developers to unveil themselves to the world.",
                        "authors" : ["Divya Pankaja Nanda"],
                        "repository_link" : "to be updated",
                        "deployment_link" : "to be updated",
                    }
                ],
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str