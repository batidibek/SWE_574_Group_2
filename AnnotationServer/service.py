import json
import uuid
import db
from datetime import datetime

def create_annotation(data):
    annotation_id = str(uuid.uuid1())
    data["id"] = annotation_id
    data["created"] = str(datetime.now())
    db.add_to_memory(data)
    return data

def serve_annotation(id):
    annotation = db.find_row(id)
    return annotation

def edit_annotation(data, id):
    annotation = db.find_row(id)
    print(annotation)
    annotation["body"] = data["body"]
    annotation["modified"] = str(datetime.now())
    db.edit_row(annotation)
    return annotation

def remove_annotation(id):
    db.delete_row(id)