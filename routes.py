from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from models import db, Task

main = Blueprint("main", __name__)


@main.route("/")
def index():
    priority_filter = request.args.get("priority", "all")
    status_filter = request.args.get("status", "all")
    sort_by = request.args.get("sort", "created")

    query = Task.query

    if priority_filter != "all":
        query = query.filter(Task.priority == priority_filter)

    if status_filter == "completed":
        query = query.filter(Task.completed == True)
    elif status_filter == "pending":
        query = query.filter(Task.completed == False)

    if sort_by == "priority":
        priority_order = {"high": 0, "medium": 1, "low": 2}
        tasks = query.all()
        tasks = sorted(tasks, key=lambda t: priority_order.get(t.priority, 1))
    else:
        tasks = query.order_by(Task.created_at.desc()).all()

    stats = {
        "total": Task.query.count(),
        "completed": Task.query.filter(Task.completed == True).count(),
        "pending": Task.query.filter(Task.completed == False).count(),
        "high": Task.query.filter(
            Task.priority == "high", Task.completed == False
        ).count(),
    }

    return render_template(
        "index.html",
        tasks=tasks,
        stats=stats,
        priority_filter=priority_filter,
        status_filter=status_filter,
        sort_by=sort_by,
    )


@main.route("/task/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    description = request.form.get("description")
    priority = request.form.get("priority", "medium")

    if not title:
        flash("Title is required!", "error")
        return redirect(url_for("main.index"))

    task = Task(
        title=title,
        description=description,
        priority=priority,
    )

    db.session.add(task)
    db.session.commit()

    flash("Task added successfully!", "success")
    return redirect(url_for("main.index"))


@main.route("/task/<int:task_id>/edit", methods=["POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    task.title = request.form.get("title")
    task.description = request.form.get("description")
    task.priority = request.form.get("priority", "medium")

    db.session.commit()

    flash("Task updated successfully!", "success")
    return redirect(url_for("main.index"))


@main.route("/task/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    flash("Task deleted successfully!", "success")
    return redirect(url_for("main.index"))


@main.route("/task/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)

    task.completed = not task.completed
    db.session.commit()

    status = "completed" if task.completed else "pending"
    flash(f"Task marked as {status}!", "success")
    return redirect(url_for("main.index"))


@main.route("/api/task/<int:task_id>")
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())
