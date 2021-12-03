from app.configs.database import db

class TaskCategoryModel(db.Model):
    __tablename__ = 'task_categories'

    id = db.Column(db.Integer, primary_key=True)
    
    
    task_id = db.Column(
      db.Integer,
      db.ForeignKey("tasks.id"),
      )

    category_id = db.Column(
      db.Integer,
      db.ForeignKey("categories.id"),
      )
