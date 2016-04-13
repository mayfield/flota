#!/usr/bin/env python3

from setuptools import setup, find_packages

README = 'README.md'

with open('requirements.txt') as f:
    requirements = f.readlines()


def long_desc():
    try:
        import pypandoc
    except ImportError:
        with open(README) as f:
            return f.read()
    else:
        return pypandoc.convert(README, 'rst')

setup(
    name='flota',
    version='0',
    description='Spanish for fleet - A Docker CLI',
    url='https://github.com/mayfield/flota/',
    long_description=long_desc(),
    packages=find_packages(),
    test_suite='test',
    install_requires=requirements,
    entry_points = {
        'console_scripts': ['flota=flota.main:main'],
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
    ]
)
