from typing import List

from fastapi import APIRouter, HTTPException
from models import TestResult, TestScoreStats
from database import students_db, tests_db, results_db
from statistics import mean

router = APIRouter()


@router.post("/", response_model=TestResult)
async def submit_result(result: TestResult):
    if result.student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    if result.test_id not in tests_db:
        raise HTTPException(status_code=404, detail="Test not found")
    if result.score > tests_db[result.test_id].max_score:
        raise HTTPException(status_code=400, detail="Score exceeds maximum possible score")

    results_db.append(result)
    students_db[result.student_id].tests_taken.append(result.test_id)
    return result


@router.get("/student/{student_id}/", response_model=List[TestResult])
async def get_student_results(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return [r for r in results_db if r.student_id == student_id]


@router.get("/test/{test_id}/", response_model=List[TestResult])
async def get_test_results(test_id: int):
    if test_id not in tests_db:
        raise HTTPException(status_code=404, detail="Test not found")
    return [r for r in results_db if r.test_id == test_id]


@router.get("/test/{test_id}/stats", response_model=TestScoreStats)
async def get_test_score_stats(test_id: int):
    if test_id not in tests_db:
        raise HTTPException(status_code=404, detail="Test not found")

    scores = [r.score for r in results_db if r.test_id == test_id]
    if not scores:
        raise HTTPException(status_code=404, detail="No results found for this test")

    return TestScoreStats(
        average_score=mean(scores),
        highest_score=max(scores),
        max_possible_score=tests_db[test_id].max_score
    )


@router.get("/test/{test_id}/highest", response_model=int)
async def get_highest_score(test_id: int):
    if test_id not in tests_db:
        raise HTTPException(status_code=404, detail="Test not found")
    scores = [r.score for r in results_db if r.test_id == test_id]
    if not scores:
        raise HTTPException(status_code=404, detail="No results found for this test")
    return max(scores)