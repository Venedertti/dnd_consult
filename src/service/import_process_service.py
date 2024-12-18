import uuid
import threading
from datetime import datetime
from src.database import db
from src.database.import_process_model import ImportProcess
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

class ImportProcessService:
    @staticmethod
    def create_new_process():
        new_process = ImportProcess(
            process_id=str(uuid.uuid4()),
            status="processing",
            start_time=datetime.utcnow(),
            end_time=None,
            result=None
        )
        db.session.add(new_process)
        db.session.commit()
        return new_process.process_id

    @staticmethod
    def update_process_status(process_id, status, result=None):
        
        process = ImportProcess.query.get(process_id)
        if process:
            process.status = status
            process.result = result
            process.end_time = datetime.utcnow() if status == "completed" else None
            db.session.commit()

    @staticmethod
    def get_process_status(process_id):
        process = ImportProcess.query.get(process_id)
        if process:
            return {
                "process_id": process.process_id,
                "status": process.status,
                "result": process.result,
                "start_time": process.start_time,
                "end_time": process.end_time
            }
        return {"error": "Process not found"}
