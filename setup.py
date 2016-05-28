import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

tests_require = ['pytest', 'coverage == 3.7.1', 'coveralls == 0.5']

with open('requirements.txt') as f:
    install_requires = [l.strip() for l in f if l.strip()]

class PyTest(TestCommand):

    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

VERSION = '0.0.1'

setup(
    name = "PyBayes",
    version = VERSION,
    author = "Nathan Pucheril & Keith Hardaway",
    author_email = 'nathanpucheril@gmail.com | keithhardaway1@gmail.com',
    description = ("simple BayesNet Modeler"),
    license = "Apache",
    url = "https://github.com/nathanpucheril/PyBayes",
    packages = ['PyBayes'],
    cmdclass = {'test': PyTest},
    tests_require = tests_require,
    install_requires = install_requires + tests_require,
    classifiers = [
        "Topic :: Utilities",
        "Intended Audience :: Data Scientists",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
    ],
)
