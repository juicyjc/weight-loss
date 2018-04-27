def entry_obj(entry):
    return {
        "id":           entry.external_id,
        "created_date": str(entry.created_date.isoformat()[:19]) + "Z",
        "chest":        str(entry.chest),
        "stomach":      str(entry.stomach),
        "hips":         str(entry.hips),
        "weight":       str(entry.weight),
        "links": [
            { "rel": "self", "href": "/entries/" + entry.external_id }
        ]
    }


def entries_obj(entries):
    entries_obj = []
    for entry in entries.items:
        entries_obj.append(entry_obj(entry))
    return entries_obj
