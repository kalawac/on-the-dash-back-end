# from app import db
from flask import make_response, abort

def validate_instance(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    instance = cls.query.get(model_id)

    if not instance:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return instance

def append_dicts_to_list(objects):
    return [object.to_dict() for object in objects]