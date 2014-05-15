%define		ver		6.3
%define		patchlevel	5

Summary:	Library for reading lines from a terminal
Name:		readline
Version:	%{ver}%{?patchlevel:.%{patchlevel}}
Release:	1
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.cwru.edu/pub/bash/%{name}-%{ver}.tar.gz
# Source0-md5:	33c8fb279e981274f485fd91da77e94a
Source1:	%{name}-sys_inputrc
#Patch1000:	%{name}-patchlevel-%{patchlevel}.patch
%patchset_source -f http://ftp.gnu.org/gnu/readline/readline-6.3-patches/readline63-%03g 1 %{patchlevel}
URL:		http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ncurses-devel
BuildRequires:	texinfo
Requires(post,postun):	/usr/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The "readline" library will read a line from the terminal and return
it, allowing the user to edit the line with the standard emacs editing
keys. It allows the programmer to give the user an easier-to-use and
more intuitive interface.

%package devel
Summary:	file for developing programs that use the readline library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ncurses-devel

%description devel
The "readline" library will read a line from the terminal and return
it, using prompt as a prompt. If prompt is null, no prompt is issued.
The line returned is allocated with malloc(3), so the caller must free
it when finished. The line returned has the final newline removed, so
only the text of the line remains.

%prep
%setup -qn %{name}-%{ver}
#%patch1000 -p0
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

