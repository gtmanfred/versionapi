# -*- coding: utf-8 -*-
import celery
import importlib
import os

import versionapi.config

tasks = celery.Celery(
    'tasks',
    backend='db+postgresql://daniel:braves123@postgres/version',
    broker='pyamqp://daniel:braves123@rabbitmq//',
)
tasks.conf.update(versionapi.config.get_config())


curdir = os.path.dirname(__file__)
with os.scandir(f'{curdir}/tasks/') as rit:
    for entry in rit:
        if not entry.name[0].startswith('__') and entry.is_file():
            name = entry.name[:-3]
            spec = importlib.util.spec_from_file_location(f'versionapi.tasks.{name}', entry.path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)


if __name__ == '__main__':
    tasks.start()
