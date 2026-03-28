from pydantic import BaseModel, Field


class OptimizedQuery(BaseModel):
    terms: list[str] = Field(description="List of optimized job search terms")
