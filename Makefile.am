all:
	python libextractor_python_setup.py $(EXT_LIB_PATH) build
install-exec-local:
	python libextractor_python_setup.py $(EXT_LIB_PATH) install --prefix=$(PYTHON_PREFIX)
EXTRA_DIST = \
  extract.py \
  libextractor_python_setup.py \
  libextractor_python.c \
  Extractor.py \
  README.debian