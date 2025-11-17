"""
Database Schemas for the Nonprofit Site

Each Pydantic model below represents one MongoDB collection. The collection
name will be the lowercase of the class name.

Examples:
- ContactMessage -> "contactmessage"
- VolunteerApplication -> "volunteerapplication"
- Program -> "program"
- Event -> "event"
- Subscriber -> "subscriber"
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List


class Program(BaseModel):
    title: str = Field(..., description="Program title, e.g., 'After‑School Coding Club'")
    summary: str = Field(..., description="Short description of the program")
    age_group: str = Field(..., description="Target ages, e.g., 'Ages 8–12'")
    topics: List[str] = Field(default_factory=list, description="Key topics covered")
    image: Optional[str] = Field(None, description="Public image URL")


class Event(BaseModel):
    title: str = Field(..., description="Event title")
    description: str = Field(..., description="What the event is about")
    date: str = Field(..., description="ISO date string or human readable date")
    location: str = Field(..., description="Event location or 'Online'")
    signup_url: Optional[str] = Field(None, description="External registration link if any")


class ContactMessage(BaseModel):
    name: str = Field(..., description="Sender name")
    email: EmailStr
    message: str = Field(..., min_length=5, description="Message body")
    subject: Optional[str] = Field(None, description="Optional subject line")


class VolunteerApplication(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    interests: List[str] = Field(default_factory=list, description="Areas of interest: mentoring, events, curriculum")
    notes: Optional[str] = None


class Subscriber(BaseModel):
    email: EmailStr
    name: Optional[str] = None
