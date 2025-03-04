from typing import Dict, List
from models import Student, Test, TestResult

students_db: Dict[int, Student] = {
    1: Student(id=1, name="Nodirbekova", email="nodirbekova@gmail.com", tests_taken=[]),
    2: Student(id=2, name="Rozagul", email="Rozagul@gmail.com", tests_taken=[])
}

tests_db: Dict[int, Test] = {
    101: Test(id=101, name="Math Quiz", max_score=100),
    102: Test(id=102, name="Science Exam", max_score=100)
}

results_db: List[TestResult] = [
    TestResult(student_id=1, test_id=101, score=85),
    TestResult(student_id=1, test_id=102, score=90),
    TestResult(student_id=2, test_id=101, score=70)
]