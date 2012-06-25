try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
import distutils.cmd
import os
import os.path
import shutil
import sys
import tempfile

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


class upload_doc(distutils.cmd.Command):
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


cpghstore = Extension(
    'cpghstore', sources=['cpghstore.c'], extra_compile_args=['-O3']
)


setup(name='pghstore',
      py_modules=['pghstore', '_pghstore'],
      ext_modules=[cpghstore],
      version=pghstore.__version__,
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
      cmdclass={'upload_doc': upload_doc},
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
      ])

