from typing import List

from fastapi import APIRouter, HTTPException
from models import Test
from database import tests_db

router = APIRouter()

@router.post("/", response_model=Test)
async def create_test(test: Test):
    if test.id in tests_db:
        raise HTTPException(status_code=400, detail="Test ID already exists")
    tests_db[test.id] = test
    return test

@router.get("/{test_id}/", response_model=Test)
async def get_test(test_id: int):
    if test_id not in tests_db:
        raise HTTPException(status_code=404, detail="Test not found")
    return tests_db[test_id]

@router.get("/", response_model=List[Test])
async def get_all_tests():
    return list(tests_db.values())