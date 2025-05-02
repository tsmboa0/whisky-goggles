import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import endpoints

app = FastAPI(
    title="Whisky Goggles API",
    description="An API for recognizing whisky bottles from images.",
    version="1.0.0"
)

# Serve the frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dir, "assets")), name="assets")

# Include the API endpoints router
app.include_router(endpoints.router)

@app.get("/")
def read_root():
    return FileResponse(os.path.join(frontend_dir, "index.html"))
