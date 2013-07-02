__author__ = 'charlie'


import codecs
import json
import os
config = dict()
error_code = dict()

network_target_ids = []


def load_json_file(path):

    print path
    f = codecs.open(os.path.join(os.path.dirname(os.path.dirname(__file__)), path), 'r', 'UTF-8')
    config_text = f.read()
    f.close()
    return json.loads(config_text)


def load_config():

    path = 'fetch/config.json'

    return load_json_file(path)


def load_error_code():

    path = 'fetch/error_code.json'

    return load_json_file(path)


def load_network_target_id():

    f = codecs.open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "fetch/person_info"), 'r', 'UTF-8')

    ids = []

    for l in f:
        id = l.split(" ")[0]
        ids.append(id)

    f.close()

    return ids


config = load_config()

error_code = load_error_code()

network_target_ids = load_network_target_id()