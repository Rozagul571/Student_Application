from fastapi import FastAPI
from routers import students, tests, results
app = FastAPI(
    title="Student Application Testing",
    description="A system to manage student tests and results",
    version="1.0.0"
)

app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(tests.router, prefix="/tests", tags=["Tests"])
app.include_router(results.router, prefix="/results", tags=["Results"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)