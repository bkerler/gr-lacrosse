find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_LACROSSE gnuradio-lacrosse)

FIND_PATH(
    GR_LACROSSE_INCLUDE_DIRS
    NAMES gnuradio/lacrosse/api.h
    HINTS $ENV{LACROSSE_DIR}/include
        ${PC_LACROSSE_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_LACROSSE_LIBRARIES
    NAMES gnuradio-lacrosse
    HINTS $ENV{LACROSSE_DIR}/lib
        ${PC_LACROSSE_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-lacrosseTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_LACROSSE DEFAULT_MSG GR_LACROSSE_LIBRARIES GR_LACROSSE_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_LACROSSE_LIBRARIES GR_LACROSSE_INCLUDE_DIRS)
