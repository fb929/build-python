Name:           python3.11
Version:        3.11.11
Release:        1%{?dist}
Summary:        Python programming language, version 3.11

License:        Python
URL:            https://www.python.org/
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tgz

BuildRequires:  gcc, openssl11-devel, bzip2-devel, libffi-devel, zlib-devel

%if 0%{?amzn}
Requires:       chkconfig
%else
Requires:       alternatives
%endif
Provides:       alternative-for(python)

%global __brp_python_bytecompile %{nil}
%global __requires_exclude ^/usr/local/bin/python3.11$
%global __requires_exclude ^/usr/local/bin/python$
%global alternatives_files %{_bindir}/python3 %{_mandir}/man1/python3.1.gz %{_bindir}/pip3 %{_bindir}/pydoc3 %{_bindir}/idle3 %{_bindir}/python3-config

%description
Python is an interpreted, interactive, object-oriented programming language.

%prep
%setup -q -n Python-%{version}

%build
export PATH=%{buildroot}/usr/local/bin:$PATH
echo "Current PATH: $PATH"

./configure \
    --enable-optimizations \
    --with-openssl=/usr
make %{?_smp_mflags}

%install
export PATH=%{buildroot}/usr/local/bin:$PATH
echo "Current PATH: $PATH"

make altinstall DESTDIR=%{buildroot}

# All ghost files controlled by alternatives need to exist for the files
# section check to succeed
# - Don't list /usr/bin/python as a ghost file so `yum install /usr/bin/python`
#   doesn't install this package
install -d \
    %{buildroot}%{_bindir} \
    %{buildroot}%{_mandir}/man1
for FILE in %{alternatives_files}; do
    touch %{buildroot}${FILE}
done

# ======================================================
# Scriptlets for alternatives
# ======================================================
%post
# save origin link
for FILE in %{alternatives_files}; do
    if [ -e "${FILE}" ]; then
        mv ${FILE} ${FILE}.origin_system
    fi
done
# set up alternatives
alternatives \
    --install %{_bindir}/python3 python3 /usr/local/bin/python3.11 300 \
    --slave   %{_mandir}/man1/python3.1.gz python3-man /usr/local/share/man/man1/python3.11.1 \
    --slave   %{_bindir}/pip3 pip3 /usr/local/bin/pip3.11 \
    --slave   %{_bindir}/pydoc3 pydoc3 /usr/local/bin/pydoc3.11 \
    --slave   %{_bindir}/idle3 idle3 /usr/local/bin/idle3.11 \
    --slave   %{_bindir}/python3-config python3-config /usr/local/bin/python3.11-config

%postun
# Do this only during uninstall process (not during update)
if [ $1 -eq 0 ]; then
    alternatives --remove python3 /usr/local/bin/python3.11
    # resteore origin link
    for FILE in %{alternatives_files}; do
        if [ -e "${FILE}.origin_system" ]; then
            mv ${FILE}.origin_system ${FILE}
        fi
    done
    if [ -d /usr/local/lib/python3.11 ]; then
        rm -rf /usr/local/lib/python3.11
    fi
fi

%files
# Alternatives
%ghost %{_bindir}/python3
%ghost %{_mandir}/man1/python3.1.gz
%ghost %{_bindir}/pip3
%ghost %{_bindir}/pydoc3
%ghost %{_bindir}/idle3
%ghost %{_bindir}/python3-config

/usr/local/bin/*
/usr/local/lib/python3.11
/usr/local/lib/pkgconfig/*
/usr/local/lib/libpython3.11.a
/usr/local/share/*
/usr/local/include/*
