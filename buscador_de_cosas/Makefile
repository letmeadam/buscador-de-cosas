include ${MPCMAKE_PATH}/latest/MakePythonPackage

MODULE = buscador_de_cosas
VERSION = 1.1.1
BUILD_FOR = c6maya2015
AUTHORS = adam-lev
MAILTO = adam.levasseur@technicolor.com
DESCRIPTION = A Qt UI Debugger


ION_ONLY = 1

ENABLE_DEPENDENCY_TYPES = 1
DEPENDENCIES = \
	Python
RUNTIME_DEPENDENCIES = \
	mpc.tvcQtCore \
	python-six \
	QtPy

##################################################################
# python
##################################################################
python.PYTHON_ROOT = python
${call MakePythonPackage,python}
