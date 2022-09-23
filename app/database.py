import databases
import sqlalchemy


def connect_database():
    DATABASE_URL = "sqlite:///./blog.db"

    database = databases.Database(DATABASE_URL)

    metadata = sqlalchemy.MetaData()

    engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )

    posts_table = sqlalchemy.Table(
        "posts",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True),
        sqlalchemy.Column("title", sqlalchemy.String),
        sqlalchemy.Column("text", sqlalchemy.String),
    )

    metadata.create_all(engine)

    return database, posts_table
