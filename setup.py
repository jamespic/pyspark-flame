#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='PySpark Flame',
    version='0.1.0',
    description='A low-overhead sampling profiler for PySpark, that outputs Flame Graphs',
    author='James Pickering',
    author_email='james_pic@hotmail.com',
    license='MIT',
    url='https://github.com/jamespic/pyspark-flame',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    test_suite='test'
)
