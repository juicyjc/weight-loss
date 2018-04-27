schema = {
    "type": "object",
    "properties": {
        "created_date": {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"},
        "chest": {"type": "string"},
        "stomach": {"type": "string"},
        "hips": {"type": "string"},
        "weight": {"type": "string"},
    },
    "required": ["created_date", "weight"]
}
