"""
To make release:
    python setup.py sdist
Installation:
    python setup.py install
"""
import sys
from distutils.core import setup
from setuptools import find_packages


package_data = {
    'gui_args_framework': [
        'ui/ArgsWindow.ui',
    ]
}


setup(
    name='gui_args_framework',
    version='1.0',
    packages=find_packages(),
    license=open('LICENSE.txt').read(),
    long_description=open('README.md').read(),
    install_requires=[
        'PyQt5==5.15.2',
        'PyQt5-sip==12.8.1',
    ],
    package_data=package_data,
)
