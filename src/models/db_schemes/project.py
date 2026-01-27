from pydantic import BaseModel, ConfigDict,Field, field_validator
from typing import Optional
from bson import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId]=Field(None, alias="_id")
    project_id: str = Field(...,min_length=1)
    # description: str
    # is_active: bool


    @field_validator('project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
        return value
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )