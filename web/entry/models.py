import datetime
import pytz
# from datetime import timezone
# from tzlocal import get_localzone
from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import DataRequired


class Entry:
    def __init__(self, id, created_date, chest, stomach,
                 hips, weight, links):
        self.id = id
        self.created_date = created_date
        self.chest = chest
        self.stomach = stomach
        self.hips = hips
        self.weight = weight
        self.links = links

    @staticmethod
    def entry_json(entry_obj):
        'Single entry JSON object returned from API.'
        created_date = datetime.datetime.strptime(
            entry_obj['created_date'], "%Y-%m-%dT%H:%M:%SZ")
        # utc = pytz.utc
        # created_date_utc = created_date.astimezone(utc)
        # eastern = pytz.timezone('US/Eastern')
        # created_date_eastern = created_date.astimezone(eastern)
        created_date_eastern = created_date.astimezone(pytz.timezone('US/Eastern'))

        return Entry(
            entry_obj['id'],
            created_date_eastern,
            Decimal(entry_obj['chest']),
            Decimal(entry_obj['stomach']),
            Decimal(entry_obj['hips']),
            Decimal(entry_obj['weight']),
            entry_obj['links']
        )

    @classmethod
    def entries_json(cls, entries_obj):
        'List of entry JSON objects returned from API.'
        entries = []
        for entry_obj in entries_obj['entries']:
            entries.append(cls.entry_json(entry_obj))
        return entries


class EntryForm(FlaskForm):
    weight = DecimalField('Weight', validators=[DataRequired()])
    chest = DecimalField('Chest')
    stomach = DecimalField('Stomach')
    hips = DecimalField('Hips')
