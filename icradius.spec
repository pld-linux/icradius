Summary:	RADIUS Server
Summary(pl):	Serwer RADIUS
Name:		icradius
Version:	0.17b
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.innercite.com/pub/icradius/%{name}-%{version}.tar.gz
Source1:	%{name}.pamd
Source2:	%{name}.initd
Source3:	%{name}.logrotate
Patch0:		%{name}-radius_dir.patch
BuildRequires:	mysql-devel
BuildRequires:	pam-devel
URL:		http://radius.innercite.com/
Requires:	perl-Authen-Radius >= 0.05
Requires:	perl >= 5.6.0
Provides:	radius
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	radius

%description
RADIUS server with MySQL backend based on Cistron Radius.

%package cgi
Summary:	ICRADIUS web interface.
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	%{name} = %{version}
Requires:	httpd

%description cgi
ICRADIUS web interface.

%package mysql
Summary:	ICRADIUS MySQL Backend
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	%{name} = %{version}
Requires:	perl
Requires:	mysql-client

%description mysql
ICRADIUS MySQL Backend.

%prep
%setup -q
%patch0 -p1

%build
cd src
%{__make} PAM=-DPAM PAMLIB="-lpam -ldl" CFLAGS="%{rpmcflags}"
cd ..

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT%{_datadir}/%{name} \
	$RPM_BUILD_ROOT/home/httpd/html/%{name}/images \
	$RPM_BUILD_ROOT%{_sysconfdir}/raddb \
	$RPM_BUILD_ROOT%{_sysconfdir}/pam.d \
	$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d \
	$RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d \
	$RPM_BUILD_ROOT%{_mandir}/man8 \
	$RPM_BUILD_ROOT/var/log/radacct

install src/{radiusd,checkrad.pl} \
	$RPM_BUILD_ROOT/%{_sbindir}
install scripts/{radlast,radwatch,radwho,testrad,syncaccounting.pl} \
	$RPM_BUILD_ROOT/%{_sbindir}

#db
install scripts/{radius.db,acctexport.pl,acctimport.pl,acctsummarize.pl} \
	scripts/{dictimport.pl,radiusfixup.pl,userexport.pl,userimport.pl} \
	$RPM_BUILD_ROOT/%{_datadir}/%{name}

#cgi
install scripts/images/* \
	$RPM_BUILD_ROOT/home/httpd/html/%{name}/images
install scripts/{radius.cgi,usage.cgi} \
	$RPM_BUILD_ROOT/home/httpd/html/%{name}

#etc
install raddb/* 	$RPM_BUILD_ROOT%{_sysconfdir}/raddb
install %{SOURCE1}	$RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/radius
install %{SOURCE2}	$RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/radius
install %{SOURCE3}	$RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/radius

install doc/*.8		$RPM_BUILD_ROOT%{_mandir}/man8
gzip -9nf scripts/{README,deloldsess.sh,radiusd.cron.daily}
	scripts/{radiusd.cron.monthly,rc.radiusd,usonlineconv.pl}
gzip -9nf {COPYING,COPYRIGHT.Cistron,COPYRIGHT.ICRADIUS,COPYRIGHT.Livingston} \
	doc/{ChangeLog,ChangeLog.cistron,FAQ,THANKS,TODO} \
	doc/{README,README.Y2K,README.cisco,README.hints,README.proxy,README.simul} \

:> $RPM_BUILD_ROOT/var/log/rad{u,w}tmp
:> $RPM_BUILD_ROOT/var/log/radwtmp
:> $RPM_BUILD_ROOT/var/log/radius.log

%post
touch /var/log/rad{u,w}tmp
/sbin/chkconfig --add radius
if test -r /var/lock/subsys/radius; then
	/etc/rc.d/init.d/radius restart >&2
else
	echo "Run \"/etc/rc.d/init.d/radius start\" to start radius daemon."
fi

%preun
if [ "$1" = "0" ]; then
	/etc/rc.d/init.d/radius stop >&2
	/sbin/chkconfig --del radius
fi

%post mysql
echo radius.db

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/{ChangeLog,README,README.pam,README.proxy}.gz
%doc scripts/*.gz

%attr(750,root,root) %dir /var/log/radacct
%attr(750,root,root) %dir %{_sysconfdir}/raddb

%attr(640,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/raddb/*

%attr(755,root,root) %{_sbindir}/*
%attr(644,root,root) %{_mandir}/*/*

%attr(754,root,root) /etc/rc.d/init.d/radius
%attr(640,root,root) /etc/logrotate.d/radius

%attr(640,root,root) %ghost /var/log/radutmp
%attr(640,root,root) %ghost /var/log/radwtmp
%attr(640,root,root) %ghost /var/log/radius.log

%files cgi
%defattr(644,root,root,755)
%attr(755,root,root) /home/httpd/html/%{name}/*

%files mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{_datadir}/%{name}/*
