import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Agregar la carpeta base al path para importar `app`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Ahora puedes importar desde app.*
from app.database import Base
from app.models import (
    analisis,
    formulario_ingreso,
    muestra,
    usuarios
)  # Asegúrate de importar todos los modelos aquí para que Alembic los detecte

# Configuración de Alembic
config = context.config

# Configuración de logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata para el autogenerate
target_metadata = Base.metadata

# Configuración para conexión offline
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Configuración para conexión online
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

# Ejecutar migraciones
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
