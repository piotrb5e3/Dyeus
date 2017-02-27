import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'pytest'
]

setup(name='dyeus',
      version='0.0.2',
      author='Piotr Bakalarski',
      author_email='piotrb5e3@gmail.com',
      license='GPLv3',
      description=(
          'Dyeus is a web application for gathering and displaying sensory '
          'data, and making recommendations based on preset rules.'),
      long_description=read('README.md'),
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = dyeus:main
      """,
      )
