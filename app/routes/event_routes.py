from app import db
from flask import Blueprint, jsonify, request, make_response, abort

bp = Blueprint("events_bp", __name__, url_prefix="/events")