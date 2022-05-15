from flask import jsonify


def success_message(payload=None):
    if not payload:
        payload = dict()
    payload.update({"success": "ok"})
    return jsonify(payload)
