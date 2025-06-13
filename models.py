from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CodeSummary(BaseModel):
    """
    Pydantic model to store a filename and its corresponding code summary.

    This model is designed to capture the essential information about a code file
    and its AI-generated summary for code-to-summary conversion tasks.
    """

    filename: str = Field(
        description="The name or path of the code file",
        min_length=1,
        examples=["main.py"]
    )

    summary: str = Field(
        description="AI-generated summary of the code content",
        min_length=1,
        examples=["This Python script implements a main function that initializes the application and handles user input."]
    )

    language: Optional[str] = Field(
        default=None,
        description="Programming language of the code file",
        examples=["python"]
    )

    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when the summary was created"
    )

    confidence_score: Optional[float] = Field(
        default=None,
        description="Confidence score of the summary (0.0 to 1.0)",
        ge=0.0,
        le=1.0
    )

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }

    def __str__(self) -> str:
        return f"CodeSummary(filename='{self.filename}', summary_length={len(self.summary)})"

    def __repr__(self) -> str:
        return self.__str__()
