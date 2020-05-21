%define major 0
%define libname %mklibname ogg %{major}
%define devname %mklibname ogg -d
%define lib32name libogg%{major}
%define dev32name libogg-devel

%global optflags %{optflags} -O3

# flac uses libogg, audiofile uses flac, wine uses audiofile
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

# (tpg) enable PGO build
%bcond_without pgo

Summary:	Ogg Bitstream Library
Name:		libogg
Version:	1.3.4
Release:	2
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

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{devname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Main library for %{name} (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{dev32name}
Summary:	Headers for developing programs that will use %{name} (32-bit)
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
This package contains the headers that programmers will need to develop
applications which will use %{name}.
%endif

%prep
%autosetup -p1
autoreconf -fi
sed -i "s/-O20/$CFLAGS/" configure

%build
export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir build32
cd build32
%configure32 --disable-static
cd ..
%endif

mkdir build
cd build
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
cd ..

%if %{with compat32}
%make_build -C build32
%endif

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

rm -rf %{buildroot}%{_docdir}/libogg/

%files -n %{libname}
%{_libdir}/libogg.so.%{major}*

%files -n %{devname}
%doc AUTHORS CHANGES
%doc doc/*.html doc/*.png doc/*.txt
%{_includedir}/ogg/*.h
%{_libdir}/*.so
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libogg.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*
%endif
