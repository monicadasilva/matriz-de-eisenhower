from flask import Blueprint

from app.controllers.tasks_controller import create_task, delete_task, update_task

bp_task = Blueprint('bp_task', __name__, url_prefix='/task')

bp_task.post('')(create_task)
bp_task.patch('/<int:id>')(update_task)
bp_task.delete('/<int:id>')(delete_task)