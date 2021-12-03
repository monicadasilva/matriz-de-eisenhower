from flask import request, current_app, jsonify
from app.models.categories_model import CategoryModel
from sqlalchemy import exc, orm
from app.models.eisenhowers_model import EisenhowerModel

from app.models.tasks_model import TaskModel

def create_category(kwargs):
    session = current_app.db.session
    
    if kwargs == None:
        data = request.get_json()
        
        try:
            category = CategoryModel(**data)
            session.add(category)
            session.commit()
            
            return {'id':category.id, 'name': category.name, 'description': category.description}, 201
        
        except exc.IntegrityError:
            return {'msg': 'This category already exists!'}, 409
    
   
    category = CategoryModel(**kwargs)
    session.add(category)
    session.commit()
    return {'id':category.id}


def update_category(id:int):
    session = current_app.db.session
    data = request.get_json()
    
    for value in data.values():    
        if type(value) != str:
            return jsonify({'msg': 'All inputs must be a string.'}), 400
    
    try:
        category = CategoryModel.query.filter_by(id=id).update(data)
        session.commit()
        
        category = CategoryModel.query.get(id)

        if category == None:
            return jsonify({'msg': 'Category not found.'}), 404

        return jsonify({'id':category.id, 'name': category.name, 'description': category.description}), 200

    except exc.IntegrityError:
            return jsonify({'msg': 'This category already exists!'}), 409
        
    except exc.InvalidRequestError:
            return jsonify({'msg': 'Only name and description keys are allowed.'}), 400


def delete_category(id:int):
    session = current_app.db.session

    try:
        category = CategoryModel.query.get(id)
        session.delete(category)
        session.commit()
        return '', 204

    except orm.exc.UnmappedInstanceError:
        return jsonify({'msg': 'Category not found.'}), 404
    

def get_all():
    session = current_app.db.session
    
    result = session.query(CategoryModel, TaskModel, EisenhowerModel).filter(TaskModel.eisenhowers_id == EisenhowerModel.id).all()
    output = []
    
    
    for categories, tasks, eisenhowers in result:
        output.append({
            "id":categories.id,
            "name": categories.name,
            "description": categories.description,
            "tasks":[{
            "id":tasks.id,
            "name": tasks.name,
            "description": tasks.description,
            "priority": eisenhowers.type,
            }]
            })
    
    
    return jsonify(output), 200
    