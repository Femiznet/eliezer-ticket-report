from typing import Optional, Any
from pydantic import BaseModel, Field, model_validator

class TicketModel(BaseModel):
    TicketOwner: str = ""
    TicketNo: str = Field(alias="ticketNumber")
    Subject: str = Field(alias="subject")
    Description: Optional[str] = Field(default=None, alias="description")
    CreatedTime: str = Field(alias="createdTime")
    ClosedTime: Optional[str] = Field(default=None, alias="closedTime")
    Status: str = Field(alias="status")
    Address: Optional[str] = None
    Location: Optional[str] = None
    RequestCoverage: Optional[str] = None
    RequestCategory: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def transform_data(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
            
        assignee = data.get('assignee') or {}
        first = assignee.get('firstName') or ''
        last = assignee.get('lastName') or ''
        data['TicketOwner'] = f"{first} {last}".strip()
        
        cf = data.get('customFields', {}) or {}
        data['Address'] = cf.get('Address')
        data['Location'] = cf.get('Location')
        data['RequestCoverage'] = cf.get('Request Coverage')
        data['RequestCategory'] = cf.get('Request Category')
        
        return data