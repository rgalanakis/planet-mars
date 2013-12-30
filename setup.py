#!/usr/bin/env python
"""The Planet Feed Aggregator"""

from distutils.core import setup
from planet.constants import __version__, __url__

setup(name="planet-mars",
      version=__version__,
      description="A simpler but familiar Planet feed aggregator",
      author="Rob Galanakis",
      author_email="rob.galanakis@gmail.com",
      url=__url__,
      license='Python',
      packages=["planet", "planet.tests"],
      install_requires=[
          'feedparser',
          'sanitize',
          'jinja2',
          ]
)
