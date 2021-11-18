from core.config import DATABASE_URL


TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["db", "aerich.models"],
            "default_connection": "default",
        },
    },
}
