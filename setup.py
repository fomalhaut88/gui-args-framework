from setuptools import setup


with open('README.md') as f:
    long_description = f.read()


setup(
    name='gui-args-framework',
    version='1.3.0',
    packages=['gui_args_framework'],
    author="Alexander Fomalhaut",
    url="https://github.com/fomalhaut88/gui-args-framework",
    project_urls={
        "Homepage": "https://pypi.org/project/gui-args-framework/",
        "Documentation": "https://fomalhaut88.github.io/gui-args-framework/",
        "Source": "https://github.com/fomalhaut88/gui-args-framework",
        "Issues": "https://github.com/fomalhaut88/gui-args-framework/issues",
    },
    license="MIT",
    description="A framework to create a GUI for a Python console application.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'PyQt5>=5.15',
    ],
    python_requires=">=3.12",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="gui qt",
)
