#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "pyrmollib" for configuration "Debug"
set_property(TARGET pyrmollib APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(pyrmollib PROPERTIES
  IMPORTED_LOCATION_DEBUG "/Users/darnaud/dev/sim/metasim/workspace/src/rmol/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/lib/python3.8/site-packages/pyrmol/pyrmol.1.00.6.so"
  IMPORTED_SONAME_DEBUG "@rpath/pyrmol.1.00.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS pyrmollib )
list(APPEND _IMPORT_CHECK_FILES_FOR_pyrmollib "/Users/darnaud/dev/sim/metasim/workspace/src/rmol/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/lib/python3.8/site-packages/pyrmol/pyrmol.1.00.6.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
