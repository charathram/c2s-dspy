from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class CodeFileType(str, Enum):
    """
    Enumeration of code file classification types.
    """
    SCREEN = "Screen"
    DATA_MODEL = "Data_Model"
    API = "API"
    BUSINESS_LOGIC = "Business_Logic"
    DATABASE = "Database"
    PROGRAM_JOB_CONTROL = "JCL"


class CodeSummary(BaseModel):
    """
    Pydantic model to store a filename and its corresponding code summary.

    This model is designed to capture the essential information about a code file
    and its AI-generated summary for code-to-summary conversion tasks.
    """

    filename: str = Field(
        description="The name of the code file",
        min_length=1,
        examples=["main.py"]
    )

    filepath: str = Field(
        description="The full path for the code file",
        min_length=1,
        examples=["./directory/main.py"]
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

    classification: Optional[CodeFileType] = Field(
        default=None,
        description="Classification of the code file type",
        examples=[CodeFileType.SCREEN, CodeFileType.API]
    )

    suggested_classification: Optional[str] = Field(
        default=None,
        description="LLM-suggested classification of the code file type",
        examples=["Business Logic", "Data Model"]
    )

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }

    def __str__(self) -> str:
        classification_str = self.classification.value if self.classification else "None"
        suggested_classification_str = self.suggested_classification or "None"

        return (f"CodeSummary(\n"
                f"  filepath: {self.filepath}\n"
                f"  language: {self.language or 'Unknown'}\n"
                f"  classification: {classification_str}\n"
                f"  suggested_classification: {suggested_classification_str}\n"
                f"  confidence_score: {self.confidence_score}\n"
                f"  created_at: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"  summary: {self.summary}\n"
                f")")

    def __repr__(self) -> str:
        return self.__str__()
