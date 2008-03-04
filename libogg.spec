%define name libogg
%define version 1.1.3
%define lib_name %mklibname ogg 0

Name: %{name}
Summary: Ogg Bitstream Library
Version: %{version}
Release: %mkrel 3
Group: System/Libraries
License: BSD
URL: http://www.xiph.org/
Source:	http://downloads.xiph.org/releases/ogg/%{name}-%{version}.tar.bz2
Patch0: libogg-fix-optflags.patch
Patch1: libogg-1.0-lib64.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: autoconf2.5

%description
Libogg is a library for manipulating ogg bitstreams. It handles
both making ogg bitstreams and getting packets from ogg bitstreams.

%package -n %{lib_name}
Summary: Main library for %{name}
Group: System/Libraries
Provides: %{name} = %{version}-%{release}

%description -n %{lib_name}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{lib_name}-devel
Summary: Headers for developing programs that will use %{name}
Group: Development/C
Requires: %{lib_name} = %{version}-%{release}
Provides: libogg-devel = %{version}-%{release}

%description -n %{lib_name}-devel
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -p1 -b .lib64

%build
autoconf
%if %mdkversion <= 1000
%define __libtoolize true
%endif
%configure2_5x
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean 
rm -rf $RPM_BUILD_ROOT

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files -n %{lib_name}
%defattr(-,root,root)
%doc AUTHORS CHANGES COPYING README
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc doc/*.html doc/*.png
%dir %_docdir/libogg-%version/
%doc %_docdir/libogg-%version/*.html
%doc %_docdir/libogg-%version/*.png
%doc %_docdir/libogg-%version/*.txt
%dir %_docdir/libogg-%version/ogg/
%doc %_docdir/libogg-%version/ogg/*.html
%doc %_docdir/libogg-%version/ogg/*.css
%{_includedir}/ogg
%{_libdir}/*.*a
%{_libdir}/*.so
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*


