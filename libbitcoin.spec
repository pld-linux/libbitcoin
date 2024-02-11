#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Bitcoin Cross-Platform C++ Development Toolkit 
Summary(pl.UTF-8):	Wieloplatformowy toolkit C++ do programowania związanego z bitcoinami
Name:		libbitcoin
Version:	3.3.0
Release:	1
License:	AGPL with a lesser clause
Group:		Libraries
#Source0Download: https://github.com/libbitcoin/libbitcoin-system/releases
#Source0:	https://github.com/libbitcoin/libbitcoin-system/archive/v%{version}/%{name}-%{version}.tar.gz
Source0:	https://github.com/libbitcoin/libbitcoin/archive/v%{version}.tar.gz
# Source0-md5:	04af8f20cf05a4f2ae4edbb3211f520c
Patch0:		%{name}-boost.patch
URL:		https://libbitcoin.info/
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake
# chrono date_time filesystem iostreams locale log program_options regex system thread unit_test_framework
BuildRequires:	boost-devel >= 1.57.0
BuildRequires:	libpng-devel >= 2:1.6.29
BuildRequires:	libsecp256k1-devel >= 0.0.1
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	qrencode-devel >= 3.4.4
Requires:	libpng >= 2:1.6.29
Requires:	libsecp256k1 >= 0.0.1
Requires:	qrencode-libs >= 3.4.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bitcoin Cross-Platform C++ Development Toolkit 

%description -l pl.UTF-8
Wieloplatformowy toolkit C++ do programowania związanego z bitcoinami.

%package devel
Summary:	Header files for libbitcoin library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbitcoin
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel >= 1.57.0
Requires:	libpng-devel >= 2:1.6.29
Requires:	libsecp256k1-devel >= 0.0.1
Requires:	libstdc++-devel >= 6:4.7
Requires:	qrencode-devel >= 3.4.4

%description devel
Header files for libbitcoin library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libbitcoin.

%package static
Summary:	Static libbitcoin library
Summary(pl.UTF-8):	Statyczna biblioteka libbitcoin
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libbitcoin library.

%description static -l pl.UTF-8
Statyczna biblioteka libbitcoin.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-png \
	--with-qrencode
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbitcoin.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libbitcoin

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# COPYING contains AGPL v3 with additional exception
%doc AUTHORS COPYING README.md
%attr(755,root,root) %{_libdir}/libbitcoin.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbitcoin.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbitcoin.so
%{_includedir}/bitcoin
%{_pkgconfigdir}/libbitcoin.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbitcoin.a
%endif
