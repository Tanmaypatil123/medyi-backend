def sample_reponse(name, data=None):
    if data is None:
        data = {}

    return {"event": {"name": name, "type": "on"}, "data": data}


def sample_error(name, msg: str):
    if not msg:
        msg = "request issue"

    return {"event": {"name": name, "type": "on"}, "error": msg, "data": {}}
