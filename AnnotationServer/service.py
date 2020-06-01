import json
import uuid
import db, validator
from datetime import datetime

def create_annotation(data):
    data_validation = validator.validate_body(data)
    if data_validation == True:
        annotation_id = str(uuid.uuid1())
        data["id"] = annotation_id
        data["created"] = str(datetime.now())
        db.add_to_memory(data)
        return data
    else:
        return data_validation

def serve_annotation(id):
    annotation = db.find_row(id)
    return annotation

def edit_annotation(data, id):
    data_validation = validator.validate_body(data)
    if data_validation == True:
        annotation = db.find_row(id)
        annotation["body"] = data["body"]
        annotation["modified"] = str(datetime.now())
        db.edit_row(annotation)
        return annotation
    else:
        return data_validation

def remove_annotation(id):
    db.delete_row(id)