%define modname mailparse
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A12_%{modname}.ini

Summary:	Email message manipulation for PHP
Name:		php-%{modname}
Version:	2.1.6
Release:	3
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


%changelog
* Wed May 02 2012 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.6-2mdv2012.0
+ Revision: 794913
- rebuild for php-5.4.x

* Tue Apr 10 2012 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.6-1
+ Revision: 790122
- 2.1.6

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.5-17
+ Revision: 761118
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.5-16
+ Revision: 696369
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.5-15
+ Revision: 695313
- rebuilt for php-5.3.7

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.5-14
+ Revision: 667480
- mass rebuild

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.5-13
+ Revision: 646553
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.5-12mdv2011.0
+ Revision: 629739
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.5-11mdv2011.0
+ Revision: 628045
- ensure it's built without automake1.7

* Tue Nov 23 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.5-10mdv2011.0
+ Revision: 600177
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.5-9mdv2011.0
+ Revision: 588714
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.5-8mdv2010.1
+ Revision: 514568
- rebuilt for php-5.3.2

* Mon Feb 22 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.5-7mdv2010.1
+ Revision: 509467
- rebuild
- rebuild

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.5-5mdv2010.1
+ Revision: 485260
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.5-4mdv2010.1
+ Revision: 468087
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.5-3mdv2010.0
+ Revision: 451217
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1:2.1.5-2mdv2010.0
+ Revision: 397548
- Rebuild

* Wed May 13 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.5-1mdv2010.0
+ Revision: 375423
- fix deps (mbfl-devel)
- 2.1.5
- fix build (P1)

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.4-7mdv2009.1
+ Revision: 346513
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.4-6mdv2009.1
+ Revision: 341510
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.4-5mdv2009.1
+ Revision: 321769
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.4-4mdv2009.1
+ Revision: 310219
- rebuilt against php-5.2.7

* Tue Jul 15 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.4-3mdv2009.0
+ Revision: 235878
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.4-2mdv2009.0
+ Revision: 200110
- rebuilt against php-5.2.6

* Wed Apr 09 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.4-1mdv2009.0
+ Revision: 192503
- 2.1.4

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.3-2mdv2008.1
+ Revision: 161942
- rebuild

* Wed Jan 09 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.3-1mdv2008.1
+ Revision: 147167
- 2.1.3

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.2-2mdv2008.1
+ Revision: 107571
- restart apache if needed

* Thu Nov 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.2-1mdv2008.1
+ Revision: 106948
- 2.1.2

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.1-11mdv2008.0
+ Revision: 77458
- rebuilt against php-5.2.4

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.1-10mdv2008.0
+ Revision: 64302
- use the new %%serverbuild macro

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.1-9mdv2008.0
+ Revision: 39385
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.1-8mdv2008.0
+ Revision: 33780
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.1-7mdv2008.0
+ Revision: 21029
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.1-6mdv2007.0
+ Revision: 117535
- rebuilt against new upstream version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.1-5mdv2007.0
+ Revision: 78208
- re-submitted
- fix deps
- bunzip patches and sources

* Tue Nov 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.1-4mdv2007.1
+ Revision: 77361
- rebuilt for php-5.2.0

* Thu Nov 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.1-3mdv2007.1
+ Revision: 75250
- Import php-mailparse

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.1-3
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.1-2mdk
- rebuild

* Mon May 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.1-1mdk
- 2.1.1
- drop upstream patches; P1

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-7mdk
- rebuilt for php-5.1.4

* Fri May 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-6mdk
- rebuilt for php-5.1.3

* Thu Feb 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-5mdk
- new group (Development/PHP) and iurt rebuild

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-4mdk
- rebuilt against php-5.1.2

* Tue Nov 29 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-3mdk
- rebuilt against php-5.1.1

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-2mdk
- rebuilt against php-5.1.0

* Thu Nov 03 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-1mdk
- rebuilt against php-5.1.0RC4
- fix versioning

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_2.1-0.RC1.1mdk
- rebuilt for php-5.1.0RC1

* Tue Sep 13 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_2.1-2mdk
- added P1 to fix http://bugs.php.net/bug.php?id=32999

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_2.1-1mdk
- rename the package

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_2.1-1mdk
- 5.0.4

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_2.1-3mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_2.1-2mdk
- rebuilt against a non hardened-php aware php lib

* Sun Jan 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_2.1-1mdk
- 2.1
- rebuild due to hardened-php-0.2.6

* Fri Dec 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_2.0b-1mdk
- rebuilt for php-5.0.3

* Sat Sep 25 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.2_2.0b-1mdk
- rebuilt for php-5.0.2

* Sun Aug 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.1_2.0b-1mdk
- rebuilt for php-5.0.1

* Wed Aug 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.0_2.0b-1mdk
- rebuilt for php-5.0.0
- major cleanups

* Thu Jul 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_2.0b-1mdk
- rebuilt for php-4.3.8

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_2.0b-2mdk
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_2.0b-1mdk
- rebuilt for php-4.3.7

* Mon May 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_2.0b-2mdk
- use the %%configure2_5x macro
- move scandir to /etc/php.d

* Thu May 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_2.0b-1mdk
- 2.0b
- fix url
- built for php 4.3.6

