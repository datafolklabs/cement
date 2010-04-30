%{!?pyver: %global pyver %(%{__python} -c "import sys ; print sys.version[:3]")}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}

%global basever 0.8

Name:           Cement
Version:        0.8     
Release:        1%{?dist}
Summary:        CLI Application Framework for Python

Group:          Development/Libraries        
License:        MIT
URL:            http://builtoncement.org
Source0:        http://builtoncement.org/stable/0.8/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: %{name}(api) = 0.7-0.8:20100210

BuildRequires:  python-devel, python-setuptools
BuildRequires:  python-nose
Requires:       python >= %{pyver}
Requires:       python-configobj, python-jsonpickle, python-genshi

# avoid setuptools installing un-necessary deps for rpm install
Patch0: Cement-0.8-noreqs.patch
# doc requires cement to be installed/importable to grab version, and such
Patch1: Cement-0.8-doc.patch
Patch2: Cement-0.8-tests.patch

%description
Cement is an advanced CLI Application Framework for Python. It promotes code
re-use by way of plugins and helper libraries that can be shared between
any application built on Cement.  The MVC and overall framework design is
very much inspired by the TurboGears2 web framework.  Its goal is to introduce
a standard, and feature-full platform for both simple and complex command
line applications as well as support rapid development needs without sacrificing
quality.

At a minimum, Cement configures the following features for every application:
::
     * Multiple Configuration file parsing (default: /etc, ~/)
     * Command line argument and option parsing
     * Dual Console/File Logging Support
     * Full Internal and External (3rd Party) Plugin support
     * Basic "hook" support
     * Full MVC support for advanced application design
     * Text output rendering with Genshi templates
     * Json output rendering allows other programs to access your CLI-API


%package devel
Summary: Development Libraries and Tools for Building Applications on Cement
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: python-tempita, python-paste

%description devel
This package provides development libraries and tools for building applications
on the Cement CLI Application Framework for Python.  Cement provides plugins
for the paster utility allowing developers to easily quickstart a new project.
For example:

    $ paster cement-app helloworld
    
%package doc
Summary: Documentation for Cement
Group: Documentation
BuildRequires: python-configobj, python-genshi, python-jinja2, python-sphinx
BuildRequires: python-jsonpickle

%description doc
This package provides the Sphinx documentation for the Cement CLI Application
Framework for Python.


%prep
%setup -q

%patch0 -p1 -b .noreqs
%patch1 -p1 -b .doc
%patch2 -p1 -b .tests

sed -i 's|@@@cement_basever@@@|%{basever}|' doc/source/conf.py
sed -i 's|@@@cement_version@@@|%{version}|' doc/source/conf.py

%build
%{__python} setup.py build
%{__python} setup.py nosetests --verbosity 3
sphinx-build doc/source doc/build/html 

# cleanup 
rm -rf  build/lib/tests \
        doc/build/html/.doctrees \
        doc/build/html/.buildinfo

%install
rm -rf %{buildroot}

%{__python} setup.py install -O1 \
    --skip-build \
    --root %{buildroot} \
    --single-version-externally-managed


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README LICENSE ChangeLog
%{python_sitelib}/%{name}-%{version}-py%{pyver}.egg-info/
%{python_sitelib}/cement/
%exclude %{python_sitelib}/cement/paste

%files devel
%defattr(-,root,root,-)
%{python_sitelib}/cement/paste

%files doc
%defattr(-,root,root,-)
%doc doc/build/html

%changelog
* Fri Apr 30 2010 BJ Dierkes <wdierkes@rackspace.com> - 0.8-1
- Initial spec build
