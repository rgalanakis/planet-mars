#!/usr/bin/env python
"""The Planet Feed Aggregator"""

from distutils.core import setup
from planet.constants import __version__, __url__

setup(name="planet-techart",
      version=__version__,
      description="The Tech Art Planet Feed Aggregator",
      author="Rob Galanakis",
      author_email="rob.galanakis@gmail.com",
      url=__url__,
      license='Python',
      packages=["planet", "planet.tests"],
      scripts=["make_techart.py"],
      install_requires=[
          'feedparser',
          'sanitize',
          'jinja2',
          ]
)
