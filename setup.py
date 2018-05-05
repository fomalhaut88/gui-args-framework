"""
To make release:
    python setup.py sdist
Installation:
    python setup.py install
"""
import sys
from distutils.core import setup
from setuptools import find_packages


setup(
    name='gui-args-framework',
    version='1.0',
    packages=find_packages(),
    license=open('LICENSE.txt').read(),
    long_description=open('README.md').read(),
    data_files=[('ui', ['ui/ArgsWindow.ui'])],
    install_requires=[
        'PyQt5==5.8.2',
    ],
)
