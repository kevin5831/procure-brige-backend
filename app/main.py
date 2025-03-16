from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database import init_db
from app.routes import user, company, assets, auth
from app.routes.finance import depreciation_schedule, depreciation_setup, impairment_revaluation
from app.exceptions import custom_exception_handler

# ✅ Lifespan Context Manager (Replaces `on_event("startup")`)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting FastAPI Application...")
    await init_db()  # Initialize database
    yield  # Application is running
    print("🛑 Shutting down FastAPI Application...")

# ✅ Initialize FastAPI with Lifespan
app = FastAPI(title=settings.SITE_NAME, lifespan=lifespan)

# ✅ CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register Routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(company.router, prefix="/companies", tags=["Companies"])
app.include_router(assets.router, prefix="/assets", tags=["Assets"])

app.include_router(depreciation_setup.router, prefix="/finance", tags=["Finance"])
app.include_router(depreciation_schedule.router, prefix="/finance", tags=["Finance"])
app.include_router(impairment_revaluation.router, prefix="/finance", tags=["Finance"])

# ✅ Exception Handling
app.add_exception_handler(Exception, custom_exception_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
