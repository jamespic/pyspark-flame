#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pyspark-flame',
    version='0.2.0',
    description='A low-overhead sampling profiler for PySpark, that outputs Flame Graphs',
    author='James Pickering',
    author_email='james_pic@hotmail.com',
    license='MIT',
    url='https://github.com/jamespic/pyspark-flame',
    download_url='https://github.com/jamespic/pyspark-flame/archive/0.1.2.tar.gz',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    scripts=['FlameGraph/flamegraph.pl'],
    test_suite='test'
)
