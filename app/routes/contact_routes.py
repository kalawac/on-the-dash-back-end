from app import db
from app.models.contact import Contact
from flask import Blueprint, jsonify, request, make_response, abort

bp = Blueprint("contacts_bp", __name__, url_prefix="/contacts")
