# -*- coding: utf-8 -*-
import os
import yaml


def get_config():
    return {
        'CELERY_TRACK_STARTED': True,
        'BROKER_URL': os.environ.get('BROKER', 'pyamqp://daniel:braves123@rabbitmq//'),
        'CELERY_RESULT_BACKEND': os.environ.get('BACKEND', 'db+postgresql://daniel:braves123@postgres/version'),
    }
