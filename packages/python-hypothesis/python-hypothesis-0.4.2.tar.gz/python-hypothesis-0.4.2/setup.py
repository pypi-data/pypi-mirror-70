#!/usr/bin/python

# See file COPYING distributed with python-hypothesis for copyright and 
# license.

from setuptools import setup

long_description = open('README.rst').read()

setup(name='python-hypothesis', 
      version='0.4.2', 
      description='Python library for the Hypothes.is API', 
      author='Christian Haselgrove', 
      author_email='christian.haselgrove@umassmed.edu', 
      url='https://github.com/chaselgrove/python-hypothesis', 
      packages=['h_annot'], 
      scripts=[], 
      install_requires=['requests', 
                        'python-dateutil',
                        'six'], 
      classifiers=['Development Status :: 3 - Alpha', 
                   'Environment :: Web Environment', 
                   'Intended Audience :: Developers', 
                   'License :: OSI Approved :: BSD License', 
                   'Natural Language :: English', 
                   'Operating System :: OS Independent', 
                   'Programming Language :: Python', 
                   'Topic :: Internet :: WWW/HTTP', 
                   'Topic :: Software Development :: Libraries'], 
      license='BSD license', 
      long_description=long_description
     )

# eof
