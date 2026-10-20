# from flask import Flask, Blueprint, session, redirect, render_template, flash, request, url_for
# from app import db
# from app.models import Task

# tasks_bp = Blueprint('tasks', __name__)

# @tasks_bp.route('/')
# def view_tasks():
#     if 'user' not in session:
#         return redirect(url_for('auth.login'))
        
#     tasks = Task.query.all()
#     return render_template('tasks.html', tasks=tasks)
    
# @tasks_bp.route('/add', methods=["POST"])
# def add_task():
#     if 'user' not in session:
#         return redirect(url_for('auth.login'))
        
#     title = request.form.get('title')
#     if title:
#         new_task = Task(title = title, status = 'Pending')
#         db.session.add(new_task)
#         db.session.commit()
#         flash('Task Added Successfully', 'success')

#         return redirect(url_for('tasks.view_tasks'))

# @tasks_bp.route('/toggle/<int:task_id>', methods=["POST"])
# def toggle_status(task_id):
#     task = Task.query.get(task_id)
#     if task:
#         if task.status == 'Pending':
#             task.status = 'Working'
#         elif task.status == 'Working':
#             task.status = 'Done'
#         else:
#             task.status = 'Pending'
#     db.session.commit()
#     return redirect(url_for('tasks.view_tasks'))

# @tasks_bp.route('/clear', methods=["POST"])
# def clear_task():
#     Task.query.delete()
#     db.session.commit()
#     flash('All Tasks Cleared', 'info')
#     return redirect(url_for('tasks.view_tasks'))

from flask import Blueprint, session, redirect, render_template, request, url_for, jsonify
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)

# 1. Main Page UI Router
@tasks_bp.route('/')
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('tasks.html') # Simply serves your HTML layout file

# 2. GET API: Fetch all tasks from the database
@tasks_bp.route('/api/tasks', methods=['GET'])
def get_tasks_api():
    tasks = Task.query.all()
    return jsonify({"success": True, "data": [{"id": t.id, "title": t.title, "status": t.status} for t in tasks]})

# 3. POST API: Add a task via JSON from the frontend
@tasks_bp.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json() # Grabs the data coming from your JavaScript
    new_task = Task(title=data['title'], status='Pending')
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"success": True})

# 4. PUT API: Toggle status, auto-clear tasks, and auto-logout
@tasks_bp.route('/api/tasks/toggle/<int:task_id>', methods=['PUT'])
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"success": False, "error": "Task not found"}), 404

    task.status = 'Working' if task.status == 'Pending' else 'Done' if task.status == 'Working' else 'Pending'
    db.session.commit()

    # Check if any tasks are still incomplete
    remaining_incomplete_tasks = Task.query.filter(Task.status != 'Done').first()
    
    # If everything is Done, wipe the database and log out the user session
    if not remaining_incomplete_tasks:
        Task.query.delete()
        db.session.commit()
        
        session.clear()  # <-- Safely destroys the user login session logs
        return jsonify({"success": True, "cleared": True, "logged_out": True})

    return jsonify({"success": True, "cleared": False, "logged_out": False})

# 5. DELETE API: Clear all entries instantly
@tasks_bp.route('/api/tasks/clean', methods=['DELETE'])
def clear_task():
    Task.query.delete()
    db.session.commit()
    return jsonify({"success": True})