import databases
import sqlalchemy
from storeapi.config import config

### Sqlalchemy is used to create the database engine; we define what tables & columns we want to create
metadata = sqlalchemy.MetaData()

post_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
)

comment_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    ### foreign key to posts table(table name, column name), the metadata object is used to detect the target data type and apply it to the column below
    sqlalchemy.Column(
        "post_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("posts.id"), nullable=False
    ),
)

### connect_args={"check_same_thread": False} - only needed in sqlite, because it is traditionally single threaded
engine = sqlalchemy.create_engine(
    config.DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)
### Databases module is used to connect to the database, our code will use it to interact with the database
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLLBACK
)
