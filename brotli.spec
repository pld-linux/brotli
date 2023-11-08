#
# Conditional build:
%bcond_without	python2		# Python 2 module
%bcond_without	python3		# Python 3 module
%bcond_without	static_libs	# static libraries
#
Summary:	Brotli - generic-purpose lossless compression algorithm
Summary(pl.UTF-8):	Brotli - algorytm bezstratnej kompresji ogólnego przeznaczenia
Name:		brotli
Version:	1.1.0
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/google/brotli/releases
Source0:	https://github.com/google/brotli/archive/v%{version}/Brotli-%{version}.tar.gz
# Source0-md5:	3a6a3dba82a3604792d3cb0bd41bca60
Patch0:		%{name}-py2.patch
URL:		https://github.com/google/brotli/
BuildRequires:	bc
BuildRequires:	cmake >= 3.16
BuildRequires:	libstdc++-devel >= 6:4.7
%{?with_python2:BuildRequires:	python-devel >= 1:2.7}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.3}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	libbrotli = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Brotli is a generic-purpose lossless compression algorithm that
compresses data using a combination of a modern variant of the LZ77
algorithm, Huffman coding and 2nd order context modeling, with a
compression ratio comparable to the best currently available
general-purpose compression methods. It is similar in speed with
deflate but offers more dense compression.

The specification of the Brotli Compressed Data Format is defined in
the following Internet draft:
<http://www.ietf.org/id/draft-alakuijala-brotli>.

%description -l pl.UTF-8
Brotli to algorytm kompresji bezstratnej ogólnego przeznaczenia,
kompresujący dane przy użyciu kombinacji współczesnego wariantu
algorytmu LZ77, kodowania Huffmana oraz modelowania kontekstu 2.
rzędu, ze współczynnikami kompresji porównywalnymi do najlepszych
obecnie dostępnych metod kompresji ogólnego przeznaczenia. Szybkość
jest podobna do deflatingu, ale kompresja jest bardziej zwarta.

Specyfikacja formatu danych kompresji Brotli jest zdefiniowana w
następującym szkicu internetowym:
<http://www.ietf.org/id/draft-alakuijala-brotli>.

%package -n libbrotli
Summary:	Brotli compression encoding/decoding libraries
Summary(pl.UTF-8):	Biblioteki do kodowania/dekodowania kompresji Brotli
Group:		Libraries

%description -n libbrotli
Brotli compression encoding/decoding libraries.

%description -n libbrotli -l pl.UTF-8
Biblioteki do kodowania/dekodowania kompresji Brotli.

%package -n libbrotli-devel
Summary:	Header files for Brotli libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Brotli
Group:		Development/Libraries
Requires:	libbrotli = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7

%description -n libbrotli-devel
Header files for Brotli libraries.

%description -n libbrotli-devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Brotli.

%package -n libbrotli-static
Summary:	Static Brotli libraries
Summary(pl.UTF-8):	Statyczne biblioteki Brotli
Group:		Development/Libraries
Requires:	libbrotli-devel = %{version}-%{release}

%description -n libbrotli-static
Static Brotli libraries.

%description -n libbrotli-static -l pl.UTF-8
Statyczne biblioteki Brotli.

%package -n python-brotli
Summary:	Python 2 module for Brotli compression decoding/encoding
Summary(pl.UTF-8):	Moduł Pythona 2 do kodowania/dekodowania kompresji Brotli
Group:		Libraries/Python

%description -n python-brotli
Python 2 module for Brotli compression decoding/encoding.

%description -n python-brotli -l pl.UTF-8
Moduł Pythona 2 do kodowania/dekodowania kompresji Brotli.

%package -n python3-brotli
Summary:	Python 3 module for Brotli compression decoding/encoding
Summary(pl.UTF-8):	Moduł Pythona 3 do kodowania/dekodowania kompresji Brotli
Group:		Libraries/Python

%description -n python3-brotli
Python 3 module for Brotli compression decoding/encoding.

%description -n python3-brotli -l pl.UTF-8
Moduł Pythona 3 do kodowania/dekodowania kompresji Brotli.

%prep
%setup -q
%patch0 -p1

%build
%cmake -B build

%{__make} -C build

%if %{with static_libs}
%cmake -B build-static \
	-DBUILD_SHARED_LIBS=OFF

%{__make} -C build-static
%endif

%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libbrotli -p /sbin/ldconfig
%postun	-n libbrotli -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README README.md
%attr(755,root,root) %{_bindir}/brotli

%files -n libbrotli
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbrotlicommon.so.*.*
%ghost %{_libdir}/libbrotlicommon.so.1
%attr(755,root,root) %{_libdir}/libbrotlidec.so.*.*
%ghost %{_libdir}/libbrotlidec.so.1
%attr(755,root,root) %{_libdir}/libbrotlienc.so.*.*
%ghost %{_libdir}/libbrotlienc.so.1

%files -n libbrotli-devel
%defattr(644,root,root,755)
%{_libdir}/libbrotlicommon.so
%{_libdir}/libbrotlidec.so
%{_libdir}/libbrotlienc.so
%{_includedir}/brotli
%{_pkgconfigdir}/libbrotlicommon.pc
%{_pkgconfigdir}/libbrotlidec.pc
%{_pkgconfigdir}/libbrotlienc.pc

%files -n libbrotli-static
%defattr(644,root,root,755)
%{_libdir}/libbrotlicommon.a
%{_libdir}/libbrotlidec.a
%{_libdir}/libbrotlienc.a

%if %{with python2}
%files -n python-brotli
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_brotli.so
%{py_sitedir}/brotli.py[co]
%{py_sitedir}/Brotli-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-brotli
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_brotli.cpython-*.so
%{py3_sitedir}/brotli.py
%{py3_sitedir}/__pycache__/brotli.cpython-*.py[co]
%{py3_sitedir}/Brotli-%{version}-py*.egg-info
%endif
