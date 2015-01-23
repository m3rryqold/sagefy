from flask import Blueprint, jsonify, request
from models.unit import Unit
from flask.ext.login import current_user

unit = Blueprint('unit', __name__, url_prefix='/api/units')


@unit.route('/<unit>/', methods=['GET'])
def get_unit(unit_id):
    """
    Get a specific unit given an ID.
    """
    pass
