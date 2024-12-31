from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl, validator
from bson import ObjectId, Binary

class PyObjectId(ObjectId):
    """Custom type for handling MongoDB ObjectId"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class AlumniProfile(BaseModel):
    """Alumni Profile Model - Represents the main profile document"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    fullName: str
    currentRole: str
    company: str
    university: str
    highSchool: str
    linkedInURL: HttpUrl
    alumniEmb: Optional[list] = None
    dateUpdated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration"""
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat(),
            HttpUrl: str
        }
        populate_by_name = True
        arbitrary_types_allowed = True

    def to_mongo(self):
        """Convert to MongoDB document format"""
        return {
            "_id": self.id,
            "fullName": self.fullName,
            "currentRole": self.currentRole,
            "company": self.company,
            "university": self.university,
            "highSchool": self.highSchool,
            "linkedInURL": str(self.linkedInURL),
            "alumniEmb": self.alumniEmb,
            "dateUpdated": self.dateUpdated
        }