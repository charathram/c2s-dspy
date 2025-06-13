from models import CodeSummary
from datetime import datetime
import json

def main():
    """
    Example usage of the CodeSummary Pydantic model.
    """

    # Create a simple code summary instance
    summary1 = CodeSummary(
        filename="main.py",
        summary="This Python script implements a main function that initializes the application and handles user input.",
        language="python",
        confidence_score=0.85
    )

    # Create another instance with minimal required fields
    summary2 = CodeSummary(
        filename="utils.js",
        summary="JavaScript utility functions for string manipulation and data validation."
    )

    # Create an instance with all fields
    summary3 = CodeSummary(
        filename="calculator.cpp",
        summary="C++ program that implements a basic calculator with arithmetic operations including addition, subtraction, multiplication, and division.",
        language="cpp",
        confidence_score=0.92,
        created_at=datetime.now()
    )

    print("=== CodeSummary Examples ===\n")

    # Display the summaries
    print("1. Python file summary:")
    print(f"   {summary1}")
    print(f"   Language: {summary1.language}")
    print(f"   Confidence: {summary1.confidence_score}")
    print(f"   Created: {summary1.created_at}")
    print()

    print("2. JavaScript file summary:")
    print(f"   {summary2}")
    print(f"   Language: {summary2.language}")
    print(f"   Confidence: {summary2.confidence_score}")
    print()

    print("3. C++ file summary:")
    print(f"   {summary3}")
    print(f"   Language: {summary3.language}")
    print(f"   Confidence: {summary3.confidence_score}")
    print()

    # Convert to JSON
    print("=== JSON Serialization ===\n")
    print("Summary 1 as JSON:")
    print(json.dumps(summary1.model_dump(), indent=2, default=str))
    print()

    # Create from dictionary
    print("=== Creating from Dictionary ===\n")
    data = {
        "filename": "database.py",
        "summary": "Python module containing database connection and CRUD operations for user management.",
        "language": "python",
        "confidence_score": 0.78
    }

    summary_from_dict = CodeSummary(**data)
    print(f"Created from dict: {summary_from_dict}")
    print()

    # Validation example
    print("=== Validation Examples ===\n")
    try:
        # This will fail due to empty filename
        invalid_summary = CodeSummary(filename="", summary="Some summary")
    except ValueError as e:
        print(f"Validation error for empty filename: {e}")

    try:
        # This will fail due to invalid confidence score
        invalid_summary = CodeSummary(
            filename="test.py",
            summary="Test summary",
            confidence_score=1.5  # Invalid: must be <= 1.0
        )
    except ValueError as e:
        print(f"Validation error for invalid confidence score: {e}")

if __name__ == "__main__":
    main()
