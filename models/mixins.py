from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class TimeStampMixin(BaseModel):
    created: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={
            "onupdate": datetime.now(timezone.utc),
        },
    )
