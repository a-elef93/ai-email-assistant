from typing import Literal
from pydantic import BaseModel


class EmailAnalysis(BaseModel):
    category: Literal["order", "support", "other"]
    priority: Literal["high", "normal", "low"]
    reason: str