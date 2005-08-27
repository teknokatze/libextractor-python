from distutils.core import Extension, setup
import sys

path=sys.argv[1]
sys.argv = sys.argv[1:]

cmod = Extension("extractor",["libextractor_python.c"],
                 libraries=["extractor"],
                 include_dirs=[path + "/include"],
                 library_dirs=[path + "/lib"])

setup(name="Extractor",
      version="0.5.4",
      ext_modules=[cmod],
      author="Christian Grothoff, Heiko Wundram",
      author_email="libextractor@gnu.org")

