%define major 0
%define libname %mklibname ogg %{major}
%define devname %mklibname ogg -d

%global optflags %{optflags} -O3

# (tpg) enable PGO build
%bcond_without pgo

Summary:	Ogg Bitstream Library
Name:		libogg
Version:	1.3.3
Release:	5
Group:		System/Libraries
License:	BSD
Url:		http://www.xiph.org/
Source0:	http://downloads.xiph.org/releases/ogg/%{name}-%{version}.tar.xz

%description
Libogg is a library for manipulating ogg bitstreams. It handles
both making ogg bitstreams and getting packets from ogg bitstreams.

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{devname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%autosetup -p1

#fix build with new automake
sed -i -e 's,AM_CONFIG_HEADER,AC_CONFIG_HEADERS,g' configure.*
autoreconf -fi
sed -i "s/-O20/$CFLAGS/" configure

%build
%if %{with pgo}
export LLVM_PROFILE_FILE=%{name}-%p.profile.d
export LD_LIBRARY_PATH="$(pwd)"
CFLAGS="%{optflags} -fprofile-instr-generate" \
CXXFLAGS="%{optflags} -fprofile-instr-generate" \
FFLAGS="$CFLAGS_PGO" \
FCFLAGS="$CFLAGS_PGO" \
LDFLAGS="%{ldflags} -fprofile-instr-generate" \
%configure --disable-static
%make_build
make check

unset LD_LIBRARY_PATH
unset LLVM_PROFILE_FILE
llvm-profdata merge --output=%{name}.profile *.profile.d

make clean

CFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
CXXFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
LDFLAGS="%{ldflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
%endif
%configure --disable-static
%make_build

%install
%make_install

# we don't want these
find %{buildroot} -name '*.la' -delete

rm -rf %{buildroot}%{_docdir}/libogg/

%if %{mdvver} <= 3000000
%multiarch_includes %{buildroot}%{_includedir}/ogg/config_types.h
%endif

%files -n %{libname}
%{_libdir}/libogg.so.%{major}*

%files -n %{devname}
%doc AUTHORS CHANGES
%doc doc/*.html doc/*.png doc/*.txt
%if %{mdvver} <= 3000000
%dir %{multiarch_includedir}/ogg
%{multiarch_includedir}/ogg/config_types.h
%endif
%{_includedir}/ogg/*.h
%{_libdir}/*.so
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
