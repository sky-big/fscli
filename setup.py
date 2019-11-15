# -*- coding: utf-8 -*-

import io
import re
import os
from setuptools import setup, find_packages


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', os.linesep)
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


def read_requirements(req='base.txt'):
    content = read(os.path.join("requirements", req))
    return [line for line in content.split(os.linesep)
            if not line.strip().startswith('#')]


def read_version():
    content = read(os.path.join(
        os.path.dirname(__file__), 'fscli', '__init__.py'))
    return re.search(r"__version__ = \"([^']+)\"", content).group(1)


cmd_name = "fs"

setup(
    name='jdcloud-fs-cli',
    version=read_version(),
    packages=find_packages(),
    description='This is a local tools for JDCloud Function Service.',
    long_description=io.open('README.md', encoding='utf-8').read(),
    author='JD Cloud',
    url='https://github.com/sky-big/fscli.git',
    maintainer_email="xuxingwen@jd.com",
    license="Apache License 2.0",
    python_requires='>=2.7, <=4.0, !=4.0',
    entry_points={
        'console_scripts': [
            '{}=fscli.cli.main:cli'.format(cmd_name)
        ]
    },
    install_requires=read_requirements('base.txt'),
    include_package_data=True,
)
