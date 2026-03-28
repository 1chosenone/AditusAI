from pydantic import BaseModel, Field


class ParsedQuery(BaseModel):
    terms: list[str] = Field(description="List of optimized job search terms")
