#
# Config file for the TraDemGen Python package.
# It defines the following variables:
#  TRADEMGEN_PY_LIBRARY_DIRS - Python library directories for TraDemGen
#  TRADEMGEN_PY_LIBRARIES    - Python libraries to link against
#  TRADEMGEN_PY_EXECUTABLES  - Python binaries/executables

# Tell the user project where to find TraDemGen Python libraries
set (TRADEMGEN_PY_LIBRARY_DIRS "/Users/darnaud/dev/sim/metasim/workspace/src/trademgen/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/lib/python3.8/site-packages/pytrademgen")

# Library dependencies for TraDemGen (contains definitions for the TraDemGen
# IMPORTED targets)
include ("/Users/darnaud/dev/sim/metasim/workspace/src/trademgen/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/share/trademgen/CMake/trademgen-library-depends.cmake")
include ("/Users/darnaud/dev/sim/metasim/workspace/src/trademgen/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/share/trademgen/CMake/trademgen-python-library-depends.cmake")

# These are the TraDemGen IMPORTED targets, created by
# trademgen-python-library-depends.cmake
set (TRADEMGEN_PY_LIBRARIES pytrademgenlib)
set (TRADEMGEN_PY_EXECUTABLES pytrademgen)

