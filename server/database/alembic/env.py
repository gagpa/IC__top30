from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

from database import Base
from settings import postgres_settings

config = context.config
config.set_main_option('sqlalchemy.url', postgres_settings.ALEMBIC_URI)

fileConfig(config.config_file_name)  # setting up loggers

target_metadata = Base.metadata

exclude_tables = ['hr_statistics']


def include_object(object, name, type_, *args, **kwargs):
    return not (type_ == 'table' and name in exclude_tables)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=postgres_settings.ALEMBIC_URI,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
        compare_type=True,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(postgres_settings.ALEMBIC_URI)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
