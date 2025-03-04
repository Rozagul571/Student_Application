from typing import List
from fastapi import APIRouter, HTTPException
from models import Student, ResponseMessage
from database import students_db, results_db

router = APIRouter()

@router.post("/", response_model=Student)
async def create_student(student: Student):
    if student.id in students_db:
        raise HTTPException(status_code=400, detail="Student ID already exists")
    students_db[student.id] = student
    return student

@router.get("/{student_id}/", response_model=Student)
async def get_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[student_id]

@router.get("/", response_model=List[Student])
async def get_all_students():
    return list(students_db.values())

@router.delete("/{student_id}/", response_model=ResponseMessage)
async def delete_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    del students_db[student_id]
    results_db[:] = [r for r in results_db if r.student_id != student_id]
    return {"message": "Student deleted successfully"}