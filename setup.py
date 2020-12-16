#!/usr/bin/env python
from setuptools import setup, find_packages
long_description = open('README.md').read()

setup(
    name='pyspark-flame',
    description='A low-overhead sampling profiler for PySpark, that outputs Flame Graphs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='James Pickering',
    author_email='james_pic@hotmail.com',
    license='MIT',
    url='https://github.com/jamespic/pyspark-flame',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    scripts=['FlameGraph/flamegraph.pl'],
    install_requires=['pyspark'],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    test_suite='test',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
