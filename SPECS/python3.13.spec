Name:           python3.13
Version:        3.13.0
Release:        1%{?dist}
Summary:        Python programming language, version 3.13

License:        Python
URL:            https://www.python.org/
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tgz

BuildRequires:  gcc, openssl-devel, bzip2-devel, libffi-devel, zlib-devel

%global __brp_python_bytecompile %{nil}
%global __requires_exclude ^/usr/local/bin/python3.13$

%description
Python is an interpreted, interactive, object-oriented programming language.

%prep
%setup -q -n Python-%{version}

%build
export PATH=%{buildroot}/usr/local/bin:$PATH
echo "Current PATH: $PATH"

./configure --enable-optimizations
make %{?_smp_mflags}

%install
export PATH=%{buildroot}/usr/local/bin:$PATH
echo "Current PATH: $PATH"

make altinstall DESTDIR=%{buildroot}

# delete unused files
rm -rf %{buildroot}/usr/local/include

%files
/usr/local/bin/*
/usr/local/lib/python3.13
/usr/local/lib/pkgconfig/*
/usr/local/lib/libpython3.13.a
/usr/local/share/*
