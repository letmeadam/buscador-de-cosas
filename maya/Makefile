include ${MPCMAKE_PATH}/latest/MakePythonPackage

MODULE = buscador_de_cosas_maya
VERSION = 1.1.0
BUILD_FOR = c6maya2015
AUTHORS = adam-lev
MAILTO = adam-lev@technicolor.com
DESCRIPTION = A Qt UI Debugger (Maya)


ION_ONLY = 1

ENABLE_DEPENDENCY_TYPES = 1
DEPENDENCIES = \
	Python
RUNTIME_DEPENDENCIES = \
	maya \
	mpc.tvcQtCore \
	mpc.tvcUtils \
	QtPy

##################################################################
# python
##################################################################
python.PYTHON_ROOT = python
${call MakePythonPackage,python}
