# -*- coding: utf-8 -*-
import os
import yaml


def get_config():
    if os.path.isfile('config.yml'):
        with open('config.yml') as configfile:
            return yaml.load(configfile)
    return {}
