from app import db
from flask import Blueprint, jsonify, request, make_response, abort

bp = Blueprint("indicators_bp", __name__, url_prefix="/indicators")