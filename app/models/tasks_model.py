from app.configs.database import db

class TaskModel(db.Model):
    id:int
    name:str
    description:str    
    duration:int
    importance:int 
    urgency:int
    eisenhower_id:int

    __tablename__ = 'tasks'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(200))
    duration = db.Column(db.Integer)
    importance = db.Column(db.Integer)
    urgency = db.Column(db.Integer)
    
    tasks_categories = db.relationship("TaskCategoryModel", backref="task",uselist=True)
    
    
    eisenhowers_id = db.Column(
      db.Integer,
      db.ForeignKey("eisenhowers.id"),
      nullable=False,
      )
