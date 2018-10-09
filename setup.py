import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()


def get_version(filename):
    import ast
    version = None
    with open(filename) as f:
        for line in f:
            if line.startswith('__version__'):
                version = ast.parse(line).body[0].value.s
                break
        else:
            raise ValueError('No version found in %r.' % filename)
    if version is None:
        raise ValueError(filename)
    return version


version = get_version(filename='src/duckietown_data_client/__init__.py')

setup(name='duckietown-data-client',
      version=version,
      download_url='http://github.com/duckietown/duckietown-data-client/tarball/%s' % version,
      package_dir={'': 'src'},
      packages=find_packages('src'),
      install_requires=[
          'uptime',
      ],

      tests_require=[
      ],

      # This avoids creating the egg file, which is a zip file, which makes our data
      # inaccessible by dir_from_package_name()
      zip_safe=False,

      # without this, the stuff is included but not installed
      include_package_data=True,

      entry_points={
          'console_scripts': [
              'dt-dc = duckietown_data_client:main',
          ]
      }
      )
