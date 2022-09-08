# remirepo/fedora spec file for libmongocrypt
#
# Copyright (c) 2020-2022 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_owner     mongodb
%global gh_project   libmongocrypt
%global libname      %{gh_project}
%global libver       1.0
%global soname       0

Name:      %{libname}
Summary:   The companion C library for client side encryption in drivers
Version:   1.6.0
Release:   1%{?dist}

# see kms-message/THIRD_PARTY_NOTICES
# kms-message/src/kms_b64.c is ISC
# everything else is ASL 2.0
License:   ASL 2.0 and ISC
URL:       https://github.com/%{gh_owner}/%{gh_project}

Source0:   https://github.com/%{gh_owner}/%{gh_project}/archive/%{version}.tar.gz

# drop all reference to static libraries
Patch0:    %{libname}-static.patch

BuildRequires: cmake >= 3.5
BuildRequires: gcc
BuildRequires: gcc-c++
# pkg-config may pull compat-openssl10
BuildRequires: openssl-devel
BuildRequires: cmake(bson-1.0) >= 1.11
# for documentation
BuildRequires: doxygen
BuildRequires: make


%description
%{summary}.


%package devel
Summary:    Header files and development libraries for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   pkgconfig
Requires:   cmake-filesystem

%description devel
This package contains the header files and development libraries
for %{name}.


%prep
%autosetup -n %{gh_project}-%{version}%{?prever:-dev} -p1
echo "%{version}" >VERSION_CURRENT


%build
%cmake \
    -DENABLE_PIC:BOOL=ON \
    -DUSE_SHARED_LIBBSON:BOOL=ON \
    -DMONGOCRYPT_MONGOC_DIR:STRING=USE-SYSTEM \
    -DENABLE_ONLINE_TESTS:BOOL=OFF \
    -DENABLE_STATIC:BOOL=OFF

%cmake_build

doxygen ./doc/Doxygen


%install
%cmake_install


%check
make test

if grep -r static %{buildroot}%{_libdir}/cmake; then
  : cmake configuration file contain reference to static library
  exit 1
fi


%files
%license LICENSE
%{_libdir}/libkms_message.so.%{soname}*
%{_libdir}/libmongocrypt.so.%{soname}*


%files devel
%doc *.md
%doc doc/html
%{_includedir}/kms_message
%{_includedir}/mongocrypt
%{_libdir}/libkms_message.so
%{_libdir}/libmongocrypt.so
%{_libdir}/cmake/kms_message
%{_libdir}/cmake/mongocrypt
%{_libdir}/pkgconfig/*.pc


%changelog
* Thu Sep  8 2022 Remi Collet <remi@remirepo.net> - 1.6.0-1
- update to 1.6.0

* Mon Aug  1 2022 Remi Collet <remi@remirepo.net> - 1.5.2-1
- update to 1.5.2

* Mon Jul 18 2022 Remi Collet <remi@remirepo.net> - 1.5.1-1
- update to 1.5.1
- open https://jira.mongodb.org/browse/MONGOCRYPT-451 build with shared libbson
- open https://jira.mongodb.org/browse/MONGOCRYPT-460 ABI/API breakage

* Fri Jun 17 2022 Remi Collet <remi@remirepo.net> - 1.4.1-1
- update to 1.4.1

* Wed Mar  2 2022 Remi Collet <remi@remirepo.net> - 1.3.1-1
- update to 1.3.1

* Fri Nov  5 2021 Remi Collet <remi@remirepo.net> - 1.3.0-1
- update to 1.3.0

* Wed Sep  8 2021 Remi Collet <remi@remirepo.net> - 1.2.2-1
- update to 1.2.2

* Tue Jul 13 2021 Remi Collet <remi@remirepo.net> - 1.2.1-1
- update to 1.2.1

* Fri Jan 22 2021 Remi Collet <remi@remirepo.net> - 1.2.0-1
- update to 1.2.0

* Tue Jan 12 2021 Remi Collet <remi@remirepo.net> - 1.1.0-1
- update to 1.1.0
- fix cmake macros usage

* Thu May 14 2020 Remi Collet <remi@remirepo.net> - 1.0.4-1
- update to 1.0.4

* Thu Feb 13 2020 Remi Collet <remi@remirepo.net> - 1.0.3-1
- update to 1.0.3
- drop patch merged upstream

* Wed Feb 12 2020 Remi Collet <remi@remirepo.net> - 1.0.2-1
- update to 1.0.2
- drop patches merged upstream
- install missing header using patch from
  https://github.com/mongodb/libmongocrypt/pull/90

* Sat Jan 18 2020 Remi Collet <remi@remirepo.net> - 1.0.1-2
- modernize spec from review #1792224
- add generated html documentation

* Fri Jan 17 2020 Remi Collet <remi@remirepo.net> - 1.0.1-1
- initial package
- fix installation layout using patch from
  https://github.com/mongodb/libmongocrypt/pull/87
