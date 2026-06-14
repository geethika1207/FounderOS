from pydantic import BaseModel
from typing import List, Any
from datetime import datetime

class MessagesResponse(BaseModel):
    question : str
    answer : str

    class Config:
        orm_mode = True

class AnalysisResponse(BaseModel):
    developer_idea : str
    app_type : list
    core_features : list
    target_users : list
    db_design : dict
    end_points : Any
    risk_factors : Any
    roadmap : Any
    messages : List[MessagesResponse] = []

    class Config:
        orm_mode = True


class HistoryResponse(BaseModel):
    developer_idea: str
    app_type: list
    created_at: datetime
    message_count: int

    class Config:
        orm_mode = True