include ${MPCMAKE_PATH}/latest/MakePythonPackage

MODULE = buscador_de_cosas_houdini
VERSION = 1.1.0
BUILD_FOR = c6houdini2015
AUTHORS = adam-lev
MAILTO = adam-lev@technicolor.com
DESCRIPTION = A Qt UI Debugger (Houdini)


ION_ONLY = 1

ENABLE_DEPENDENCY_TYPES = 1
DEPENDENCIES = \
	Python
RUNTIME_DEPENDENCIES = \
	houdini \
	mpc.tvcQtCore \
	QtPy

##################################################################
# python
##################################################################
python.PYTHON_ROOT = python
${call MakePythonPackage,python}
