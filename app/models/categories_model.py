from app.configs.database import db

class CategoryModel(db.Model):
    id:int
    name:str
    description:str    
    
    __tablename__ = 'categories'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(200))
    

    task_categories = db.relationship("TaskCategoryModel", backref="category",uselist=True)