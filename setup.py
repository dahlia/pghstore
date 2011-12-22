import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import pghstore


try:
    readme_f = open('README.rst')
    long_description = readme_f.read()
    readme_f.close()
except IOError:
    long_description = None

if sys.version_info < (2, 6):
    tests_require = ['simplejson']
else:
    tests_require = None


setup(name='pghstore',
      py_modules=['pghstore'],
      version=pghstore.__version__,
      description='PostgreSQL hstore formatter',
      long_description=long_description,
      license='MIT License',
      author='Hong Minhee',
      author_email='dahlia' '@' 'stylesha.re',
      maintainer='StyleShare',
      maintainer_email='dev' '@' 'stylesha.re',
      url='http://styleshare.github.com/pghstore/',
      test_suite='pghstoretests.tests',
      tests_require=tests_require,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Stackless'
      ])
