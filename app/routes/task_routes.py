from flask import Blueprint, request, Response, session
from app.models.task import Task
from ..db import db
from .routes_utilities import create_model, validate_model, get_models_with_filters
from datetime import datetime

task_list_bp = Blueprint("task_list", __name__, url_prefix="/tasks")

@task_list_bp.get("/<id>")
def get_task_by_id(id):
    task = validate_model(Task, id)
    return task.to_dict()

@task_list_bp.get("")
def get_all_tasks():
    sort = request.args.get("sort", "asc")
    return get_models_with_filters(Task, request.args, sort=sort)


@task_list_bp.post("")
def create_new_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

@task_list_bp.put("/<id>")
def replace_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")


@task_list_bp.delete("/<id>")
def delete_task(id):
    task = validate_model(Task, id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@task_list_bp.patch("/<id>/mark_complete")
def mark_task_complete(id):
    task = validate_model(Task, id)
    task.to_dict()


    task.is_complete = True
    task.completed_at = datetime.now()


    db.session.commit()
    return Response(status=204, mimetype="application/json")

@task_list_bp.patch("/<id>/mark_incomplete") 
def mark_task_incomplete(id):
    task = validate_model(Task, id)
    task.completed_at = None
    task.is_complete = False

    db.session.commit()
    return Response(status=204, mimetype="application/json")
