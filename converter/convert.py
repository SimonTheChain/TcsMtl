import json
import os
from operator import itemgetter


def create_languages():
    directory = os.getcwd()

    with open(os.path.join(directory + os.sep, "converter" + os.sep + "languages.json"), "r") as data:
        languages = [(key, val) for key, val in json.load(data).items()]
        languages.sort(key=itemgetter(1))
    return languages


def create_countries():
    directory = os.getcwd()

    with open(os.path.join(directory + os.sep, "converter" + os.sep + "countries.json"), "r") as data:
        countries = [(key, val) for key, val in json.load(data).items()]
        countries.sort(key=itemgetter(1))
    return countries
