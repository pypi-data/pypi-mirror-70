#
# Config file for the RMOL package. It defines the following variables:
#  RMOL_VERSION         - version of RMOL
#  RMOL_BINARY_DIRS     - binary directories for RMOL
#  RMOL_INCLUDE_DIRS    - include directories for RMOL
#  RMOL_LIBRARY_DIRS    - library directories for RMOL
#  RMOL_LIBEXEC_DIR     - internal exec directory for RMOL
#  RMOL_LIBRARIES       - libraries to link against
#  RMOL_EXECUTABLES     - the RMOL binaries/executables
#

# Tell the user project where to find RMOL headers and libraries
set (RMOL_VERSION "1.00.6")
set (RMOL_BINARY_DIRS "/Users/darnaud/dev/sim/metasim/workspace/src/rmol/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/bin")
set (RMOL_INCLUDE_DIRS "/Users/darnaud/dev/sim/metasim/workspace/src/rmol/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/include")
set (RMOL_LIBRARY_DIRS "/Users/darnaud/dev/sim/metasim/workspace/src/rmol/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/lib")
set (RMOL_LIBEXEC_DIR "/Users/darnaud/dev/sim/metasim/workspace/src/rmol/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/")

# Library dependencies for RMOL (contains definitions for the RMOL IMPORTED
# targets)
include ("/Users/darnaud/dev/sim/metasim/workspace/src/rmol/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/share/rmol/CMake/rmol-library-depends.cmake")

# These are the RMOL IMPORTED targets, created by rmol-library-depends.cmake
set (RMOL_LIBRARIES rmollib)
set (RMOL_EXECUTABLES rmol rmol_extractBPC rmol_drawBPC)
