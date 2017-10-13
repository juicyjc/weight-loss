from flask import Blueprint

from entry.api import EntryAPI

entry_app = Blueprint('entry_app', __name__)

entry_view = EntryAPI.as_view('entry_api')
entry_app.add_url_rule('/entries/', defaults={'entry_id': None},
    view_func=entry_view, methods=['GET',])
entry_app.add_url_rule('/entries/', view_func=entry_view, methods=['POST',])
entry_app.add_url_rule('/entries/<entry_id>', view_func=entry_view,
    methods=['GET', 'PUT', 'DELETE',])
