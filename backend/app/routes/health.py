from flask import jsonify, Blueprint
from app import db
from sqlalchemy import text

health_routes = Blueprint('health', __name__)

@health_routes.route('/health', methods=['GET'])
def get_status():
    try:
        # check for db connection
        db.session.execute(text('SELECT 1'))
        return jsonify(
            {
                "status": "success",
                "message": "Service is up and healthy."
            }
        ), 200
    except Exception as e:
        # if there is a connection issue
        return jsonify(
            {
                "status": "fail",
                "message": f'Service is down: {str(e)}'
            }
        ), 500