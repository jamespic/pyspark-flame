#!/usr/bin/env python
from setuptools import setup, find_packages
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='pyspark-flame',
    version='0.2.5',
    description='A low-overhead sampling profiler for PySpark, that outputs Flame Graphs',
    long_description=long_description,
    author='James Pickering',
    author_email='james_pic@hotmail.com',
    license='MIT',
    url='https://github.com/jamespic/pyspark-flame',
    download_url='https://github.com/jamespic/pyspark-flame/archive/0.2.4.tar.gz',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    scripts=['FlameGraph/flamegraph.pl'],
    install_requires=['pyspark'],
    setup_requires=['pypandoc'],
    test_suite='test'
)
