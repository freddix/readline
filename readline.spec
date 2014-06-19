%define		ver		6.3
%define		patchlevel	6

Summary:	GNU Readline library
Name:		readline
Version:	%{ver}%{?patchlevel:.%{patchlevel}}
Release:	1
License:	GPL
Group:		Core/Libraries
Source0:	ftp://ftp.cwru.edu/pub/bash/%{name}-%{ver}.tar.gz
# Source0-md5:	33c8fb279e981274f485fd91da77e94a
Source1:	%{name}-sys_inputrc
%patchset_source -f http://ftp.gnu.org/gnu/readline/readline-6.3-patches/readline63-%03g 1 %{patchlevel}
URL:		http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ncurses-devel
BuildRequires:	texinfo
Requires(post,postun):	/usr/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The GNU Readline library provides a set of functions for use by
applications that allow users to edit command lines as they are typed
in.

%package devel
Summary:	Header files and libraries for readline development
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ncurses-devel

%description devel
This package contains the header files and libraries needed
to develop programs that use the readline library.

%prep
%setup -qn %{name}-%{ver}
%patchset_patch -p2 1 %{patchlevel}

%build
cp -f /usr/share/automake/config.sub support
mv -f aclocal.m4 acinclude.m4
%{__aclocal}
%{__autoconf}
%configure \
	--disable-static	\
	--with-curses
%{__make} SHLIB_LIBS=-lncurses

%{__rm} doc/*.info
%{__make} -C doc info

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/inputrc

%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/*old

# rpm auto deps
chmod +x $RPM_BUILD_ROOT%{_libdir}/lib*.so*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
/usr/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/inputrc
%attr(755,root,root) %ghost %{_libdir}/libhistory.so.?
%attr(755,root,root) %ghost %{_libdir}/libreadline.so.?
%attr(755,root,root) %{_libdir}/libhistory.so.*.*
%attr(755,root,root) %{_libdir}/libreadline.so.*.*
%{_infodir}/*info*

%files devel
%defattr(644,root,root,755)
%{_includedir}/readline
%attr(755,root,root) %{_libdir}/libhistory.so
%attr(755,root,root) %{_libdir}/libreadline.so
%{_mandir}/man3/*

