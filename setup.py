#!/usr/bin/env python3

from setuptools import setup, find_packages

README = 'README.md'


def long_desc():
    try:
        import pypandoc
    except ImportError:
        with open(README) as f:
            return f.read()
    else:
        return pypandoc.convert(README, 'rst')

setup(
    name='scalp',
    version='1',
    description='Snowflake Calender PagerDuty',
    url='https://github.com/snowflakedb/calendar/',
    long_description=long_desc(),
    packages=find_packages(),
    test_suite='test',
    install_requires=[
        'google-api-python-client',
        'pygerduty',
        'shellish==2.1',
        'pyyaml',
    ],
    entry_points = {
        'console_scripts': ['scalp=scalp.main:main'],
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
