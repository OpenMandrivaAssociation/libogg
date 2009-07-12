%define major 0
%define libname %mklibname ogg %{major}
%define develname %mklibname ogg -d

Summary:	Ogg Bitstream Library
Name:		libogg
Version:	1.1.4
Release:	%mkrel 2
Group:		System/Libraries
License:	BSD
URL:		http://www.xiph.org/
Source:		http://downloads.xiph.org/releases/ogg/%{name}-%{version}.tar.bz2
Patch1:		libogg-1.0-lib64.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package -n %{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	libogg-devel = %{version}-%{release}
Obsoletes:	%{mklibname ogg 0 -d}

%description -n %{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q

%build
sed -i "s/-O20/$CFLAGS/" configure
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

rm -rf %{buildroot}%{_docdir}/libogg-%{version}/

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS CHANGES README
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc doc/*.html doc/*.png doc/*.txt
%{_includedir}/ogg
%{_libdir}/*.*a
%{_libdir}/*.so
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
