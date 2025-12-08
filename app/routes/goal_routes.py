from flask import Blueprint, make_response, request, Response, abort
from .routes_utilities import create_model, validate_model, get_models_with_filters
from app.models.goal import Goal
from app.models.task import Task
from ..db import db

goal_list_bp = Blueprint("goal_list", __name__, url_prefix="/goals")

@goal_list_bp.post("")
def create_new_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@goal_list_bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)

@goal_list_bp.get("/<id>")
def get_goal_by_id(id):
    goal = validate_model(Goal, id)
    return goal.to_dict()

@goal_list_bp.put("/<id>")
def replace_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")

@goal_list_bp.delete("/<id>")
def delete_goal(id):
    goal = validate_model(Goal, id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@goal_list_bp.post("/<id>/tasks")
def create_task_for_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])

    for task in goal.tasks:
        task.goal_id = None

    tasks = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id
        tasks.append(task)

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": [task.id for task in tasks]
    }, 200


@goal_list_bp.get("/<id>/tasks")
def get_tasks_for_specific_goal(id):
    goal = validate_model(Goal, id)

    tasks_response = [task.to_dict() for task in goal.tasks]


    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }, 200