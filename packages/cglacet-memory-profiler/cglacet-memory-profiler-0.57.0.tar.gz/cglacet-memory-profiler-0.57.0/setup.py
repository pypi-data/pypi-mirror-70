import os
import io
import re
from setuptools import find_packages, setup


# https://packaging.python.org/guides/single-sourcing-package-version/
def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)


CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.2
Programming Language :: Python :: 3.3
Topic :: Software Development
Operating System :: POSIX
Operating System :: Unix

"""


setup(
    name='cglacet-memory-profiler',
    description='A module for monitoring memory usage of a python program',
    long_description=open('README.rst').read(),
    version=find_version("memory_profiler", "__init__.py"),
    author='Fabian Pedregosa',
    author_email='f@bianp.net',
    url='https://github.com/pythonprofilers/memory_profiler',
    py_modules=['mprof'],
    packages=find_packages(include=('memory_profiler',)),
    entry_points={
        'console_scripts': ['mprof = mprof:main'],
    },
    install_requires=['psutil'],
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
    license='BSD'
)
