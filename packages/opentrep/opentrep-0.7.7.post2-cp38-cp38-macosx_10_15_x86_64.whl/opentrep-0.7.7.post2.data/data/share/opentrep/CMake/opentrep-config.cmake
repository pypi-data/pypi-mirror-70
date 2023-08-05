#
# Config file for the OpenTrep package. It defines the following variables:
#  OPENTREP_VERSION         - version of OpenTrep
#  OPENTREP_BINARY_DIRS     - binary directories for OpenTrep
#  OPENTREP_INCLUDE_DIRS    - include directories for OpenTrep
#  OPENTREP_LIBRARY_DIRS    - library directories for OpenTrep
#  OPENTREP_PY_LIBRARY_DIRS - Python library directories for OpenTrep
#  OPENTREP_LIBEXEC_DIR     - internal exec directory for OpenTrep
#  OPENTREP_LIBRARIES       - libraries to link against
#  OPENTREP_PY_LIBRARIES    - Python libraries to link against
#  OPENTREP_EXECUTABLES     - binaries/executables
#  OPENTREP_PY_EXECUTABLES  - Python binaries/executables
#  OPENTREP_SAMPLE_DIR      - directory for sample data files
#

# Tell the user project where to find OpenTrep headers and libraries
set (OPENTREP_VERSION "0.07.7")
set (OPENTREP_BINARY_DIRS "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/bin")
set (OPENTREP_INCLUDE_DIRS "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/include")
set (OPENTREP_LIBRARY_DIRS "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/lib")
set (OPENTREP_PY_LIBRARY_DIRS "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/lib/python3.8/site-packages/pyopentrep")
set (OPENTREP_LIBEXEC_DIR "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/")
set (OPENTREP_SAMPLE_DIR "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/share/opentrep/data")

# Library dependencies for OpenTrep (contains definitions for the OpenTrep
# IMPORTED targets)
include ("/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/share/opentrep/CMake/opentrep-library-depends.cmake")

# These are the OpenTrep IMPORTED targets, created by
# opentrep-library-depends.cmake
set (OPENTREP_LIBRARIES opentreplib)
set (OPENTREP_PY_LIBRARIES pyopentreplib)
set (OPENTREP_EXECUTABLES opentrep)
set (OPENTREP_PY_EXECUTABLES pyopentrep)

