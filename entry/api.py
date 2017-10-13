from flask.views import MethodView
from flask import jsonify, request, abort
from jsonschema import Draft4Validator
from jsonschema.exceptions import best_match
import uuid
import json
import datetime

from app.decorators import app_required
from entry.models import Entry
from entry.schema import schema
from entry.templates import entry_obj, entries_obj


class EntryAPI(MethodView):

    decorators = [app_required]

    def __init__(self):
        self.ENTRIES_PER_PAGE = 10
        if (request.method != 'GET' and request.method != 'DELETE') and not request.json:
            abort(400)

    def get(self, entry_id):
        if entry_id:
            entry = Entry.objects.filter(external_id=entry_id).first()
            if entry:
                response = {
                    "result": "ok",
                    "entry": entry_obj(entry)
                }
                return jsonify(response), 200
            else:
                return jsonify({}), 404
        else:
            pass

    def post(self):
        entry_json = request.json
        error = best_match(Draft4Validator(schema).iter_errors(entry_json))
        if error:
            return jsonify({"error": error.message}), 400
        try:
            created_date = datetime.datetime.strptime(
                entry_json.get('created_date'), "%Y-%m-%dT%H:%M:%SZ")
        except:
            return jsonify({"error": "INVALID_DATE"}), 400

        entry = Entry(
            external_id=str(uuid.uuid4()),
            created_date=created_date,
            chest=entry_json.get('chest'),
            stomach=entry_json.get('stomach'),
            hips=entry_json.get('hips'),
            weight=entry_json.get('weight')
        ).save()
        response = {
            "result": "ok",
            "entry": entry_obj(entry)
        }
        return jsonify(response), 201

    def put(self):
        pass

    def delete(self):
        pass
