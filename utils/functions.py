import configparser


'''Config'''


def get_config(section="driver", key=""):
    config = configparser.RawConfigParser()
    config.read("setup.cfg")
    return config.get(section, key)

