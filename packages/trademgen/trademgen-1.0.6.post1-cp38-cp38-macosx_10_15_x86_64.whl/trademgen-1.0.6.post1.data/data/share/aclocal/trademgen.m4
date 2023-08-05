#
# Configure paths and flags for the TraDemGen library.
# Denis Arnaud <denis_arnaud at users dot sourceforge dot net>, July 2008
#
# Note: the TRADEMGEN library depends upon BOOST to build.
# Your configure.ac must therefore define appropriately the BOOST
# variables (i.e., BOOST_CFLAGS, BOOST_LIBS, BOOST_DATE_TIME_LIB).
#
# Variables set by this macro:
#  * TRADEMGEN_VERSION
#  * TRADEMGEN_CFLAGS
#  * TRADEMGEN_LIBS
#  * TRADEMGEN_SAMPLE_DIR
#

AC_DEFUN([AM_PATH_TRADEMGEN],
[
AC_LANG_SAVE
AC_LANG([C++])

##
AC_ARG_WITH(trademgen,
	[ --with-trademgen=PFX Prefix where TraDemGen is installed (optional) ],
	    trademgen_dir="$withval",
	    trademgen_dir="")

  if test "x${TRADEMGEN_CONFIG+set}" != xset ; then
     if test "x$trademgen_dir" != x ; then
         TRADEMGEN_CONFIG="$trademgen_dir/bin/trademgen-config"
     fi
  fi

  AC_PATH_PROG(TRADEMGEN_CONFIG, trademgen-config, no)

  ## Check whether Boost flags and libraries are defined
  # General Boost compilation flags
  AC_MSG_CHECKING(for BOOST_CFLAGS environment variable)
  if test x"${BOOST_CFLAGS}" = x; then
	AC_MSG_RESULT([Warning: TraDemGen needs Boost, and the BOOST_CFLAGS environment variable does not appear to be set. It may not be a problem, though, if your Unix distribution is standard, that is, if Boost is installed in /usr. Otherwise, the TraDemGen will fail to compile.])
  else
	AC_MSG_RESULT([ok (set to ${BOOST_CFLAGS})])
  fi

  # Boost Date-Time library
  AC_MSG_CHECKING(for BOOST_DATE_TIME_LIB environment variable)
  if test x"${BOOST_DATE_TIME_LIB}" = x; then
	AC_MSG_RESULT([Warning: TraDemGen needs the Boost Date-Time library, and the BOOST_DATE_TIME_LIB environment variable does not appears to be set. The TraDemGen may fail to link.])
  else
	AC_MSG_RESULT([ok (set to ${BOOST_DATE_TIME_LIB})])
  fi

  # Boost Program Options library
  AC_MSG_CHECKING(for BOOST_PROGRAM_OPTIONS_LIB environment variable)
  if test x"${BOOST_PROGRAM_OPTIONS_LIB}" = x; then
	AC_MSG_RESULT([Warning: TraDemGen needs the Boost Program Options library, and the BOOST_PROGRAM_OPTIONS_LIB environment variable does not appears to be set. The TraDemGen may fail to link.])
  else
	AC_MSG_RESULT([ok (set to ${BOOST_PROGRAM_OPTIONS_LIB})])
  fi

  # Boost File System library
  AC_MSG_CHECKING(for BOOST_FILESYSTEM_LIB environment variable)
  if test x"${BOOST_FILESYSTEM_LIB}" = x; then
	AC_MSG_RESULT([Warning: TraDemGen needs the Boost Date-Time library, and the BOOST_FILESYSTEM_LIB environment variable does not appears to be set. The TraDemGen may fail to link.])
  else
	AC_MSG_RESULT([ok (set to ${BOOST_FILESYSTEM_LIB})])
  fi

  ## TraDemGen version
  min_trademgen_version=ifelse([$1], ,0.1.0,$1)
  AC_MSG_CHECKING(for TraDemGen - version >= $min_trademgen_version)
  no_trademgen=""
  if test "${TRADEMGEN_CONFIG}" = "no" ; then
     no_trademgen=yes
     AC_MSG_RESULT([no])
  else
     TRADEMGEN_VERSION=`${TRADEMGEN_CONFIG} --version`
     TRADEMGEN_CFLAGS=`${TRADEMGEN_CONFIG} --cflags`
     TRADEMGEN_CFLAGS="${BOOST_CFLAGS} ${TRADEMGEN_CFLAGS}"
     TRADEMGEN_LIBS=`${TRADEMGEN_CONFIG} --libs`
     TRADEMGEN_LIBS="${BOOST_LIBS} ${BOOST_DATE_TIME_LIB} ${TRADEMGEN_LIBS}"
     TRADEMGEN_SAMPLE_DIR=`${TRADEMGEN_CONFIG} --sampledir`

     AC_SUBST([TRADEMGEN_VERSION])
     AC_SUBST([TRADEMGEN_CFLAGS])
     AC_SUBST([TRADEMGEN_LIBS])
     AC_SUBST([TRADEMGEN_SAMPLE_DIR])

    trademgen_major_version=`echo ${TRADEMGEN_VERSION} | sed 's/^\([[0-9]]*\).*/\1/'`
    if test "x${trademgen_major_version}" = "x" ; then
       trademgen_major_version=0
    fi

    trademgen_minor_version=`echo ${TRADEMGEN_VERSION} | \
						sed 's/^\([[0-9]]*\)\.\{0,1\}\([[0-9]]*\).*/\2/'`
    if test "x${trademgen_minor_version}" = "x" ; then
       trademgen_minor_version=0
    fi

    trademgen_micro_version=`echo ${TRADEMGEN_VERSION} | \
          sed 's/^\([[0-9]]*\)\.\{0,1\}\([[0-9]]*\)\.\{0,1\}\([[0-9]]*\).*/\3/'`
    if test "x${trademgen_micro_version}" = "x" ; then
       trademgen_micro_version=0
    fi

    ## Simple test of compilation and link
    SAVED_CPPFLAGS="${CPPFLAGS}"
    SAVED_LDFLAGS="${LDFLAGS}"
    CPPFLAGS="${CPPFLAGS} ${BOOST_CFLAGS} ${TRADEMGEN_CFLAGS}"
    LDFLAGS="${LDFLAGS} ${TRADEMGEN_LIBS}"


    AC_COMPILE_IFELSE(
		[AC_LANG_PROGRAM([[#include <trademgen/TRADEMGEN_Service.hpp>
				]],
				[[int i=0;]]
		)]
		,

    	[AC_MSG_RESULT([yes (${TRADEMGEN_VERSION})])],

	[AC_MSG_ERROR([We could not compile a simple TraDemGen example. See config.log.])]
    )

    CPPFLAGS="${SAVED_CPPFLAGS}"
    LDFLAGS="${SAVED_LDFLAGS}"

  fi

AC_LANG_RESTORE
])
