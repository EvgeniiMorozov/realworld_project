from starlette.config import Config


config = Config(".env")

DATABASE_URL = config("RW_DATABASE_URL", cast=str, default="")


JWT_CONST = "This is the most common scenario for using JWT. Once the user is logged in, each subsequent request will" \
            " include the JWT, allowing the user to access routes, services, and resources that are permitted " \
            "with that token. Single Sign On is a feature that widely uses JWT nowadays, because of its small" \
            " overhead and its ability to be easily used across different domains."
