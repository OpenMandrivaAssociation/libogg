%define major	0
%define libname	%mklibname ogg %{major}
%define devname	%mklibname ogg -d

Summary:	Ogg Bitstream Library
Name:		libogg
Version:	1.3.1
Release:	3
Group:		System/Libraries
License:	BSD
Url:		http://www.xiph.org/
Source0:	http://downloads.xiph.org/releases/ogg/%{name}-%{version}.tar.xz
Patch1:		libogg-1.0-lib64.patch

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
%setup -q
#fix build with new automake
sed -i -e 's,AM_CONFIG_HEADER,AC_CONFIG_HEADERS,g' configure.*
autoreconf -fi
sed -i "s/-O20/$CFLAGS/" configure

%build
%configure2_5x \
	--disable-static

%make

%install
%makeinstall_std

rm -rf %{buildroot}%{_docdir}/libogg/

%multiarch_includes %{buildroot}%{_includedir}/ogg/config_types.h

%files -n %{libname}
%{_libdir}/libogg.so.%{major}*

%files -n %{devname}
%doc AUTHORS CHANGES README
%doc doc/*.html doc/*.png doc/*.txt
%dir %{multiarch_includedir}/ogg
%{multiarch_includedir}/ogg/config_types.h
%{_includedir}/ogg/*.h
%{_libdir}/*.so
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*

