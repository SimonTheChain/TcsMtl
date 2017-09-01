import json
import os


def languages():
    directory = os.getcwd()

    with open(os.path.join(directory + os.sep, "converter/languages.json"), "r") as data:
        languages_dict = json.load(data)
    return print(languages_dict)
