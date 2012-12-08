%define major 0
%define libname %mklibname ogg %{major}
%define develname %mklibname ogg -d

Summary:	Ogg Bitstream Library
Name:		libogg
Version:	1.3.0
Release:	3
Group:		System/Libraries
License:	BSD
URL:		http://www.xiph.org/
Source:		http://downloads.xiph.org/releases/ogg/%{name}-%{version}.tar.xz
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

%package -n %{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	libogg-devel = %{version}-%{release}

%description -n %{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q

%build
sed -i "s/-O20/$CFLAGS/" configure
%configure2_5x \
	--disable-static

%make

%install
rm -rf %{buildroot}
%makeinstall_std

rm -rf %{buildroot}%{_docdir}/libogg-%{version}/

%multiarch_includes %{buildroot}%{_includedir}/ogg/config_types.h

%files -n %{libname}
%doc AUTHORS CHANGES README
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc doc/*.html doc/*.png doc/*.txt
%dir %{multiarch_includedir}/ogg
%{multiarch_includedir}/ogg/config_types.h
%{_includedir}/ogg/*.h
%{_libdir}/*.so
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*


%changelog
* Sat Mar 31 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.0-2mdv2012.0
+ Revision: 788524
- do not build static libraries
- fix multiarch issues (mdvbz #65455)

* Thu Aug 25 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.0-1
+ Revision: 697121
- update to new version 1.3.0

  + Matthew Dawkins <mattydaw@mandriva.org>
    - split out static pkg

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-2
+ Revision: 661510
- mass rebuild

* Sun Jan 30 2011 Funda Wang <fwang@mandriva.org> 1.2.2-1
+ Revision: 634087
- update to new version 1.2.2

* Sun Nov 28 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-2mdv2011.0
+ Revision: 602590
- rebuild

* Sat Mar 27 2010 Funda Wang <fwang@mandriva.org> 1.2.0-1mdv2010.1
+ Revision: 528055
- new version 1.2.0

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.4-3mdv2010.1
+ Revision: 520892
- rebuilt for 2010.1

* Sun Jul 12 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.4-2mdv2010.0
+ Revision: 395098
- fix obsoletes

* Sun Jul 12 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.4-1mdv2010.0
+ Revision: 394924
- use sed instead of patch 0
- disable patch1
- protect major
- spec file clean
- follow mdv's devel policy
- update to new version 1.1.4

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.1.3-4mdv2009.0
+ Revision: 222943
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.3-3mdv2008.1
+ Revision: 178987
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot


* Sun Jan 14 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1.1.3-1mdv2007.0
+ Revision: 108699
- Import libogg

* Sun Jan 14 2007 Götz Waschk <waschk@mandriva.org> 1.1.3-1mdv2007.1
- unpack patches

* Wed Nov 30 2005 GÃ¶tz Waschk <waschk@mandriva.org> 1.1.3-1mdk
- New release 1.1.3

* Tue Nov 09 2004 Götz Waschk <waschk@linux-mandrake.com> 1.1.2-1mdk
- New release 1.1.2
- fix 10.0 build
- fix source URL

