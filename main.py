from fastapi import FastAPI, status, HTTPException, Request
import time
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"])

async def log_middleware(request: Request, call_next):
    print(f"Request received: {request.method} {request.url}")
    start_time = time.time()
    
    response = await call_next(request)
    
    end_time = time.time()
    duration = end_time - start_time
    print(f"Duration: {duration:.4f} seconds")
    return response

app.middleware("http")(log_middleware)

#==============================
users = []

class User(BaseModel):
    firstname: str
    lastname: str
    age: int
    email: str
    height: str

#==============================
@app.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    if any(existing_user.email == user.email for existing_user in users):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    
    users.append(user)
    return user