from pydantic import BaseModel

class RequestsAndDogsStatsResponse(BaseModel):
    new_requests_count: int
    total_dogs_count: int
