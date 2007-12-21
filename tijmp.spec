%define gcj_support 1

Name:           tijmp
Version:        0.4
Release:        %mkrel 2
Epoch:          0
Summary:        Memory profiler for Java
URL:            http://www.khelekore.org/jmp/tijmp/
Source0:        http://www.khelekore.org/jmp/tijmp/tijmp-%{version}.tar.gz
License:        GPL
Group:          Development/Java
Requires:       java >= 1.6.0
BuildRequires:  chrpath
BuildRequires:  gtk2-devel
BuildRequires:  java-rpmbuild
BuildRequires:  java-devel-icedtea
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%endif
BuildRequires:  pkgconfig
Obsoletes:      jmp <= 0:0.51
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
TIJmp is a memory profiler for Java. TIJmp is made for Java 6 and
later, it will not work on Java 5 systems. If you need a profiler
for Java 5 or earlier, try the JMP profiler.

TIJmp is written to be fast and have a small footprint, both memory-
and CPU-wise. This means that the JVM will run at almost full speed,
until you use TIJmp to find some information.

TIJmp uses C code to talk to the JVM and it uses Swing to show the
tables of information. So TIJmp is written in C (using JVMTI and
JNI) and Java.

TIJmp runs in the same JVM as the program being profiled. This
means that it can easily get access to all things JVMTI/JNI has to
offer.

TIJmp is distributed under the General Public License, GPL.

%prep
%setup -q
%{__perl} -pi -e 's/^libtijmp_la_LDFLAGS =.*/libtijmp_la_LDFLAGS = -avoid-version -module/' src/Makefile.{am,in}

%build
export CLASSPATH=""
export JAVA_HOME="%{_jvmdir}/java-icedtea"
export CFLAGS="`echo %{optflags} | sed 's/-O[0-9]*/-O3/'`"
%ifarch x86_64
export CFLAGS="-march=athlon64 ${CFLAGS}"
%endif
%{configure2_5x}
%{make} JAVAC=${JAVA_HOME}/bin/javac JAVAH=${JAVA_HOME}/bin/javah JAR=${JAVA_HOME}/bin/jar

%install
%{__rm} -rf %{buildroot}
export JAVA_HOME="%{_jvmdir}/java-icedtea"
%{makeinstall_std} jardir=%{_jnidir} JAR=${JAVA_HOME}/bin/jar
(cd %{buildroot}%{_jnidir} && %{__mv} %{name}.jar %{name}-%{version}.jar && for jar in *-%{version}.jar; do %{__ln_s} ${jar} `/bin/echo ${jar} | %{__sed} "s|-%{version}||g"`; done)

pushd %{buildroot}%{_libdir}
#%{_bindir}/chrpath -d lib%{name}.so.*.*.*
%{__rm} lib%{name}.la
popd

%find_lang %{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files -f %{name}.lang
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README TODO
%{_jnidir}/%{name}-%{version}.jar
%{_jnidir}/%{name}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
%attr(-,root,root) %{_libdir}/lib%{name}.so
