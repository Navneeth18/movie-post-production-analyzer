from pydantic import BaseModel, Field
from typing import Optional

class ArtistModel(BaseModel):
    """Database representation of an artist from the BOB dataset."""
    name: str = Field(..., alias="Name")
    role: str = Field(..., alias="Role")
    grade: str = Field(..., alias="Grade")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "Name": "S. S. Rajamouli",
                "Role": "Director",
                "Grade": "Grade 1"
            }
        }