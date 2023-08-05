# Get XAPIAN_CXXFLAGS, XAPIAN_LIBS, and XAPIAN_VERSION from xapian-config and
# AC_SUBST() them.

# serial 7

# AC_PROVIDE_IFELSE(MACRO-NAME, IF-PROVIDED, IF-NOT-PROVIDED)
# -----------------------------------------------------------
# If this macro is not defined by Autoconf, define it here.
m4_ifdef([AC_PROVIDE_IFELSE],
	 [],
	 [m4_define([AC_PROVIDE_IFELSE],
		 [m4_ifdef([AC_PROVIDE_$1],
			   [$2], [$3])])])

# XO_LIB_XAPIAN([ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND]])
# --------------------------------------------------------
# AC_SUBST-s XAPIAN_CXXFLAGS, XAPIAN_LIBS, and XAPIAN_VERSION for use in
# Makefile.am
#
# If ACTION-IF-FOUND and ACTION-IF-NOT-FOUND are both unset, then an
# appropriate AC_MSG_ERROR is used as a default ACTION-IF-NOT-FOUND.
# This allows XO_LIB_XAPIAN to be used without any arguments in the
# common case where Xapian is a requirement (rather than optional).
AC_DEFUN([XO_LIB_XAPIAN],
[
  AC_ARG_VAR(XAPIAN_CONFIG, [Location of xapian-config])
  AC_PATH_PROG(XAPIAN_CONFIG, xapian-config, [])
  if test -z "$XAPIAN_CONFIG"; then
    ifelse([$2], ,
      [ifelse([$1], , [
	dnl Simple check to see if the problem is likely to
	dnl be that we're using a "packaged" xapian-core but
	dnl only have the runtime package installed.
	for sfx in '' 32 64 ; do
	  set /usr/lib$sfx/libxapian.so.*
	  if test "/usr/lib$sfx/libxapian.so.*" != "$1" ; then
	    if test -r /etc/debian_version ; then
	      pkg="libxapian-dev"
	    else
	      pkg="xapian-core-devel"
	    fi
	    AC_MSG_ERROR([Can't find xapian-config, although the xapian-core runtime library seems to be installed.  If you've installed xapian-core from a package, you probably need to install an extra package called something like $pkg in order to be able to build code using the Xapian library.])
	  fi
	done
	AC_MSG_ERROR([Can't find Xapian library])],
	:)],
      [$2])
  else
    AC_MSG_CHECKING([$XAPIAN_CONFIG works])
    dnl check for --ltlibs but not --libs as "xapian-config --libs" will
    dnl fail if xapian isn't installed...

    dnl run with exec to avoid leaking output on "real" bourne shells
    if (exec >&5 2>&5 ; $XAPIAN_CONFIG --ltlibs --cxxflags; exit $?) then
      AC_MSG_RESULT(yes)
    else
      AC_MSG_ERROR([\`$XAPIAN_CONFIG --ltlibs --cxxflags' doesn't work, aborting])
    fi

dnl If LT_INIT, AC_PROG_LIBTOOL or the deprecated older version
dnl AM_PROG_LIBTOOL has already been expanded, enable libtool support now.
dnl Otherwise add hooks to the end of LT_INIT, AC_PROG_LIBTOOL and
dnl AM_PROG_LIBTOOL to enable it if one of these is expanded later.
    XAPIAN_VERSION=`$XAPIAN_CONFIG --version|sed 's/.* //;s/_svn[[0-9]]*$//'`
    XAPIAN_CFLAGS=`$XAPIAN_CONFIG --cxxflags`
    AC_PROVIDE_IFELSE([LT_INIT],
      [XAPIAN_LIBS=`$XAPIAN_CONFIG --ltlibs`],
      [AC_PROVIDE_IFELSE([AC_PROG_LIBTOOL],
	[XAPIAN_LIBS=`$XAPIAN_CONFIG --ltlibs`],
	[AC_PROVIDE_IFELSE([AM_PROG_LIBTOOL],
	  [XAPIAN_LIBS=`$XAPIAN_CONFIG --ltlibs`],
	  dnl Pass magic option so xapian-config knows we called it (so it
	  dnl can choose a more appropriate error message if asked to link
	  dnl with an uninstalled libxapian).  Also pass ac_top_srcdir
	  dnl so the error message can correctly say "configure.ac" or
	  dnl "configure.in" according to which is in use.
	  [XAPIAN_LIBS=`ac_top_srcdir="$ac_top_srcdir" $XAPIAN_CONFIG --from-xo-lib-xapian --libs`
	  define([LT_INIT], defn([LT_INIT])
		 [XAPIAN_LIBS=`$XAPIAN_CONFIG --ltlibs`])
	  define([AC_PROG_LIBTOOL], defn([AC_PROG_LIBTOOL])
		 [XAPIAN_LIBS=`$XAPIAN_CONFIG --ltlibs`])
	  define([AM_PROG_LIBTOOL], defn([AM_PROG_LIBTOOL])
		 [XAPIAN_LIBS=`$XAPIAN_CONFIG --ltlibs`])])])])
    ifelse([$1], , :, [$1])
  fi
  AC_SUBST(XAPIAN_CFLAGS)
  AC_SUBST(XAPIAN_LIBS)
  AC_SUBST(XAPIAN_VERSION)
])
