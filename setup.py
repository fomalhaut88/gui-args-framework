"""
To make release:
    python setup.py sdist
Installation:
    python setup.py install
"""
from distutils.core import setup
from setuptools import find_packages


setup(
    name='gui_args_framework',
    version='1.1',
    packages=find_packages(),
    license=open('LICENSE.txt').read(),
    long_description=open('README.md').read(),
    install_requires=[
        'PyQt5==5.15.4',
        'PyQt5-Qt5==5.15.2',
        'PyQt5-sip==12.9.0',
    ],
)
