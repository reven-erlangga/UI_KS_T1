from flask import Blueprint, request, send_file
from services.download_service import get_file_path

download_bp = Blueprint('download', __name__)

@download_bp.route('/<file>', methods=['GET'])
def download_file(file):
    """
    Route to handle file downloads.
    """
    try:
        path = get_file_path(file)  # Get the file path from the service
        return send_file(path, as_attachment=True)
    except FileNotFoundError:
        return {"error": "File not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
