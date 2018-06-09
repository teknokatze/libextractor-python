#!/bin/env/python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = "Extractor",
    version = "0.7",

    packages = ['libextractor'],
    scripts = ['examples/extract.py'],

    # install_requires = ['ctypes >= 0.9'],

    # metadata for upload to PyPI
    author = "Bader Ladjemi, Christian Grothoff, Nils Gillmann (ng0)",
    author_email = "libextractor@gnu.org",
    description = "Python bindings for GNU libextractor",
    license = "GNU GPLv3+",
    keywords = "libextractor binding tag metadata",
    url = "https://www.gnu.org/s/libextractor/",
    long_description="""libextractor is a simple library for keyword extraction.  libextractor
does not support all formats but supports a simple plugging mechanism
such that you can quickly add extractors for additional formats, even
without recompiling libextractor. libextractor typically ships with a
dozen helper-libraries that can be used to obtain keywords from common
file-types.

libextractor is a part of the GNU project (https://www.gnu.org/).""",

    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU General Public License (GPL)',
                 'Operating System :: OS Independent',
                 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX',
                 'Topic :: System :: Filesystems',
                 'Topic :: Text Processing :: Filters'],

    platforms=['windows', 'Linux', 'MacOS X', 'Solaris', 'FreeBSD'],

)
