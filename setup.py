"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from wavefront_cli import __version__

this_dir = abspath(dirname(__file__))

with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""

    description = 'run tests'
    user_options = []

    def initialize_options(self):
        """Skip this test case."""
        pass

    def finalize_options(self):
        """Skip this test case."""
        pass

    def run(self):
        """Run all tests."""
        errno = call(['py.test', '--cov=wave', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name='wavefront-cli',
    version=__version__,
    description='Wavefront client CLI utility.',
    long_description=long_description,
    url='https://github.com/wavefrontHQ/wavefront-cli',
    author='Evan Pease',
    author_email='evan@wavefront.com',
    license='UNLICENSE',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords=['lib', 'cli'],
    packages=find_packages(exclude=['docs', 'tests*']),
    # packages=['wave'],
    install_requires=['docopt', 'requests', 'boto', 'distro'],
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'wave=wavefront_cli.cli:main',
        ],
    },
    cmdclass={'test': RunTests},
)
