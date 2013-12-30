#!/usr/bin/env python
"""The Planet Feed Aggregator"""

from distutils.core import setup


# version and url copied from planet.constants,
# but because __init__ imports dependencies we cannot import it here.

setup(name="planet-mars",
      version='3.0.0',
      description="A simpler but familiar Planet feed aggregator",
      author="Rob Galanakis",
      author_email="rob.galanakis@gmail.com",
      url='https://github.com/rgalanakis/planet-mars',
      license='Python',
      packages=["planet", "planet.tests"],
      install_requires=[
          'feedparser',
          'sanitize',
          'jinja2',
          ]
)
