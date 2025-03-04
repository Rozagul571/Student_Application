from fastapi.testclient import TestClient
from main import app
from models import Student, Test, TestResult, ResponseMessage, TestScoreStats
from database import students_db, tests_db, results_db
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    students_db.clear()
    tests_db.clear()
    results_db.clear()
    students_db.update({
        1: Student(id=1, name="Nodirbekova", email="nodirbekova@gmail.com", tests_taken=[]),
        2: Student(id=2, name="Rozagul", email="Rozagul@gmail.com", tests_taken=[])
    })
    tests_db.update({
        101: Test(id=101, name="Math Quiz", max_score=100),
        102: Test(id=102, name="Science Exam", max_score=100)
    })
    results_db.extend([
        TestResult(student_id=1, test_id=101, score=85),
        TestResult(student_id=1, test_id=102, score=90),
        TestResult(student_id=2, test_id=101, score=70)
    ])


def test_create_student():
    new_student = {"id": 3, "name": "Robiya", "email": "Robiya@gmail.com", "tests_taken": []}
    response = client.post("/students/", json=new_student)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 3
    assert data["name"] == "Robiya"
    assert students_db[3].name == "Robiya"

def test_create_student_duplicate_id():
    new_student = {"id": 1, "name": "Surayyo", "email": "Surayyo@gmail.com", "tests_taken": []}
    response = client.post("/students/", json=new_student)
    assert response.status_code == 400
    assert response.json()["detail"] == "Student ID already exist"

def test_get_student():
    response = client.get("/students/1/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Nodirbekova"

def test_get_student_not_found():
    response = client.get("/students/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

def test_get_all_students():
    response = client.get("/students/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(student["id"] == 1 for student in data)

def test_delete_student():
    response = client.delete("/students/1/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Student deleted successfully"
    response = client.get("/students/1/")
    assert response.status_code == 404

def test_delete_student_not_found():
    response = client.delete("/students/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

def test_create_test():
    new_test = {"id": 103, "name": "History Exam", "max_score": 100}
    response = client.post("/tests/", json=new_test)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 103
    assert data["name"] == "History Exam"
    assert tests_db[103].name == "History Exam"

def test_create_test_duplicate_id():
    new_test = {"id": 101, "name": "Duplicate Quiz", "max_score": 100}
    response = client.post("/tests/", json=new_test)
    assert response.status_code == 400
    assert response.json()["detail"] == "Test ID already exists"

def test_get_test():
    response = client.get("/tests/101/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 101
    assert data["name"] == "Math Quiz"

def test_get_test_not_found():
    response = client.get("/tests/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Test not found"

def test_submit_result():
    new_result = {"student_id": 1, "test_id": 101, "score": 95}
    response = client.post("/results/", json=new_result)
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == 1
    assert data["score"] == 95
    assert len(results_db) == 4  # 3 + 1 yangi natijani olish un

def test_submit_result_exceed_max_score():
    new_result = {"student_id": 1, "test_id": 101, "score": 150}
    response = client.post("/results/", json=new_result)
    assert response.status_code == 400
    assert response.json()["detail"] == "Score exceeds maximum possible score"

def test_submit_result_invalid_student():
    new_result = {"student_id": 999, "test_id": 101, "score": 50}
    response = client.post("/results/", json=new_result)
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

def test_get_student_results():
    response = client.get("/results/student/1/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # 2dagu natija 85 90

def test_get_test_results():
    response = client.get("/results/test/101/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # 2li natija 85, 70

def test_get_test_stats():
    response = client.get("/results/test/101/stats")
    assert response.status_code == 200
    data = response.json()
    assert "average_score" in data
    assert "highest_score" in data
    assert "max_possible_score" in data
    assert data["average_score"] == 77.5  # (85 + 70) / 2
    assert data["highest_score"] == 85
    assert data["max_possible_score"] == 100

def test_get_highest_score():
    response = client.get("/results/test/101/highest")
    assert response.status_code == 200
    data = response.json()
    assert data == 85

def test_get_test_stats_no_results():
    response = client.get("/results/test/999/stats")
    assert response.status_code == 404
    assert response.json()["detail"] == "No results found for this test"