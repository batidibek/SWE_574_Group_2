import sqlalchemy
import json

db_engine = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername='postgresql+psycopg2',
        username='kajuyatjzemxvb',
        password='31d522de25d83c38b5b31a4c51e1aacf7c266147d4caf932253e4cce19bb970b',
        database='dcakhbp4q7nbn7',
        host='ec2-52-207-93-32.compute-1.amazonaws.com',
        port='5432'
    )
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