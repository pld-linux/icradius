%include	/usr/lib/rpm/macros.perl
Summary:	RADIUS Server
Summary(pl):	Serwer RADIUS
Name:		icradius
Version:	0.17b
Release:	8
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.innercite.com/pub/icradius/%{name}-%{version}.tar.gz
# Source0-md5:	ff8eef808dbc601ea120617b787af26b
Source1:	%{name}.pamd
Source2:	%{name}.initd
Source3:	%{name}.logrotate
Source4:	%{name}.QUICKSTART.txt
Source5:	%{name}-ICRadiusCFG.pm
Source6:	%{name}-dictionary.cisco
Source7:	%{name}-dictionary.default
Patch0:		%{name}-radius_dir.patch
Patch1:		%{name}-ICRadiusCFG.patch
Patch2:		%{name}-Cisco-VOIP.patch
URL:		http://radius.innercite.com/
Requires:	perl-Authen-Radius >= 0.05
Requires:	perl >= 5.6.0
Requires:	mysql
Prereq:		/sbin/chkconfig
BuildRequires:	mysql-devel
BuildRequires:	pam-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Provides:	radius
Obsoletes:	radius

%description
RADIUS server with MySQL backend based on Cistron Radius.

%description -l pl
Serwer RADIUS z backendem MySQL bazowanym na Cistron Radius.

%package cgi
Summary:	ICRADIUS web interface
Summary(pl):	Interfejs WWW do ICRADIUS
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	%{name} = %{version}
Requires:	httpd

%description cgi
ICRADIUS web interface.

%description cgi -l pl
Interfejs WWW do ICRADIUS.

%package perl
Summary:	ICRADIUS perl scripts
Summary(pl):	Skrypty perlowe ICRADIUS
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	%{name} = %{version}
Requires:	perl
Requires:	perl-Msql-Mysql-modules
Requires:	perl-Authen-Radius >= 0.05
BuildRequires:	rpm-perlprov

%description perl
ICRADIUS perl scripts.

%description perl -l pl
Skrypty perlowe ICRADIUS.

%package dictionaries
Summary:	RADIUS dictionaries
Summary(pl):	S�owniki RADIUS
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	%{name} = %{version}

%description dictionaries
RADIUS dictionaries.

%description dictionaries -l pl
S�owniki RADIUS.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd src
%{__make} PAM=-DPAM PAMLIB="-lpam -ldl" CFLAGS="%{rpmcflags}"
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/dictionaries \
	$RPM_BUILD_ROOT/home/httpd/html/%{name}/images \
	$RPM_BUILD_ROOT%{_sysconfdir}/raddb \
	$RPM_BUILD_ROOT%{_sysconfdir}/pam.d \
	$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d \
	$RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d \
	$RPM_BUILD_ROOT%{_mandir}/man8 \
	$RPM_BUILD_ROOT/var/log/radacct \
	$RPM_BUILD_ROOT%{perl_sitearch}

install src/radiusd scripts/{radlast,radwho,testrad,radwatch} \
	$RPM_BUILD_ROOT/%{_sbindir}

#perl
install src/checkrad.pl \
			scripts/{radius.db,acctexport.pl,acctimport.pl,acctsummarize.pl} \
			scripts/{dictimport.pl,radiusfixup.pl,userexport.pl} \
			scripts/{userimport.pl,syncaccounting.pl} \
			$RPM_BUILD_ROOT/%{_datadir}/%{name}

#dictionaries
install raddb/dictionary* \
			$RPM_BUILD_ROOT/%{_datadir}/%{name}/dictionaries
install	%{SOURCE6} $RPM_BUILD_ROOT/%{_datadir}/%{name}/dictionaries/dictionary.cisco-new
install	%{SOURCE7} $RPM_BUILD_ROOT/%{_datadir}/%{name}/dictionaries/dictionary.cistron_default

