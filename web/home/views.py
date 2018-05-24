from flask import Blueprint, jsonify, current_app, render_template, request, abort, redirect, url_for, session
from datetime import datetime
from decimal import Decimal
import requests
import json
import pytz

from home.constants import *
from entry.models import Entry, EntryForm

home_app = Blueprint('home_app', __name__)


@home_app.route('/register_app')
def register_app():
    return register_app_with_api()


@home_app.route('/entries', methods=('GET', 'POST'))
def entries():
    headers = get_auth_headers()
    if headers:
        url = URL_ENTRIES
        form = EntryForm()
        if request.method == 'POST' and form.validate_on_submit():
            # Call API to add entry
            data = {
                "created_date": str(datetime.utcnow().isoformat()[:19]) + "Z",
                "chest": str(form.chest.data),
                "stomach": str(form.stomach.data),
                "hips": str(form.hips.data),
                "weight": str(form.weight.data)
            }
            r = requests.post(url, headers=headers, json=data)

        r = requests.get(url, headers=headers)
        entries = Entry.entries_json(r.json())
        return render_template('./home/entries.html', entries=entries, form=form)

    else:
        return 'APP_NOT_REGISTERED'


@home_app.route('/entry/<string:entry_id>', methods=('GET', 'POST'))
def entry(entry_id):
    headers = get_auth_headers()
    if headers:
        url = URL_ENTRIES + entry_id
        r = requests.get(url, headers=headers)
        if not r.json():
            abort(404)
        entry = Entry.entry_json(r.json()['entry'])
        form = EntryForm(obj=entry)
        if request.method == 'POST' and form.validate_on_submit():
            # Call API to edit entry
            data = {
                "chest": str(form.chest.data),
                "stomach": str(form.stomach.data),
                "hips": str(form.hips.data),
                "weight": str(form.weight.data)
            }
            r = requests.put(url, headers=headers, json=data)
            if r.status_code == 200:
                return redirect(url_for('home_app.entries'))
        return render_template('./home/edit_entry.html', entry=entry, form=form)
    else:
        return 'APP_NOT_REGISTERED'


@home_app.route('/set_style')
def set_style():
    style = request.args.get('style')
    styles = ['superhero', 'yeti']
    if style and style in styles:
        session['style'] = style
    return redirect(url_for('home_app.entries'))


def get_simple_headers():
    return {
        "Content-Type": "application/json"
    }


def get_app_id_and_secret():
    data = {
        "app_id": current_app.config['APP_ID'],
        "app_secret": current_app.config['APP_SECRET']
    }
    return data


def get_auth_headers():
    headers = get_simple_headers()
    data = get_app_id_and_secret()
    url = URL_ACCESS_TOKEN
    r = requests.post(url, headers=headers, json=data)
    headers = None
    try:
        token = r.json()['token']
    except KeyError:
        print('Application is not registered with API.')
    else:
        headers = {
            "Content-Type": "application/json",
            "X-APP-ID": current_app.config['APP_ID'],
            "X-APP-TOKEN": token
        }
    return headers


def register_app_with_api():
    url = URL_APPS
    headers = get_simple_headers()
    data = get_app_id_and_secret()
    r = requests.post(url, headers=headers, json=data)
    if r.status_code == 200:
        return 'APP_REGISTERED'
    else:
        return r.text
