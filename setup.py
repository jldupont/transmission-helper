#!/usr/bin/env python
"""
    Setup script for 'transmission-helper'

    @author: Jean-Lou Dupont
"""
__author__  ="Jean-Lou Dupont"
__version__ ="0.4"

from distutils.core import setup
from setuptools import find_packages

setup(name=         'transmission-helper',
      version=      __version__,
      description=  'Helper scripts for BT Transmission',
      author=       __author__,
      author_email= 'jl@jldupont.com',
      url=          'http://www.systemical.com/',
      package_dir=  {'': "src",},
      packages=     ["transmission_helper"],
      scripts=      ['src/scripts/trns-remove', ],
      )
