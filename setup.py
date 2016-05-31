# coding: utf-8
from setuptools import setup
from wolframalpha import __version__


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name="wolframalpha-cli",
    version=__version__,
    author="Fernando Xavier de Freitas Crespo",
    author_email="fernando82@gmail.com",
    description=("Command Line Interface to run queries on WolframAlpha"),
    long_description=read('README.md'),
    license=read('LICENSE'),
    keywords="wolframalpha cli python utility",
    url="https://github.com/fcrespo82/wolframalpha-cli",
    packages=['wolframalpha'],
    package_data={'wolframalpha': ['data/config.yaml']},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=open('requirements.txt').readlines(),
    entry_points={
        'console_scripts': [
            'wolframalpha-cli = wolframalpha.wolframalpha:main',
            'wa-cli = wolframalpha.wolframalpha:main'
        ]
    },
)
