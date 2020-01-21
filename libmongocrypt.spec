# remirepo/fedora spec file for libmongocrypt
#
# Copyright (c) 2020 Remi Collet
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
Version:   1.0.1
Release:   2%{?dist}

# see kms-message/THIRD_PARTY_NOTICES
# kms-message/src/kms_b64.c is ISC
# everything else is ASL 2.0
License:   ASL 2.0 and ISC
URL:       https://github.com/%{gh_owner}/%{gh_project}

Source0:   https://github.com/%{gh_owner}/%{gh_project}/archive/%{version}.tar.gz

# Fix install layout, PR #87
Patch0:    0001-fix-installation-layout-e.g.-honors-GNUInstallDirs.patch
Patch1:    0002-add-option-to-NOT-install-static-libraries.patch

BuildRequires: cmake >= 3.5
BuildRequires: gcc
BuildRequires: gcc-c++
# pkg-config may pull compat-openssl10
BuildRequires: openssl-devel
# should be libson-1.0 only available in 1.16
BuildRequires: cmake(libbson-1.0) >= 1.11
# for documentation
BuildRequires: doxygen


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
    -DCMAKE_C_FLAGS="%{optflags} -fPIC" \
    -DENABLE_SHARED_BSON:BOOL=ON \
    -DENABLE_STATIC:BOOL=OFF \
    .

%make_build

doxygen ./doc/Doxygen


%install
%make_install


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
* Sat Jan 18 2020 Remi Collet <remi@remirepo.net> - 1.0.1-2
- modernize spec from review #1792224
- add generated html documentation

* Fri Jan 17 2020 Remi Collet <remi@remirepo.net> - 1.0.1-1
- initial package
- fix installation layout using patch from
  https://github.com/mongodb/libmongocrypt/pull/87