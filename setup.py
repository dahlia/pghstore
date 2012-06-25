from distutils.cmd import Command
from distutils.command.build_ext import build_ext
from distutils.errors import (CCompilerError, DistutilsExecError,
                              DistutilsPlatformError)
import os
import os.path
import shutil
import sys
import tempfile

from setuptools import Extension, Feature, setup

from pghstore.version import VERSION


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


class upload_doc(Command):
    """Uploads the documentation to GitHub pages."""

    description = __doc__
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        path = tempfile.mkdtemp()
        build = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'build', 'sphinx', 'html')
        os.chdir(path)
        os.system('git clone git@github.com:dahlia/pghstore.git .')
        os.system('git checkout gh-pages')
        os.system('git rm -r .')
        os.system('touch .nojekyll')
        os.system('cp -r ' + build + '/* .')
        os.system('git stage .')
        os.system('git commit -a -m "Documentation updated."')
        os.system('git push origin gh-pages')
        shutil.rmtree(path)


# Most of the following codes to allow C extension building to fail were
# copied from MarkupSafe's setup.py script.
# https://github.com/mitsuhiko/markupsafe/blob/master/setup.py

is_jython = 'java' in sys.platform
is_pypy = hasattr(sys, 'pypy_version_info')


speedups = Feature(
    'optional C speed-enhancement module',
    standard=True,
    available=not (is_jython or is_pypy),
    ext_modules=[
        Extension('pghstore._speedups', ['pghstore/_speedups.c'],
                  extra_compile_args=['-O3'])
    ]
)


ext_errors = CCompilerError, DistutilsExecError, DistutilsPlatformError
if sys.platform == 'win32' and sys.version_info > (2, 6):
    # 2.6's distutils.msvc9compiler can raise an IOError when failing to
    # find the compiler
    ext_errors += (IOError,)


class BuildFailed(Exception):

    pass


class ve_build_ext(build_ext):
    """This class allows C extension building to fail."""

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError:
            raise BuildFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except ext_errors:
            raise BuildFailed()
        except ValueError:
            # this can happen on Windows 64 bit, see Python issue 7511
            if "'path'" in str(sys.exc_info()[1]): # works with Python 2 and 3
                raise BuildFailed()
            raise


def run_setup(with_speedups):
    setup(
        name='pghstore',
        packages=['pghstore'],
        features={'speedups': speedups} if with_speedups else {},
        version=VERSION,
        description='PostgreSQL hstore formatter',
        long_description=long_description,
        license='MIT License',
        author='Hong Minhee',
        author_email='minhee' '@' 'dahlia.kr',
        maintainer='Robert Kajic',
        maintainer_email='robert' '@' 'kajic.com',
        url='https://github.com/dahlia/pghstore',
        test_suite='pghstoretests.tests',
        tests_require=tests_require,
        platforms=['any'],
        cmdclass={
            'build_ext': ve_build_ext,
            'upload_doc': upload_doc
        },
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.5',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 2 :: Only',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Programming Language :: Python :: Implementation :: Stackless',
            'Topic :: Database',
            'Topic :: Software Development :: Libraries :: Python Modules'
        ]
    )


def try_building_extension():
    try:
        run_setup(True)
    except BuildFailed:
        print '=' * 74
        print 'WARNING: The C extension could not be compiled,',
        print 'speedups are not enabled.'
        print 'Failure information, if any, is above.'
        print 'Retrying the build without the C extension now.'
        print
        run_setup(False)
        print '=' * 74
        print 'WARNING: The C extension could not be compiled,',
        print 'speedups are not enabled.'
        print 'Plain-Python installation succeeded.'
        print '=' * 74


try_building_extension()

