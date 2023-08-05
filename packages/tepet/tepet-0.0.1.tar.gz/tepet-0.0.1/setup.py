#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['tepet']

package_data = \
{'': ['*']}

setup(name='tepet',
      version='0.0.1',
      description='Small timing tool to run performance analysis',
      author='Anton Ovinnikov',
      author_email='toshakins@gmail.com',
      url='https://github.com/toshakins/tepet',
      packages=packages,
      package_data=package_data,
      python_requires='>= 3.5',
     )
