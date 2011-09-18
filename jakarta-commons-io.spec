# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global with_maven 0
%global base_name commons-io

Name:           jakarta-commons-io
Version:        1.4
Release:        3%{?dist}
Epoch:          0
Summary:        Utilities to assist with developing IO functionality 

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://commons.apache.org/io/
Source0:        http://archive.apache.org/dist/commons/io/source/commons-io-%{version}-src.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  junit >= 0:3.8.1
BuildRequires:  dos2unix
%if %{with_maven}
BuildRequires:  maven2 >= 2.0.4-10jpp
BuildRequires:  maven2-plugin-assembly
BuildRequires:  maven2-plugin-antrun
BuildRequires:  maven-plugin-bundle
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-idea
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-doxia-sitetools
%endif
Requires:       jpackage-utils
Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2
%description
Commons-IO contains utility classes, stream implementations, 
file filters, and endian classes. It is a library of utilities 
to assist with developing IO functionality.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Documentation

%description    javadoc
Javadoc for %{name}

%prep
%setup -q -n %{base_name}-%{version}-src
dos2unix *.txt

%build
%if %{with_maven}
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
        -e \
        -s $(pwd)/settings.xml \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        install javadoc:javadoc
%endif
ant jar javadoc

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -pm 644 target/%{base_name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{base_name}-%{version}.jar
ln -s %{base_name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{base_name}.jar

%if %{with_maven}
%add_to_maven_depmap %{base_name} %{base_name} %{version} JPP %{base_name}

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}.pom
%endif

install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%if %{with_maven}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%else
cp -pr target/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%endif
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with_maven}
%post
%update_maven_depmap

%postun
%update_maven_depmap
%endif

%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/*.jar
%if %{with_maven}
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%endif

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%changelog
* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0:1.4-3
- Add dos2unix BR and fix line endings in .txt files

* Mon Dec 14 2009 Andrew Overholt <overholt@redhat.com> 0:1.4-2
- Build with ant.

* Fri Sep 18 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.4-1
- Update to upstream 1.4.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.3.2-1.2 
- drop repotag
- fix license tag

* Tue Jan 22 2008 Permaine Cheung <pcheung@redhat.com> - 0:1.3.2-1jpp.1
- Merge with upstream

* Fri Jul 20 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.3.2-1jpp
- Upgrade to 1.3.2
- Build with maven2 by default
- Add pom and depmap frag

* Tue May 15 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.2-4jpp
- Make Vendor, Distribution based on macro

* Tue Feb 13 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.2-3jpp
- Add gcj_support option


* Tue Feb 13 2007 Deepak Bhole <dbhole@redhat.com> - 0:1.2-3jpp.1.fc7
- Fix spec per Fedora guidelines.

* Thu Jun 22 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.2-2jpp
- Thx Olav

* Sun Jun 18 2006 Olav Reinert <oreinert at users.sourceforge.net> - 0:1.2-1jpp
- Upgrade to 1.2

* Fri Feb 24 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.1-0.20051005.2jpp
- First JPP 1.7 build

* Wed Oct 05 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.1-0.20051005.1jpp
- Upgrade to 1.1 dev

* Wed Oct 05 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.0-1jpp
- Upgrade to 1.0 final

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:1.0.cvs20040118-4jpp
- Rebuild with ant-1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0.cvs20040118-3jpp
- Void change

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:1.0.cvs20040118-2jpp
- Upgrade to Ant 1.6.X

* Mon Jan 19 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0.cvs20040118-1jpp
- First JPackage release
