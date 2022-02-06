from src.core.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URI},
    "apps": {
        "models": {
            "models": ["db", "aerich.models"],
            "default_connection": "default",
        },
    },
}
