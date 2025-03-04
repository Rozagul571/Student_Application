from pydantic import BaseModel, Field
from typing import List

class Student(BaseModel):
    id: int = Field(description="Unique identifier for the student")
    name: str = Field(min_length=2, max_length=50, description="Student's full name")
    email: str = Field(description="Student's email address")
    tests_taken: List[int] = Field(default_factory=list, description="List of test IDs taken by the student")

class Test(BaseModel):
    id: int = Field(description="Unique identifier for the test")
    name: str = Field(min_length=2, max_length=100, description="Name of the test")
    max_score: int = Field(gt=0, description="Maximum possible score for the test")

class TestResult(BaseModel):
    student_id: int = Field(description="ID of the student taking the test")
    test_id: int = Field(description="ID of the test taken")
    score: int = Field(ge=0, description="Score obtained in the test")

class ResponseMessage(BaseModel):
    message: str = Field(description="Response message")

class TestScoreStats(BaseModel):
    average_score: float = Field(description="Average score for the test")
    highest_score: int = Field(description="Highest score achieved in the test")
    max_possible_score: int = Field(description="Maximum possible score for the test")