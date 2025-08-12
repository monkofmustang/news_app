from pydantic import BaseModel
from typing import Optional


class Subscribers(BaseModel):
    name: Optional[str] = None
    mobNumber: int
    state: Optional[str] = None

