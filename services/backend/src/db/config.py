from src.core.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.async_database_url},
    "apps": {
        "models": {
            "models": ["db", "aerich.models"],
            "default_connection": "default",
        },
    },
}
