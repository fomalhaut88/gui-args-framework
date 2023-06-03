from setuptools import find_packages, setup

from gui_args_framework.version import __version__


with open('README.md') as f:
    long_description = f.read()


setup(
    name='gui_args_framework',
    version=__version__,
    packages=find_packages(),
    license="Free",
    description="A framework to create a GUI for a Python console application.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'PyQt5>=5.15',
        'PyQt5-Qt5>=5.15',
        'PyQt5-sip>=12.9',
    ],
)
