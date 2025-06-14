#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	tests		# unit tests
#
Summary:	An implementation of the TLS/SSL protocols
Summary(pl.UTF-8):	Implementacja protokołów TLS/SSL
Name:		s2n-tls
Version:	1.5.21
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/aws/s2n-tls/releases
Source0:	https://github.com/aws/s2n-tls/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	af27cdcb1746f851ee7fe0929ee5650e
URL:		https://github.com/aws/s2n-tls
BuildRequires:	cmake >= 3.9
BuildRequires:	openssl-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
s2n-tls is a C99 implementation of the TLS/SSL protocols that is
designed to be simple, small, fast, and with security as a priority.
It is released and licensed under the Apache License 2.0.

"s2n" is short for "signal to noise" and is a nod to the almost
magical act of encryption - disguising meaningful signals, like your
critical data, as seemingly random noise.

%description -l pl.UTF-8
s2n-tls to implementacja w C99 protokołów TLS/SSL, zaprojektowana jako
prosta, mała, szybka i z myślą głównie o bezpieczeństwie. Jest wydana
na licencji Apache w wersji 2.0.

"s2n" to skrót od "signal to noise" (sygnał do szumu), co jest
nawiązaniem do prawie magicznego aktu szyfrowania - przemiany
znaczącego sygnału, zawierającego krytyczne dane, do szumu
wyglądającego na losowy.

%package devel
Summary:	Header files for AWS S2N library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki AWS S2N
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for AWS S2N library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki AWS S2N.

%package apidocs
Summary:	API documentation for AWS S2N library
Summary(pl.UTF-8):	Dokumentacja API biblioteki AWS S2N
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for AWS S2N library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki AWS S2N.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	%{!?with_tests:-DBUILD_TESTING=OFF}

%{__make}

%if %{with tests}
%{__make} test
%endif

cd ..

%if %{with apidocs}
doxygen docs/doxygen/Doxyfile
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NOTICE README.md
%attr(755,root,root) %{_libdir}/libs2n.so.*.*.*
%ghost %{_libdir}/libs2n.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/libs2n.so
%{_includedir}/s2n
%{_includedir}/s2n.h
%dir %{_libdir}/s2n
%{_libdir}/s2n/cmake

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/doxygen/output/html/*
%endif
