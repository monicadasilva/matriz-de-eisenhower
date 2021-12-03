from flask import request, current_app
from app.controllers import eisenhower
from app.controllers.categories_controller import create_category
from app.models.categories_model import CategoryModel
from app.models.tasks_categories_model import TaskCategoryModel
from app.models.tasks_model import TaskModel
from sqlalchemy import exc, orm


def create_task():
    session = current_app.db.session
    data = request.get_json()

 
    categories = data['categories']    
    cat_task_id = []
    if len(categories) >= 1:
        for item in categories:
            category = CategoryModel.query.filter_by(name=item['name']).first()
            if not category:
                cat = create_category(item)
                cat_task_id.append({'category_id': cat['id']})

            if category:
                cat_task_id.append({'category_id': category.id})

    eisenhowers = ''
    eisenhower_msg = ''
    
    try:
        eisenhower_data = eisenhower(data)
        eisenhowers = eisenhower_data[0]
        eisenhower_msg = eisenhower_data[1]
    except exc.DataError:
        return {'error': {'valid_options':{'importance': [1,2], 'urgency': [1,2]}, 'recieved_optios':{ 'importance':data['importance'], 'urgency': data['urgency']}}}, 404
    
    try:    
        data_filtered = {
        "name":data['name'],
        "description":data['description'],
        "duration":data['duration'],
        "importance":data['importance'],
        "urgency":data['urgency'],
        "eisenhowers_id": eisenhowers,
        }

        task = TaskModel(**data_filtered)
        session.add(task)
        session.commit()
        

        if len(cat_task_id) >= 1:
            for item in cat_task_id:
                item.update({'task_id': task.id})
        
        for item in cat_task_id:
                tcat = TaskCategoryModel(**item)
                session.add(tcat)
                session.commit()

        return {
        "id": task.id,
        "name":data['name'],
        "description":data['description'],
        "duration":data['duration'],
        "eisenhower_classification": eisenhower_msg.type,
        "category": categories
        },201
    
    except exc.IntegrityError:
            return {'msg': 'This task already exists!'}, 409


def update_task(id):
    session = current_app.db.session
    data = request.get_json()
    task = TaskModel.query.get(id)
    
    if task == None:
            return {'msg': 'Task not found.'}, 404
    
    info = {
            "importance": task.importance,
            "urgency":task.urgency
            }
    

    if 'importance' in data:
        info.update({"importance":data['importance']})
        
    if 'urgency' in data:
        info.update({"urgency":data['urgency']})
    
    try:
        eisenhower_data = eisenhower(info)
        eisenhowers = eisenhower_data[0]
        eisenhower_msg = eisenhower_data[1]
        
        data.update({"eisenhowers_id":eisenhowers})
        
        TaskModel.query.filter_by(id=id).update(data)
        session.commit()
        
        
        return{
        "id": task.id,
        "name": task.name,
        "description": task.description,
        "duration": task.duration,
        "eisenhower_classification":eisenhower_msg.type,
        },201
    
    except exc.IntegrityError:
        return {'msg': 'This task name already exists in database!'}, 409
   
    except exc.DataError:
        return {'error': {'valid_options':{'importance': [1,2], 'urgency': [1,2]}, 'recieved_optios':{ 'importance':data['importance'], 'urgency': data['urgency']}}}, 404

    except exc.InvalidRequestError:
            return {'msg': 'Only name, description, duration, importance, urgency keys are allowed.'}, 400


def delete_task(id:int):
    session = current_app.db.session

    try:
        tasks = TaskModel.query.get(id)
        session.delete(tasks)
        session.commit()
        return '', 204

    except orm.exc.UnmappedInstanceError:
        return {'msg': 'Task not found.'}, 404