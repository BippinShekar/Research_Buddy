from fastapi import FastAPI
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
from routes.agent_routes import router as agent_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router, prefix="/api")

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=120, workers=os.getenv("WORKERS", 1))
    except Exception as e:
        print(f"Falied to Start Server: {e}")
        raise e