import os
import sys

from distutils.core import setup

setup(name='cf_diff',
      version='0.0.0',
      description='Cloud Formation Diff Tool',
      maintainer='Andrew Butcher',
      maintainer_email='abutcher@redhat.com',
      license='GPLv3+',
      package_dir={ 'cf_diff': 'cf_diff' },
      packages=[
         'cf_diff',
         'cf_diff.parser'
      ],
      scripts=[
         'bin/cf-diff'
      ]
)
