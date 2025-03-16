from tortoise import Tortoise
from app.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "app.models.company",
                "app.models.assets",
                "app.models.depreciation",
                "app.models.depreciation_history",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}

async def init_db():
    """Initialize database and generate schema."""
    print(f"🔗 Connecting to Database: {settings.DATABASE_URL}")  # ✅ Debug print
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)
    print("✅ Database Connected Successfully")
