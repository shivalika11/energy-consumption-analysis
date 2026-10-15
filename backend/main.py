from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr


app = FastAPI(
    title="Energy Consumption Analysis & Optimization System",
    version="1.0.0"
)


# Allow the local frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str


@app.get("/")
def root():
    return {
        "message": "Energy Consumption API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/api/register")
def register_user(user: RegisterRequest):

    return {
        "message": "Registration request received successfully",
        "user": {
            "full_name": user.full_name,
            "email": user.email
        }
    }