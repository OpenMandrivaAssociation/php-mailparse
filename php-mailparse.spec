%define modname mailparse
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A12_%{modname}.ini

Summary:	Email message manipulation for PHP
Name:		php-%{modname}
Version:	2.1.5
Release:	%mkrel 3
License:	PHP License
Group:		Development/PHP
URL:		http://pecl.php.net/package/mailparse
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Source1:	%{modname}.ini
Patch0:		mailparse-0.9.4-silly_fix.patch
Patch1:		mailparse-2.1.5-libmbfl_is_external.diff
Requires:	php-cli >= 3:5.2.0
Requires:	php-mbstring
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	mbfl-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Mailparse is an extension for parsing and working with email messages. It can
deal with rfc822 and rfc2045 (MIME) compliant messages. 

%prep

%setup -q -n %{modname}-%{version}
%patch0 -p0
%patch1 -p0

# fix strange attribs
find tests -type f|xargs chmod 644

ln -s %{_usrsrc}/php-devel/ext .

cp %{SOURCE1} %{inifile}

%build
%serverbuild

phpize
%configure2_5x \
    --enable-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc tests CREDITS README try.php
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
