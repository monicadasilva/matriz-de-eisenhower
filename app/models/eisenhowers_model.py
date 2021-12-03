from app.configs.database import db

class EisenhowerModel(db.Model):
    id:int
    type:str   
    
    __tablename__ = 'eisenhowers'


    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))

    tasks = db.relationship("TaskModel", backref="eisenhower",uselist=True)