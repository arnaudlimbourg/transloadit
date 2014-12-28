from setuptools import setup, find_packages, Command
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()


class PyTest(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        import subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

setup(
    name='transloadit',
    version='0.1.0',
    description='Client for the transloadit service',
    long_description=long_description,
    url='https://github.com/arnaudlimbourg/transloadit',
    author='Arnaud Limbourg',
    author_email='arnaud@limbourg.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='transloadit',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['requests==2.5.1'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage', 'pytest'],
    },
    cmdclass={'test': PyTest},
)
