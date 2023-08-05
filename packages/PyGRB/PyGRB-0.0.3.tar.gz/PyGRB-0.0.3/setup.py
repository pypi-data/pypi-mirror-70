#!/usr/bin/env python

import setuptools

def get_long_description():
    with open('README.rst', 'r') as fh:
        text = fh.read()
    return text

def get_requirements():
    with open('requirements.txt', 'r') as f:
        text = f.read().splitlines()
    return text

long_description = get_long_description()
requirements = get_requirements()

setuptools.setup(
    name='PyGRB',
    version='0.0.3',
    author='James Paynter',
    author_email='jims.astronomy@gmail.com',
    description='A GRB light-curve analysis package.',
    license='BSD-3',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/JamesPaynter/PyGRB',
    packages=setuptools.find_packages(),
    package_dir = {'PyGRB' : 'PyGRB'},
    package_data={'PyGRB': ['data/*']},
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6.0, <3.9',
)
