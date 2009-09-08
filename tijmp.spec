%define gcj_support 0

Name:           tijmp
Version:        0.7
Release:        %mkrel 0.0.2
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
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
%{__rm} -rf %{buildroot}
export JAVA_HOME=%{java_home}
%{makeinstall_std} jardir=%{_jnidir} JAR=${JAVA_HOME}/bin/jar
(cd %{buildroot}%{_jnidir} && %{__mv} %{name}.jar %{name}-%{version}.jar && for jar in *-%{version}.jar; do %{__ln_s} ${jar} `/bin/echo ${jar} | %{__sed} "s|-%{version}||g"`; done)
%{__rm} %{buildroot}%{_libdir}/libtijmp.la

%find_lang %{name}

%{gcj_compile}

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
%{gcj_files}
%attr(-,root,root) %{_libdir}/lib%{name}.so
