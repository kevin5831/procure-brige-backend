from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database import init_db
from app.routes import user, company, assets, auth
from app.routes.finance import depreciation_schedule, depreciation_setup, impairment_revaluation
from app.exceptions import custom_exception_handler
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# ✅ Lifespan Context Manager (Replaces `on_event("startup")`)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting FastAPI Application...")
    await init_db()  # Initialize database
    yield  # Application is running
    print("🛑 Shutting down FastAPI Application...")

# ✅ Initialize FastAPI with Lifespan
app = FastAPI(
    title=settings.SITE_NAME, 
    description="API for managing company assets, transfers, disposals, and maintenance", 
    lifespan=lifespan
)

# ✅ CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")

# ✅ Register Routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(company.router, prefix="/companies", tags=["Companies"])
app.include_router(assets.router, prefix="/api/assets", tags=["Assets"], responses={404: {"description": "resource not found"}})

app.include_router(depreciation_setup.router, prefix="/finance", tags=["Finance"])
app.include_router(depreciation_schedule.router, prefix="/finance", tags=["Finance"])
app.include_router(impairment_revaluation.router, prefix="/finance", tags=["Finance"])

@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    return FileResponse(os.path.join(frontend_path, "index.html"))

# ✅ Exception Handling
app.add_exception_handler(Exception, custom_exception_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
