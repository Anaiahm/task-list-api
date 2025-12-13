from flask import Blueprint, request, Response, session
from app.models.task import Task
from ..db import db
from .routes_utilities import create_model, validate_model, get_models_with_filters
from datetime import datetime
import requests
import os




task_list_bp = Blueprint("task_list", __name__, url_prefix="/tasks")

@task_list_bp.get("/<id>")
def get_task_by_id(id):
    task = validate_model(Task, id)
    response_body = task.to_dict()
    return response_body


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
    task.completed_at = datetime.now()


    db.session.commit()
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    slack_message_text = f"Someone just completed the task {task.title}"
    slack_channel = "task-notifications"
    slack_url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    json = {
        "channel": slack_channel,
        "text": slack_message_text
    }

    response = requests.post(slack_url, headers=headers, json=json)
    try:
        requests.post(slack_url, headers=headers, json=json)
        print(response.status_code, response.text)
    except Exception as e:
        print("Slack request failed:", e)

    return Response(status=204, mimetype="application/json")

@task_list_bp.patch("/<id>/mark_incomplete") 
def mark_task_incomplete(id):
    task = validate_model(Task, id)
    task.completed_at = None
    task.is_complete = False

    db.session.commit()
    return Response(status=204, mimetype="application/json")

