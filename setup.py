#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

from setuptools import setup, find_packages

full_version = ''

root_dir = os.path.abspath(os.path.dirname(__file__))

readme_file = os.path.join(root_dir, 'README.rst')
with open(readme_file, encoding='utf-8') as f:
    long_description = f.read()

version_module = os.path.join(root_dir, 'src', 'kchatdriver', 'version.py')
with open(version_module, encoding='utf-8') as f:
    exec(f.read())

setup(
    name='kchatdriver',
    version=full_version,
    description='A Python kChat Driver',
    long_description=long_description,
    url='https://github.com/infomaniak/python-kchat-driver',
    author='Léopold Jacquot',
    author_email='leopold.jacquot@gmail.com',
    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    python_requires=">=3.7",
    install_requires=[
        'requests~=2.27.1',
        'pusher~=3.3.0',
        'pysher~=1.0.8',
    ],
)
