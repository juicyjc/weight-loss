from application import db


class Entry(db.Document):
    external_id = db.StringField(db_field="ei")
    created_date = db.DateTimeField(db_field="cd")
    chest = db.DecimalField(db_field="c", precision=1, rounding="ROUND_HALF_UP")
    stomach = db.DecimalField(db_field="s", precision=1, rounding="ROUND_HALF_UP")
    hips = db.DecimalField(db_field="h", precision=1, rounding="ROUND_HALF_UP")
    weight = db.DecimalField(db_field="w", precision=1, rounding="ROUND_HALF_UP")

    meta = {
        'indexes': [('external_id', ), ('created_date', )]
    }
