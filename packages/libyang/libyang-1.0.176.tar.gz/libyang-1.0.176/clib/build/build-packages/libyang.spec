Name: libyang
Version: 1.0.176
Release: 0
Summary: Libyang library
Url: https://github.com/CESNET/libyang
Source: %{url}/archive/master.tar.gz
Source1: libyang.rpmlintrc
License: BSD-3-Clause
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}

%if 0%{?scientificlinux_version} == 700 || ( 0%{?rhel} && 0%{?rhel} < 7 )
    %define with_lang_bind 0
%else
    %define with_lang_bind 1
%endif

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
    %define with_ly_cache 0
%else
    %define with_ly_cache 1
%endif

Requires:  pcre
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  pcre-devel
BuildRequires:  gcc
BuildRequires:  libcmocka-devel

%if %{with_lang_bind}

BuildRequires:  gcc-c++
%if 0%{?rhel} == 7
BuildRequires:  swig3 >= 3.0.12
%else
BuildRequires:  swig >= 3.0.12
%endif

%if 0%{?suse_version} + 0%{?fedora} + 0%{?centos_version} > 0
BuildRequires:  python3-devel
BuildRequires:  python3-cffi
BuildRequires:  python3-setuptools
%else
BuildRequires:  python36-devel
BuildRequires:  python36-cffi
BuildRequires:  python36-setuptools
%endif

%endif

%package devel
Summary:    Headers of libyang library
Requires:   %{name} = %{version}-%{release}
Requires:   pcre-devel

%if %{with_lang_bind}
%package -n libyang-cpp
Summary:    Bindings to c++ language
Requires:   %{name} = %{version}-%{release}

%package -n libyang-cpp-devel
Summary:    Headers of bindings to c++ language
Requires:   libyang-cpp = %{version}-%{release}
Requires:   pcre-devel

%package -n python3-yang
Summary:    SWIG binding to python
Requires:   libyang-cpp = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

%package -n python3-libyang
Summary:    CFFI binding to python
Requires:   %{name} = %{version}-%{release}
%if 0%{?suse_version} + 0%{?fedora} + 0%{?centos_version} > 0
Requires:   python3
Requires:   python3-cffi
%else
Requires:   python36
Requires:   python36-cffi
%endif

%description -n libyang-cpp
Bindings of libyang library to C++ language.

%description -n libyang-cpp-devel
Headers of bindings to c++ language.

%description -n python3-yang
SWIG bindings of libyang library to python language.

%description -n python3-libyang
CFFI bindings of libyang library to python language.
%endif

%description devel
Headers of libyang library.

%description
libyang is YANG data modelling language parser and toolkit written (and providing API) in C.

%prep
%setup -n libyang-master
mkdir build

%build
cd build
%if %{with_lang_bind}
    %define cmake_lang_bind "-DGEN_LANGUAGE_BINDINGS=ON -DGEN_PYTHON_CFFI_BINDINGS=ON"
%else
    %define cmake_lang_bind "-DGEN_LANGUAGE_BINDINGS=OFF"
%endif
%if %{with_ly_cache}
    %define cmake_ly_cache "-DENABLE_CACHE=ON"
%else
    %define cmake_ly_cache "-DENABLE_CACHE=OFF"
%endif

cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr \
   -DCMAKE_BUILD_TYPE:String="Package" \
   -DENABLE_LYD_PRIV=ON \
   -DGEN_JAVA_BINDINGS=OFF \
   -DGEN_JAVASCRIPT_BINDINGS=OFF \
   %{cmake_lang_bind} \
   %{cmake_ly_cache} ..
make

%check
cd build
ctest --output-on-failure

%install
cd build
make DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%if %{with_lang_bind}
%post -n libyang-cpp -p /sbin/ldconfig
%endif

%postun -p /sbin/ldconfig
%if %{with_lang_bind}
%postun -n libyang-cpp -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%{_bindir}/yanglint
%{_bindir}/yangre
%{_datadir}/man/man1/yanglint.1.gz
%{_datadir}/man/man1/yangre.1.gz
%{_libdir}/libyang.so.*
%{_libdir}/libyang1/*
%dir %{_libdir}/libyang1/

%files devel
%defattr(-,root,root)
%{_libdir}/libyang.so
%{_libdir}/pkgconfig/libyang.pc
%{_includedir}/libyang/*.h
%dir %{_includedir}/libyang/

%if %{with_lang_bind}
%files -n libyang-cpp
%defattr(-,root,root)
%{_libdir}/libyang-cpp.so.*

%files -n libyang-cpp-devel
%defattr(-,root,root)
%{_libdir}/libyang-cpp.so
%{_includedir}/libyang/*.hpp
%{_libdir}/pkgconfig/libyang-cpp.pc
%dir %{_includedir}/libyang/

%files -n python3-yang
%defattr(-,root,root)
%{_libdir}/python*/site-packages/yang*

%files -n python3-libyang
%defattr(-,root,root)
%{_libdir}/python3*/site-packages/libyang*
%{_libdir}/python3*/site-packages/_libyang*.so
%endif

%changelog
