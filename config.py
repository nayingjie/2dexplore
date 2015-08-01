import json
import os.path

CONFIG_FILENAME = "config.json"

conf = {}


def load():
    global conf
    if os.path.isfile(CONFIG_FILENAME):
        print "Config present, loading."
        config_file = open(CONFIG_FILENAME)
        conf = json.load(config_file)
        config_file.close()
    else:
        print "No config present, creating one."
        config_file = open(CONFIG_FILENAME, "w")
        json.dump(conf, config_file)
        config_file.flush()
        config_file.close()

def save():
    global conf
    config_file = open(CONFIG_FILENAME, "w")
    json.dump(conf, config_file)
    config_file.flush()
    config_file.close()

def get_config():
    global conf
    return  conf