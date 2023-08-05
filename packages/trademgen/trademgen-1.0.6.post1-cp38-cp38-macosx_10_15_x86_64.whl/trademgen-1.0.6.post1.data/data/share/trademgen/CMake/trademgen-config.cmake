#
# Config file for the TraDemGen package. It defines the following variables:
#  TRADEMGEN_VERSION         - version of TraDemGen
#  TRADEMGEN_BINARY_DIRS     - binary directories for TraDemGen
#  TRADEMGEN_INCLUDE_DIRS    - include directories for TraDemGen
#  TRADEMGEN_LIBRARY_DIRS    - library directories for TraDemGen (normally not used!)
#  TRADEMGEN_LIBEXEC_DIR     - internal exec directory for TraDemGen
#  TRADEMGEN_LIBRARIES       - libraries to link against
#  TRADEMGEN_EXECUTABLES     - the TraDemGen binaries/executables

# Tell the user project where to find TraDemGen headers and libraries
set (TRADEMGEN_VERSION "1.00.6")
set (TRADEMGEN_BINARY_DIRS "/Users/darnaud/dev/sim/metasim/workspace/src/trademgen/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/bin")
set (TRADEMGEN_INCLUDE_DIRS "/Users/darnaud/dev/sim/metasim/workspace/src/trademgen/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/include")
set (TRADEMGEN_LIBRARY_DIRS "/Users/darnaud/dev/sim/metasim/workspace/src/trademgen/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/lib")
set (TRADEMGEN_LIBEXEC_DIR "/Users/darnaud/dev/sim/metasim/workspace/src/trademgen/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/")

# Library dependencies for TraDemGen (contains definitions for the TraDemGen
# IMPORTED targets)
include ("/Users/darnaud/dev/sim/metasim/workspace/src/trademgen/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/share/trademgen/CMake/trademgen-library-depends.cmake")

# These are the TraDemGen IMPORTED targets, created by
# trademgen-library-depends.cmake
set (TRADEMGEN_LIBRARIES trademgenlib)
set (TRADEMGEN_EXECUTABLES trademgen
  trademgen_generateDemand
  trademgen_extractBookingRequests trademgen_drawBookingArrivals)

