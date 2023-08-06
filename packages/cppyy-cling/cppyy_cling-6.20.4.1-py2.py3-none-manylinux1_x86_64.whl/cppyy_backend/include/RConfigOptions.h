#ifndef ROOT_RConfigOptions
#define ROOT_RConfigOptions

#define R__CONFIGUREOPTIONS   "PCRE_INCLUDE_DIR=/root/cppyy-backend/cling/builddir/builtins/pcre/PCRE-prefix/src/PCRE-build PCRE_LIBRARIES=/root/cppyy-backend/cling/builddir/builtins/pcre/PCRE-prefix/src/PCRE-build/./libpcre.a PCRE_PCRE_LIBRARY=/root/cppyy-backend/cling/builddir/builtins/pcre/PCRE-prefix/src/PCRE-build/./libpcre.a PCRE_VERSION=8.43 ZLIB_INCLUDE_DIR=/root/cppyy-backend/cling/src/builtins/zlib ZLIB_INCLUDE_DIRS=/root/cppyy-backend/cling/src/builtins/zlib ZLIB_LIBRARIES=ZLIB::ZLIB ZLIB_LIBRARY=$<TARGET_FILE:ZLIB> ZLIB_VERSION=1.2.8 ZLIB_VERSION_STRING=1.2.8 xxHash_INCLUDE_DIR=/root/cppyy-backend/cling/src/builtins/xxhash xxHash_INCLUDE_DIRS=/root/cppyy-backend/cling/src/builtins/xxhash xxHash_LIBRARIES=xxHash::xxHash xxHash_LIBRARY=$<TARGET_FILE:xxhash> xxHash_VERSION=0.6.4 xxHash_VERSION_STRING=0.6.4 "
#define R__CONFIGUREFEATURES  "cxx11  builtin_clang builtin_llvm builtin_pcre builtin_xxhash builtin_zlib shared"

#endif
