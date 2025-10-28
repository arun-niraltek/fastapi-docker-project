from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from pathlib import Path

# Import routers
from src.routers import health

# Define lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ FastAPI app started successfully at: http://127.0.0.1:3000\n")
    yield
    print("🛑 FastAPI app is shutting down...")

# Initialize FastAPI app
app = FastAPI(title="My FastAPI Project", lifespan=lifespan)

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Template configuration
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Static files (CSS, JS, Images)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Root route
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "My FastAPI Project"}
    )

# Include router
app.include_router(health.router)

if __name__ == "__main__":
    import uvicorn
    host = "0.0.0.0"
    port = 3000
    print(f"\n🚀 Starting FastAPI server at: http://{host}:{port}\n")
    uvicorn.run("src.main:app", host=host, port=port, reload=True)