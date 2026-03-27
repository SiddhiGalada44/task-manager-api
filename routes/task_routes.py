from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Task, engine
from auth import require_auth

task_bp= Blueprint("tasks", __name__)

@task_bp.route("/tasks", methods=["GET"])
@require_auth
def get_tasks():
    with Session(engine) as session:
        tasks = session.query(Task).filter(Task.user_id == request.user_id).all()
        return jsonify([{
            "id": task.id,
            "title": task.title,
            "completed": task.completed
        } for task in tasks]), 200
    
@task_bp.route("/tasks", methods=["POST"])
@require_auth
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    
    with Session(engine) as session:
        new_task = Task(
            title=data["title"],
            completed=False,
            user_id=request.user_id
        )
        session.add(new_task)
        session.commit()

        return jsonify({
            "id": new_task.id,
            "title": new_task.title,
            "completed": new_task.completed
        }), 201
    
@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@require_auth
def complete_task(task_id):
    with Session(engine) as session:
        task = session.query(Task).filter(Task.id == task_id, Task.user_id == request.user_id).first()
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        task.completed = True
        session.commit()

        return jsonify({
            "id": task.id,
            "title": task.title,
            "completed": task.completed
        }), 200
    
@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@require_auth   
def delete_task(task_id):
    with Session(engine) as session:
        task = session.query(Task).filter(Task.id == task_id, Task.user_id == request.user_id).first()
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        session.delete(task)
        session.commit()

        return jsonify({"message": "Task deleted successfully"}), 200