import sqlalchemy
import json

db_engine = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername='postgres+pg8000',
        username='user_anno',
        password='pass_anno',
        database='db_anno',
        query={
            'unix_sock': '/cloudsql/{}/.s.PGSQL.5432'.format('swe574-278917:us-central1:annotation574')
        }
    ),
    pool_size=5,

    max_overflow=2,

    pool_timeout=30,

    pool_recycle=1800,
)

def create_annotation_table():
    with db_engine.connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS community_annotation "
            "( annotation_id VARCHAR(255) PRIMARY KEY, "
            "annotation_model jsonb);"
        )

def add_to_memory(annotation):
    annotation_id = annotation["id"]
    annotation = json.dumps(annotation)
    query = sqlalchemy.text(
        "INSERT INTO community_annotation (annotation_id, annotation_model)"
        " VALUES (:annotation_id, :annotation_model)"
    )
    with db_engine.connect() as conn:
        conn.execute(query, annotation_id=annotation_id, annotation_model=annotation)

def find_row(id):
    with db_engine.connect() as conn:
        query = sqlalchemy.text(
            "SELECT annotation_model FROM community_annotation WHERE annotation_id=:annotation_id "
        )
        annotation = conn.execute(query, annotation_id=id).fetchone()
        print(annotation)
        annotation = dict(annotation)
    return annotation["annotation_model"]

def edit_row(annotation):
    annotation_id = annotation["id"]
    annotation = json.dumps(annotation)
    query = sqlalchemy.text(
        "UPDATE community_annotation "
        "SET annotation_model=:annotation_model "
        "WHERE annotation_id=:annotation_id "
    )
    with db_engine.connect() as conn:
        conn.execute(query, annotation_id=annotation_id, annotation_model=annotation)

def delete_row(id):
    query = sqlalchemy.text(
        "DELETE FROM community_annotation WHERE annotation_id=:annotation_id "
    )
    with db_engine.connect() as conn:
        conn.execute(query, annotation_id=id)