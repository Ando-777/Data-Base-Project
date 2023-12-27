import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

DB_NAME = 'rock-bands'
DB_OWNER = 'Andranik_Baghdasaryan'
DB_URI = f'postgresql:///{DB_NAME}'

engine = create_engine(DB_URI)

if not database_exists(engine.url):
    create_database(engine.url)
    print(f'Database {DB_NAME} created.')
else:
    print(f'Database {DB_NAME} already exists.')

with engine.connect() as conn:
    conn.execute(f'ALTER DATABASE {DB_NAME} OWNER TO {DB_OWNER}')
    print(f'Owner of database {DB_NAME} set to {DB_OWNER}.')