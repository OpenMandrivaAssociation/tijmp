%define gcj_support 0

Name:           tijmp
Version:        0.8
Release:        0.0.3
Epoch:          0
Summary:        Memory profiler for Java
URL:            http://www.khelekore.org/jmp/tijmp/
Source0:        http://www.khelekore.org/jmp/tijmp/tijmp-%{version}.tar.gz
License:        GPLv2+
Group:          Development/Java
BuildRequires:  gtk2-devel
BuildRequires:  java-rpmbuild
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%endif
BuildRequires:  pkgconfig
Obsoletes:      jmp <= 0:0.51

%description
TIJmp is a memory profiler for Java. TIJmp is made for Java 6 and
later, it will not work on Java 5 systems. If you need a profiler
for Java 5 or earlier, try the JMP profiler.

It is written to be fast and have a small footprint, both memory-
and CPU-wise. This means that the JVM will run at almost full speed,
until you use TIJmp to find some information.

It uses C code to talk to the JVM and it uses Swing to show the
tables of information. So TIJmp is written in C (using JVMTI and
JNI) and Java.

It runs in the same JVM as the program being profiled. This
means that it can easily get access to all things JVMTI/JNI has to
offer.

%prep
%setup -q
%{__perl} -pi -e 's/^libtijmp_la_LDFLAGS =.*/libtijmp_la_LDFLAGS = -avoid-version -module/' src/Makefile.{am,in}

%build
export CLASSPATH=""
export CFLAGS="`echo %{optflags} | sed 's/-O[0-9]*/-O3/'`"
%ifarch x86_64
export CFLAGS="-march=athlon64 ${CFLAGS}"
%endif
export JAVA_HOME=%{java_home}
%{configure2_5x}
%{make} JAVAC=${JAVA_HOME}/bin/javac JAVAH=${JAVA_HOME}/bin/javah JAR=${JAVA_HOME}/bin/jar

%install
export JAVA_HOME=%{java_home}
%{makeinstall_std} jardir=%{_jnidir} JAR=${JAVA_HOME}/bin/jar
(cd %{buildroot}%{_jnidir} && %{__mv} %{name}.jar %{name}-%{version}.jar && for jar in *-%{version}.jar; do %{__ln_s} ${jar} `/bin/echo ${jar} | %{__sed} "s|-%{version}||g"`; done)

%{gcj_compile}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README TODO
%{_jnidir}/%{name}-%{version}.jar
%{_jnidir}/%{name}.jar
%{gcj_files}
%attr(-,root,root) %{_libdir}/lib%{name}.so


%changelog
* Fri Nov 27 2009 Jérôme Brenier <incubusss@mandriva.org> 0:0.8-0.0.1mdv2010.1
+ Revision: 470585
- new version 0.8

* Wed Sep 09 2009 Thierry Vignaud <tvignaud@mandriva.com> 0:0.7-0.0.2mdv2010.0
+ Revision: 434366
- rebuild

* Mon Jun 30 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:0.7-0.0.1mdv2009.0
+ Revision: 230168
- new version 0.7

* Tue May 27 2008 Thierry Vignaud <tvignaud@mandriva.com> 0:0.6-0.0.3mdv2009.0
+ Revision: 211570
- description is not license tag
- do not write name on every description line

* Mon May 26 2008 David Walluck <walluck@mandriva.org> 0:0.6-0.0.2mdv2009.0
+ Revision: 211333
- update License
- remove BuildRequires: chrpath (no longer needed)
- remove specific java-rpmbuild setting since we are already at java 1.6+

* Mon May 26 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:0.6-0.0.1mdv2009.0
+ Revision: 211308
- new version and build with java-rpmbuild

* Tue Feb 26 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:0.5-2mdv2008.1
+ Revision: 175333
- new version

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:0.4-2mdv2008.1
+ Revision: 121033
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Thu Dec 13 2007 David Walluck <walluck@mandriva.org> 0:0.4-1mdv2008.1
+ Revision: 119463
- 0.4

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:0.3-2mdv2008.0
+ Revision: 87212
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Aug 04 2007 David Walluck <walluck@mandriva.org> 0:0.3-1mdv2008.0
+ Revision: 58771
- Import tijmp

