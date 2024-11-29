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

# fix files path
install --mode=0755 --directory %{buildroot}/usr
install --mode=0555 --directory %{buildroot}/bin %{buildroot}/usr/lib64
install --mode=0755 --directory \
    %{buildroot}/usr/lib64/python3.13 \
    %{buildroot}/usr/lib64/pkgconfig \
    %{buildroot}/usr/share
mv %{buildroot}/usr/local/bin/* %{buildroot}/bin/
mv %{buildroot}/usr/local/lib/python3.13/* %{buildroot}/usr/lib64/python3.13/
mv %{buildroot}/usr/local/lib/pkgconfig/* %{buildroot}/usr/lib64/pkgconfig/
mv %{buildroot}/usr/local/lib/libpython3.13.a %{buildroot}/usr/lib64/
mv %{buildroot}/usr/local/share/* %{buildroot}/usr/share/
rm -rf %{buildroot}/usr/local/include

%files
/bin/*
/usr/lib64/*
/usr/share/*
