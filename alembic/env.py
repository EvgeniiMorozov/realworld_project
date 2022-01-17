import pathlib
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

sys.path.append(str(pathlib.Path().absolute()))


# sys.path.append(str(pathlib.Path().absolute()))
# sys.path = ['', '..'] + sys.path[1:]

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# sys.path.append(str(pathlib.Path().cwd().parent))

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from app import db
from app.core.config import settings


target_metadata = db.metadata


def get_url():
    return settings.alembic_database_url

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )
    # connectable = engine
    #
    # with connectable.connect() as connection:
    #     context.configure(
    #         connection=connection, target_metadata=target_metadata
    #     )
    #

    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
