from src.database import db
from src.database.classes_model import Classes

class ClassesService:
    
    @staticmethod
    def get_class_by_name(name):
        return Classes.query.filter_by(name=name).first()

    @staticmethod
    def get_classes_by_names(names):
        return Classes.query.filter(Classes.name.in_(names)).all()
