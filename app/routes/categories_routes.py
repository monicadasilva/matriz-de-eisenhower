from flask import Blueprint

from app.controllers.categories_controller import create_category, delete_category, get_all, update_category

bp_cat = Blueprint('bp_categories', __name__, url_prefix='/category')


bp_cat.post('')(create_category)
bp_cat.get('')(get_all)
bp_cat.patch('/<int:id>')(update_category)
bp_cat.delete('/<int:id>')(delete_category)

