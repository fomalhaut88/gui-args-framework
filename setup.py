"""
To make release:
    python setup.py sdist
Installation:
    python setup.py install
"""
from distutils.core import setup
from setuptools import find_packages

from gui_args_framework.version import __version__


setup(
    name='gui_args_framework',
    version=__version__,
    packages=find_packages(),
    license=open('LICENSE.txt').read(),
    long_description=open('README.md').read(),
    install_requires=[
        'PyQt5>=5.15',
        'PyQt5-Qt5>=5.15',
        'PyQt5-sip>=12.9',
    ],
)
