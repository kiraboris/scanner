

from . import db
from .io import load_rotor, write_rotor


def name():
    return "Pickett"


def is_valid_extension(ext):
    return ext in db.MODEL_EXTENSIONS

