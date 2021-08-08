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
Version:	1.3.5
Release:	1
Group:		System/Libraries
License:	BSD
Url:		http://www.xiph.org/
Source0:	http://downloads.xiph.org/releases/ogg/%{name}-%{version}.tar.xz
BuildRequires:	cmake
BuildRequires:	ninja

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

%build
export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
%cmake32 -DBUILD_SHARED_LIBS=ON -G Ninja
cd ..
%ninja_build -C build32
%endif

%if %{with pgo}
%define _vpath_builddir pgo
mkdir pgo
export LLVM_PROFILE_FILE=%{name}-%p.profile.d
export LD_LIBRARY_PATH="$(pwd)"
CFLAGS="%{optflags} -fprofile-instr-generate" \
CXXFLAGS="%{optflags} -fprofile-instr-generate" \
FFLAGS="$CFLAGS" \
FCFLAGS="$CFLAGS" \
LDFLAGS="%{ldflags} -fprofile-instr-generate" \
%cmake -DBUILD_SHARED_LIBS=ON -G Ninja
%ninja_build
%ninja_test ||:

unset LD_LIBRARY_PATH
unset LLVM_PROFILE_FILE
llvm-profdata merge --output=%{name}.profile *.profile.d
ninja clean
rm -rf pgo

%undefine _vpath_builddir

CFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
CXXFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
LDFLAGS="%{ldflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
%endif
%cmake -DBUILD_SHARED_LIBS=ON -G Ninja
cd ..
%ninja_build
cd ..

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%ninja_install -C build

rm -rf %{buildroot}%{_docdir}/libogg/

%files -n %{libname}
%{_libdir}/libogg.so.%{major}*

%files -n %{devname}
%doc AUTHORS CHANGES
%doc doc/*.html doc/*.png doc/*.txt
%{_includedir}/ogg/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%dir %{_libdir}/cmake/Ogg
%{_libdir}/cmake/Ogg/*.cmake

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libogg.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*
%dir %{_prefix}/lib/cmake/Ogg
%{_prefix}/lib/cmake/Ogg/*.cmake
%endif
