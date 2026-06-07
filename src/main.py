import uvicorn
from fastapi import FastAPI

from api.v1.studentendpoints import router as student_router
from api.v1.authendpoints import router as user_router


app = FastAPI(docs_url="/api/docs",
              openapi_url="/api/openapi.json")

app.include_router(student_router, prefix="/api/v1/student", tags=["student"])
app.include_router(user_router, prefix="/api/v1/user", tags=["user"])

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)