#cgi
install scripts/images/* \
	$RPM_BUILD_ROOT/home/httpd/html/%{name}/images
install scripts/{radius.cgi,usage.cgi} \
	$RPM_BUILD_ROOT/home/httpd/html/%{name}

#etc
install raddb/radius.conf 	$RPM_BUILD_ROOT%{_sysconfdir}/raddb
install raddb/huntgroups 	$RPM_BUILD_ROOT%{_sysconfdir}/raddb
install %{SOURCE1}	$RPM_BUILD_ROOT/etc/pam.d/radius
install %{SOURCE2}	$RPM_BUILD_ROOT/etc/rc.d/init.d/radius
install %{SOURCE3}	$RPM_BUILD_ROOT/etc/logrotate.d/radius
install %{SOURCE4}	doc/QUICKSTART.txt
install %{SOURCE5}	$RPM_BUILD_ROOT/%{perl_sitearch}/ICRadiusCFG.pm

install doc/*.8		$RPM_BUILD_ROOT%{_mandir}/man8
gzip -9nf scripts/{README,deloldsess.sh,radiusd.cron.daily} \
	scripts/{radiusd.cron.monthly,rc.radiusd,usonlineconv.pl} \
	{COPYING,COPYRIGHT.Cistron,COPYRIGHT.ICRADIUS,COPYRIGHT.Livingston} \
	doc/{ChangeLog,ChangeLog.cistron,FAQ,THANKS,TODO} \
	doc/{README,README.Y2K,README.cisco,README.hints,README.proxy,README.simul} \
	doc/QUICKSTART.txt

gzip -9nf $RPM_BUILD_ROOT/%{_datadir}/%{name}/dictionaries/*

:> $RPM_BUILD_ROOT/var/log/radutmp
:> $RPM_BUILD_ROOT/var/log/radwtmp
:> $RPM_BUILD_ROOT/var/log/radius.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch /var/log/rad{u,w}tmp
/sbin/chkconfig --add radius
if [ -r /var/lock/subsys/radiusd ]; then
	/etc/rc.d/init.d/radius restart >&2
else
	echo "Run \"/etc/rc.d/init.d/radius start\" to start radius daemon."
	echo "Don't forget to read"
	echo "	%{_docdir}/%{name}-%{version}/QUICKSTART.txt.gz"
	echo "if you find problems with running daemon"
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/radiusd ]; then
		/etc/rc.d/init.d/radius stop >&2
	fi
	/sbin/chkconfig --del radius
fi

%files
%defattr(644,root,root,755)
%doc {COPYING,COPYRIGHT.Cistron,COPYRIGHT.ICRADIUS,COPYRIGHT.Livingston}.gz
%doc doc/{ChangeLog,ChangeLog.cistron,FAQ,THANKS,TODO}.gz
%doc doc/{README,README.Y2K,README.cisco,README.hints,README.proxy,README.simul}.gz
%doc scripts/*.gz
%doc doc/QUICKSTART.txt.gz

%attr(750,root,root) %dir /var/log/radacct
%attr(751,root,root) %dir %{_sysconfdir}/raddb

%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/raddb/*

%attr(755,root,root) %{_sbindir}/radiusd
%attr(755,root,root) %{_sbindir}/radwatch
%attr(644,root,root) %{_mandir}/*/*
%attr(644,root,root) %{_datadir}/%{name}/radius.db

%attr(754,root,root) /etc/rc.d/init.d/radius
%attr(640,root,root) /etc/logrotate.d/radius

%attr(640,root,root) %ghost /var/log/radutmp
%attr(640,root,root) %ghost /var/log/radwtmp
%attr(640,root,root) %ghost /var/log/radius.log

%files cgi
%defattr(644,root,root,755)
%attr(755,root,root) /home/httpd/html/%{name}/*

%files perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/radlast
%attr(755,root,root) %{_sbindir}/radwho
%attr(755,root,root) %{_sbindir}/testrad
%attr(755,root,root) %{_datadir}/%{name}/*.pl
%{perl_sitearch}/ICRadiusCFG.pm

%files dictionaries
%defattr(644,root,root,755)
%attr(644,root,root) %{_datadir}/%{name}/dictionaries/*
