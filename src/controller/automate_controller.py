import threading
from flask import Blueprint, jsonify, current_app
from src.service.massive_import_service import MassiveImportService
from src.service.import_process_service import ImportProcessService

automate_bp = Blueprint('automate', __name__)

@automate_bp.route('/dnd/import/<string:source>', methods=['POST'])
def bulk_import_open5e(source):
    process_id = ImportProcessService.create_new_process()
    
    app = current_app._get_current_object()

    thread = threading.Thread(target=MassiveImportService.start_import, args=(process_id, app))
    thread.start()

    return jsonify({"message": "Process started", "process_id": process_id}), 202

@automate_bp.route('/monitor/<string:process_id>', methods=['GET'])
def bulk_import_status(process_id):
    status = ImportProcessService.get_process_status(process_id)
    return jsonify(status), 200
