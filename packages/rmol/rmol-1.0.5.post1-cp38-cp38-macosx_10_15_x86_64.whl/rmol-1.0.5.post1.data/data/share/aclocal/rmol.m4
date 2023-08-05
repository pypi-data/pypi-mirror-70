#
# Configure paths and flags for the RMOL library.
# Denis Arnaud <denis_arnaud at users dot sourceforge dot net>, July 2008
#
# Note: the RMOL library depends upon BOOST to build.
# Your configure.ac must therefore define appropriately the BOOST
# variables (i.e., BOOST_CFLAGS, BOOST_LIBS, BOOST_DATE_TIME_LIB).
#
# Variables set by this macro:
#  * RMOL_VERSION
#  * RMOL_CFLAGS
#  * RMOL_LIBS
#  * RMOL_SAMPLE_DIR
#

AC_DEFUN([AM_PATH_RMOL],
[
AC_LANG_SAVE
AC_LANG([C++])

##
AC_ARG_WITH(rmol,
	[ --with-rmol=PFX Prefix where RMOL is installed (optional) ],
	    rmol_dir="$withval",
	    rmol_dir="")

  if test "x${RMOL_CONFIG+set}" != xset ; then
     if test "x$rmol_dir" != x ; then
         RMOL_CONFIG="$rmol_dir/bin/rmol-config"
     fi
  fi

  AC_PATH_PROG(RMOL_CONFIG, rmol-config, no)

  ## Check whether Boost flags and libraries are defined
  # General Boost compilation flags
  AC_MSG_CHECKING(for BOOST_CFLAGS environment variable)
  if test x"${BOOST_CFLAGS}" = x; then
	AC_MSG_RESULT([Warning: RMOL needs Boost, and the BOOST_CFLAGS environment variable does not appear to be set. It may not be a problem, though, if your Unix distribution is standard, that is, if Boost is installed in /usr. Otherwise, the RMOL will fail to compile.])
  else
	AC_MSG_RESULT([ok (set to ${BOOST_CFLAGS})])
  fi

  # Boost Date-Time library
  AC_MSG_CHECKING(for BOOST_DATE_TIME_LIB environment variable)
  if test x"${BOOST_DATE_TIME_LIB}" = x; then
	AC_MSG_RESULT([Warning: RMOL needs the Boost Date-Time library, and the BOOST_DATE_TIME_LIB environment variable does not appears to be set. The RMOL may fail to link.])
  else
	AC_MSG_RESULT([ok (set to ${BOOST_DATE_TIME_LIB})])
  fi

  # Boost Program Options library
  AC_MSG_CHECKING(for BOOST_PROGRAM_OPTIONS_LIB environment variable)
  if test x"${BOOST_PROGRAM_OPTIONS_LIB}" = x; then
	AC_MSG_RESULT([Warning: RMOL needs the Boost Program Options library, and the BOOST_PROGRAM_OPTIONS_LIB environment variable does not appears to be set. The RMOL may fail to link.])
  else
	AC_MSG_RESULT([ok (set to ${BOOST_PROGRAM_OPTIONS_LIB})])
  fi

  # Boost File System library
  AC_MSG_CHECKING(for BOOST_FILESYSTEM_LIB environment variable)
  if test x"${BOOST_FILESYSTEM_LIB}" = x; then
	AC_MSG_RESULT([Warning: RMOL needs the Boost Date-Time library, and the BOOST_FILESYSTEM_LIB environment variable does not appears to be set. The RMOL may fail to link.])
  else
	AC_MSG_RESULT([ok (set to ${BOOST_FILESYSTEM_LIB})])
  fi

  ## RMOL version
  min_rmol_version=ifelse([$1], ,0.1.0,$1)
  AC_MSG_CHECKING(for RMOL - version >= $min_rmol_version)
  no_rmol=""
  if test "${RMOL_CONFIG}" = "no" ; then
     no_rmol=yes
     AC_MSG_RESULT([no])
  else
     RMOL_VERSION=`${RMOL_CONFIG} --version`
     RMOL_CFLAGS=`${RMOL_CONFIG} --cflags`
     RMOL_CFLAGS="${BOOST_CFLAGS} ${RMOL_CFLAGS}"
     RMOL_LIBS=`${RMOL_CONFIG} --libs`
     RMOL_LIBS="${BOOST_LIBS} ${BOOST_DATE_TIME_LIB} ${RMOL_LIBS}"
     RMOL_SAMPLE_DIR=`${RMOL_CONFIG} --sampledir`

     AC_SUBST([RMOL_VERSION])
     AC_SUBST([RMOL_CFLAGS])
     AC_SUBST([RMOL_LIBS])
     AC_SUBST([RMOL_SAMPLE_DIR])

    rmol_major_version=`echo ${RMOL_VERSION} | sed 's/^\([[0-9]]*\).*/\1/'`
    if test "x${rmol_major_version}" = "x" ; then
       rmol_major_version=0
    fi

    rmol_minor_version=`echo ${RMOL_VERSION} | \
						sed 's/^\([[0-9]]*\)\.\{0,1\}\([[0-9]]*\).*/\2/'`
    if test "x${rmol_minor_version}" = "x" ; then
       rmol_minor_version=0
    fi

    rmol_micro_version=`echo ${RMOL_VERSION} | \
          sed 's/^\([[0-9]]*\)\.\{0,1\}\([[0-9]]*\)\.\{0,1\}\([[0-9]]*\).*/\3/'`
    if test "x${rmol_micro_version}" = "x" ; then
       rmol_micro_version=0
    fi

    ## Simple test of compilation and link
    SAVED_CPPFLAGS="${CPPFLAGS}"
    SAVED_LDFLAGS="${LDFLAGS}"
    CPPFLAGS="${CPPFLAGS} ${BOOST_CFLAGS} ${RMOL_CFLAGS}"
    LDFLAGS="${LDFLAGS} ${RMOL_LIBS}"


    AC_COMPILE_IFELSE(
		[AC_LANG_PROGRAM([[#include <rmol/RMOL_Service.hpp>
				]],
				[[int i=0;]]
		)]
		,

    	[AC_MSG_RESULT([yes (${RMOL_VERSION})])],

	[AC_MSG_ERROR([We could not compile a simple RMOL example. See config.log.])]
    )

    CPPFLAGS="${SAVED_CPPFLAGS}"
    LDFLAGS="${SAVED_LDFLAGS}"

  fi

AC_LANG_RESTORE
])
