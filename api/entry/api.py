from flask.views import MethodView
from flask import jsonify, request, abort
from jsonschema import Draft4Validator
from jsonschema.exceptions import best_match
import uuid
import json
import datetime
from decimal import Decimal

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
            entry_href = "/entries/?page=%s"
            entries = Entry.objects.filter(live=True)
            page = int(request.args.get('page', 1))
            entries = entries.paginate(page=page, per_page=self.ENTRIES_PER_PAGE)
            response = {
                "result": "ok",
                "links": [
                    {
                        "href": entry_href % page,
                        "rel": "self"
                    }
                ],
                "entries": entries_obj(entries)
            }
            if entries.has_prev:
                response["links"].append(
                    {
                        "href": entry_href  % (entries.prev_num),
                        "rel": "previous"
                    }
                )
            if entries.has_next:
                response["links"].append(
                    {
                        "href": entry_href % (entries.next_num),
                        "rel": "next"
                    }
                )
            return jsonify(response), 200

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

    def put(self, entry_id):
        entry = Entry.objects.filter(external_id=entry_id, live=True).first()
        if not entry:
            return jsonify({}), 404
        entry_json = request.json
        created_date = entry.created_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        entry_json['created_date'] = str(created_date)
        error = best_match(Draft4Validator(schema).iter_errors(entry_json))
        if error:
            return jsonify({"error": error.message}), 400

        entry.chest = entry_json.get('chest')
        entry.hips = entry_json.get('hips')
        entry.stomach = entry_json.get('stomach')
        entry.weight = entry_json.get('weight')
        entry.save()
        response = {
            "result": "ok",
            "entry": entry_obj(entry)
        }
        return jsonify(response), 200

    def delete(self):
        pass
