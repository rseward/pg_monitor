#!/usr/bin/env python

from distutils.core import setup
#from setuptools import setup, find_packages

setup(name='pg_monitor',
      version='0.2',
      description='Bluestone PG Monitor',
      author='Robert Seward',
      author_email='rseward@bluestone-consulting.com',
      url='http://www.bluestone-consulting.com/',
      # python package dirs will require at a minimum an empty __init__.py file
      #   in them.
      packages=['bluestone', 'bluestone.pgmonitor'],
      scripts=['scripts/pg_monitor','scripts/deploy-pgmon-init-scripts'],
      package_dir={'bluestone':'src/bluestone'}
    )
