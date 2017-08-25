#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Bitcoin Cross-Platform C++ Development Toolkit 
# Summary(pl.UTF-8):	-
Name:		libbitcoin
Version:	3.3.0
Release:	0.1
License:	AGPL with a lesser clause
Group:		Libraries
Source0:	https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz
# Source0-md5:	04af8f20cf05a4f2ae4edbb3211f520c
#Patch0:	%{name}-what.patch
URL:		https://libbitcoin.org/
BuildRequires:	libsecp256k1-devel
BuildRequires:	boost-devel
#BuildRequires:	autoconf
#BuildRequires:	automake
#BuildRequires:	intltool
#BuildRequires:	libtool
#Requires(postun):	-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires:	-
#Provides:	-
#Obsoletes:	-
#Conflicts:	-
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# do not keep them in newly created specs
# these are only here to help fixing quickly broken specs
# %%define		filterout_ld	-Wl,--no-copy-dt-needed-entries
# %%define		filterout_ld	-Wl,--as-needed
# do not commit spec containing this (use for local testing only):
# %%define		filterout_c	-Werror=format-security
# %%define		filterout_cxx	-Werror=format-security

# Ignore file in __spec_install_post_check_so
BuildRequires:	rpmbuild(macros) >= 1.583
%define		skip_post_check_so	libunresolved.so.*

# do not commit spec containing this (use for local testing only):
%define		no_install_post_check_tmpfiles	1

%description
Bitcoin Cross-Platform C++ Development Toolkit 

#%description -l pl.UTF-8

%package common
Summary:	Common files for %{name} library
Summary(pl.UTF-8):	Wspólne pliki biblioteki %{name}
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description common
Common files for %{name} library.

%description common -l pl.UTF-8
Wspólne pliki biblioteki %{name}.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%package apidocs
Summary:	%{name} API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki %{name}
Group:		Documentation

%description apidocs
API documentation for %{name} library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki %{name}.

%prep
%setup -q
#%patch0 -p1

%build
./autogen.sh
# if ac/am/lt/* rebuilding is necessary, do it in this order and add
# appropriate BuildRequires
#%{__libtoolize}
#%{__aclocal}
#%{__autoconf}
#%{__autoheader}
#%{__automake}
%configure \
	%{!?with_static_libs:--disable-static} \
	--with-png \
	--with-qrencode
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# if library provides pkgconfig file containing proper {Requires,Libs}.private
# then remove .la pollution
#%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS README THANKS
%attr(755,root,root) %{_libdir}/%{name}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}.so.N

%files common
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}*
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%doc devel-doc/* ChangeLog NEWS TODO
%attr(755,root,root) %{_libdir}/%{name}.so
# if no pkgconfig support, or it misses .private deps, then include .la file
#%{_libdir}/libFOO.la
%{_includedir}/%{name}
%{_aclocaldir}/%{name}.m4
%{_pkgconfigdir}/%{name}.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/%{name}.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc apidocs/*
%endif
