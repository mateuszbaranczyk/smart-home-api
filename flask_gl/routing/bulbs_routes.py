from http import HTTPStatus

from flask import Blueprint, Response, make_response
from garlight.bulbs import BulbException, HomeBulb
from garlight.db.database import db
from garlight.db.models import BulbModel
from garlight.logs import gunicorn_logger
from garlight.routing.endpoints_definitions import create_definitions

bulb = Blueprint("bulb", import_name=__name__)


@bulb.route("/endpoints")
def endpoints():
    devices = db.session.execute(db.select(BulbModel)).scalars()
    names = [device.name for device in devices]
    endpoints = create_definitions(devices=names)
    response = make_response(endpoints)
    response.mimetype = "text/plain"
    return response


@bulb.route("/status")
def status():
    saved_devices = db.session.execute(db.select(BulbModel)).scalars()
    bulbs = [HomeBulb(device.name) for device in saved_devices]
    statuses = [bulb.state for bulb in bulbs]
    return {"statuses": statuses}


@bulb.route("/on-off/<string:name>")
def on_off(name: str):
    bulb = HomeBulb(name)
    response = change_request(bulb)
    return response


@bulb.route("/set-warm/<string:name>")
def set_warm(name: str):
    temperature = 2000
    brightness = 40
    bulb = HomeBulb(name)
    msg = bulb.set_temperature(temperature, brightness)
    return create_response(msg, bulb)


@bulb.route("/set-timer/<string:name>")
def set_timer(name: str):
    bulb = HomeBulb(name)
    msg = bulb.set_timier()
    return create_response(msg, bulb)


@bulb.route("/set-color/<string:name>")
def set_color(name: str):
    red = 252
    green = 3
    blue = 115
    brightness = 40
    bulb = HomeBulb(name)
    msg = bulb.set_color(red, green, blue, brightness)
    return create_response(msg, bulb)


def change_request(bulb: HomeBulb) -> Response:
    try:
        msg = bulb.on_off()
        response = create_response(msg, bulb)
    except BulbException:
        response = create_response("ERROR", bulb, HTTPStatus.INTERNAL_SERVER_ERROR)
    return response


def create_response(msg: str, bulb: HomeBulb, status: int = HTTPStatus.OK) -> Response:
    response = make_response(msg, status)
    response.mimetype = "text/plain"
    gunicorn_logger.info(f"{bulb.model.name} - {msg}")
    return response
