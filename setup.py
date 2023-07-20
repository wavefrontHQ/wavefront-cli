"""Packaging settings."""

import os
import subprocess

import setuptools


this_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(setuptools.Command):
    """Run all tests."""

    description = 'run tests'
    user_options = []

    def initialize_options(self):
        """Skip this test case."""

    def finalize_options(self):
        """Skip this test case."""

    def run(self):
        """Run all tests."""
        errno = subprocess.call(['py.test', '--cov=wave',
                                 '--cov-report=term-missing'])
        raise SystemExit(errno)


setuptools.setup(
    name='wavefront-cli',
    version='0.1.2',
    description='VMware Aria Operations for Applications CLI Utility.',
    long_description=long_description,
    url='https://github.com/wavefrontHQ/wavefront-cli',
    author='VMware Aria Operations for Applications Team',
    author_email='chitimba@wavefront.com',
    license='APACHE-V2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: Utilities',
    ],
    keywords=['apps', 'cli', 'lib', 'observability', 'ops', 'wavefront'],
    packages=setuptools.find_packages(exclude=['docs', 'tests*']),
    # packages=['wave'],
    install_requires=('boto3', 'distro', 'docopt', 'requests'),
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
