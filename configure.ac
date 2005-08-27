# Process this file with autoconf to produce a configure script.
AC_PREREQ(2.57)
AC_INIT([libextractor-python], [0.5.4], [bug-libextractor@gnu.org])
AC_REVISION($Revision: 1.67 $)
AM_INIT_AUTOMAKE([libextractor-python], [0.5.4])

AC_PROG_AWK
AC_PROG_CC

AC_PYTHON_DEVEL
AC_MSG_CHECKING(for python)
if test -z "$python_path";
then
  AC_MSG_RESULT(yes)
  AM_CONDITIONAL(HAVE_PYTHON,false)
else
  AC_MSG_RESULT(no)
  AM_CONDITIONAL(HAVE_PYTHON,true)
fi

# test for libextractor
extractor=0
AC_MSG_CHECKING([for libextractor])
AC_ARG_WITH(extractor,
   [  --with-extractor=PFX    Base of libextractor installation],
   [AC_MSG_RESULT([$with_extractor])
    case $with_extractor in
      no)
        ;;
      yes)
        AC_CHECK_HEADERS(extractor.h,
          AC_CHECK_LIB([extractor], [EXTRACTOR_loadDefaultLibraries],
            extractor=1))
        ;;
      *)
        LDFLAGS="-L$with_extractor/lib $LDFLAGS"
        CPPFLAGS="-I$with_extractor/include $CPPFLAGS"
        AC_CHECK_HEADERS(extractor.h,
          AC_CHECK_LIB([extractor], [EXTRACTOR_loadDefaultLibraries],
            EXT_LIB_PATH="$with_extractor"
            extractor=1))
        ;;
    esac
   ],
   [AC_MSG_RESULT([--with-extractor not specified])
    AC_CHECK_HEADERS(extractor.h,
     AC_CHECK_LIB([extractor], [EXTRACTOR_loadDefaultLibraries],
      extractor=1))])
if test "$extractor" != 1
then
 AC_MSG_ERROR([libextractor-python requires libextractor])
fi

AC_SUBST(EXT_LIB_PATH)

AC_CONFIG_FILES([Makefile])
AC_OUTPUT
