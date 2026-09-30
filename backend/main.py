from fastapi import FastAPI

app = FastAPI(
    title="Energy Consumption Analysis & Optimization System",
    version="1.0.0"
)

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