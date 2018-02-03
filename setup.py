#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'click>=6.0',
    'user_agent',
    'fastcache',
    'requests',
    'pyquery',
    'pandas',
    'tqdm',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

from mooquant_sina import __version__

setup(
    name='mooquant_sina',
    version=__version__,
    description="",
    long_description=readme + '\n\n' + history,
    author="bopowang",
    author_email='ibopo@126.com',
    url='https://github.com/bopo/mooquant_sina',
    packages=find_packages(include=['mooquant_sina', 'mooquant_sina.*']),
    entry_points={
        'console_scripts': [
            'mooquant_sina=mooquant_sina.cli:main',
            'mq=mooquant_sina.cli:main',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='mooquant_sina',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
