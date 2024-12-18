from src.database import db

class ImportProcess(db.Model):
    process_id = db.Column(db.String, primary_key=True)
    status = db.Column(db.String, nullable=False)
    result = db.Column(db.JSON, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
