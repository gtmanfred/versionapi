#!/usr/bin/env python

from distutils.core import setup
import distutils.dist
from distutils.command.install_data import install_data

import os

packages = ['versionapi']

with os.scandir('versionapi') as rit:
    for entry in rit:
        if entry.name[0] not in ('.', '_') and entry.is_dir() \
                and os.path.isfile(f'{entry.path}/__init__.py'):
            packages.append(f'{entry.path.replace("/", ".")}')


class VersionInstallData(install_data):
    def run(self):
        install_data.run(self)
        if os.environ.get('DEVEL', False):
            return
        for pkgfile in self.outfiles:
            with open(pkgfile, 'r') as tmpfile:
                filedata = tmpfile.read()
            filedata = filedata.replace(
                'localhost',
                'versions.gtmanfred.com'
            )
            with open(pkgfile, 'w') as tmpfile:
                print(filedata, file=tmpfile)


class VersionDist(distutils.dist.Distribution):
    def __init__(self, attrs=None):
        distutils.dist.Distribution.__init__(self, attrs)
        self.cmdclass.update({'install_data': VersionInstallData})

setup(
    distclass=VersionDist,
    name='versionapi',
    version='0.2.0',
    description='Version Checker API',
    author='Daniel Wallace',
    author_email='daniel@gtmanfred.com',
    url='https://github.com/gtmanfred/versionapi',
    packages=packages,
    include_package_data=True,
    data_files=[
        ('share/nginx/html/', [f'versionapi/html/{webfile}' for webfile in ['index.html', 'main.js', 'main.css']]),
    ],
)
