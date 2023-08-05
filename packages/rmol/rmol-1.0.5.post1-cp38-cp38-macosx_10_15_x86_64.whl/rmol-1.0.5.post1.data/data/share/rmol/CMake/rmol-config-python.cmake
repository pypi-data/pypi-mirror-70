#
# Config file for the RMOL Python package. It defines the following variables:
#  RMOL_PY_LIBRARY_DIRS - Python library directories for RMOL
#  RMOL_PY_LIBRARIES    - Python libraries to link against
#  RMOL_PY_EXECUTABLES  - Python binaries/executables
#

# Tell the user project where to find RMOL Python libraries
set (RMOL_PY_LIBRARY_DIRS "/Users/darnaud/dev/sim/metasim/workspace/src/rmol/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/lib/python3.8/site-packages/pyrmol")

# Library dependencies for RMOL (contains definitions for the RMOL IMPORTED
# targets)
include ("/Users/darnaud/dev/sim/metasim/workspace/src/rmol/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/share/rmol/CMake/rmol-library-depends.cmake")
include ("/Users/darnaud/dev/sim/metasim/workspace/src/rmol/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/share/rmol/CMake/rmol-python-library-depends.cmake")

# These are the RMOL IMPORTED targets, created
# by rmol-python-library-depends.cmake
set (RMOL_PY_LIBRARIES pyrmollib)
set (RMOL_PY_EXECUTABLES pyrmol)

