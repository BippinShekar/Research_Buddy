from fastapi import FastAPI
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
from routes.research_routes import router as research_routers
from routes.resource_routes import router as resource_routers
from enums.environmet_variables import EnvironmentVariables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(research_routers, prefix="/api")
app.include_router(resource_routers, prefix="/api")

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=120, workers = max(int(EnvironmentVariables.WORKERS.value_from_env),4))
    except Exception as e:
        print(f"Falied to Start Server: {e}")
        raise e