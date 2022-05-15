import os

from flask import Blueprint, request, redirect, jsonify

blueprint = Blueprint(
    "code",
    __name__,
)

events = []


@blueprint.route("/event")
def receive_code():
    code = request.args.get("code", None)
    encrypted_telegram_id = request.args.get("state", None)
    if code and encrypted_telegram_id:
        events.append({
            "type": "authorization_code",
            "code": code,
            "encrypted_telegram_id": encrypted_telegram_id
        })
    return redirect(os.getenv("INNOID_REDIRECT_AFTER_REGISTERING_EVENT"))


@blueprint.route("/get_event")
def get_event():
    if request.headers.get("Authorization", "") != "Bearer " + os.getenv("INNOID_LONGPOLL_AUTH_TOKEN"):
        return "Not authorized", 401
    if events:
        return jsonify({"event": events.pop(0)})
    return "Nothing happened", 404
