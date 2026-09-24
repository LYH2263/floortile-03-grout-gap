from pydantic import BaseModel, Field


class SettingsUpdate(BaseModel):
    gap_mm: float = Field(ge=0)
