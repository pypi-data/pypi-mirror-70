#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "rmollib" for configuration "Debug"
set_property(TARGET rmollib APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(rmollib PROPERTIES
  IMPORTED_LOCATION_DEBUG "/Users/darnaud/dev/sim/metasim/workspace/src/rmol/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/lib/librmol.1.00.6.dylib"
  IMPORTED_SONAME_DEBUG "@rpath/librmol.1.00.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS rmollib )
list(APPEND _IMPORT_CHECK_FILES_FOR_rmollib "/Users/darnaud/dev/sim/metasim/workspace/src/rmol/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/lib/librmol.1.00.6.dylib" )

# Import target "rmolbin" for configuration "Debug"
set_property(TARGET rmolbin APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(rmolbin PROPERTIES
  IMPORTED_LOCATION_DEBUG "/Users/darnaud/dev/sim/metasim/workspace/src/rmol/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/bin/rmol"
  )

list(APPEND _IMPORT_CHECK_TARGETS rmolbin )
list(APPEND _IMPORT_CHECK_FILES_FOR_rmolbin "/Users/darnaud/dev/sim/metasim/workspace/src/rmol/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/bin/rmol" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
