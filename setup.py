#!/usr/bin/env python
"""The Planet Feed Aggregator"""

from distutils.core import setup
from planet import __version__

setup(name="planet-techart",
      version=__version__,
      description="The Tech Art Planet Feed Aggregator",
      author="Rob Galanakis",
      author_email="rob.galanakis@gmail.com",
      url="http://www.robg3d.com/",
      license='Python',
      packages=["planet", "planet.tests"],
      scripts=["planet.py"],
      install_requires=[
          'feedparser',
          'sanitize',
          ]
)
