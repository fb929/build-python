Name:           python3.13
Version:        3.13.0
Release:        1%{?dist}
Summary:        Python programming language, version 3.13

License:        Python
URL:            https://www.python.org/
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tgz

BuildRequires:  gcc, openssl-devel, bzip2-devel, libffi-devel, zlib-devel

%description
Python is an interpreted, interactive, object-oriented programming language.

%prep
%setup -q -n Python-%{version}

%build
./configure --enable-optimizations
make %{?_smp_mflags}

%install
make altinstall DESTDIR=%{buildroot}

%files
/usr/local/bin/python3.13
/usr/local/lib/python3.13
