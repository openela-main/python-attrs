%global modname attrs

%bcond_without tests
%bcond_without python3

Name:           python-attrs
Version:        17.4.0
Release:        10%{?dist}
Summary:        Python attributes without boilerplate

License:        MIT
URL:            http://www.attrs.org/
BuildArch:      noarch
Source0:        https://github.com/hynek/%{modname}/archive/%{version}/%{modname}-%{version}.tar.gz

# Skip tests requiring python2-hypothesis
%bcond_with py2_test_with_hypothesis

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-six
%if %{with tests}
BuildRequires:  python2-pytest
%endif
%if %{with py2_test_with_hypothesis}
BuildRequires:  python2-hypothesis
%endif

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-six
%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-hypothesis
%endif  # tests
%endif  # python3

%if 0%{?rhel}
# can't run validator tests on EL without python-zope-interface
%else
BuildRequires:  python2-zope-interface
%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-zope-interface
%endif  # python3
%endif  # rhel

%description
attrs is an MIT-licensed Python package with class decorators that
ease the chores of implementing the most common attribute-related
object protocols.

%package -n python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}

%description -n python2-%{modname}
attrs is an MIT-licensed Python package with class decorators that
ease the chores of implementing the most common attribute-related
object protocols.

%if %{with python3}
%package -n python%{python3_pkgversion}-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{modname}}

%description -n python%{python3_pkgversion}-%{modname}
attrs is an MIT-licensed Python package with class decorators that
ease the chores of implementing the most common attribute-related
object protocols.
%endif

%prep
%setup -q -n %{modname}-%{version}

%if 0%{?rhel}
# can't run validator tests on EL without python-zope-interface
rm tests/test_validators.py
%endif

%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
# Doesn't install anything to /usr/bin, so I don't think the order of
# installing python2 and python3 actually matters.
%if %{with python3}
%py3_install
%endif
%py2_install

%check
%if %{with tests}
PYTHONPATH=%{buildroot}/%{python2_sitelib} py.test-2.7 -v \
%if ! %{with py2_test_with_hypothesis}
    --ignore tests/test_dark_magic.py \
    --ignore tests/test_dunders.py \
    --ignore tests/test_funcs.py \
    --ignore tests/test_make.py \
    --ignore tests/test_validators.py \
%endif

%if %{with python3}
PYTHONPATH=%{buildroot}/%{python3_sitelib} py.test-3 -v
%endif  # python3
%endif  # tests

%files -n python2-%{modname}
%license LICENSE
%doc AUTHORS.rst README.rst
%{python2_sitelib}/*

%if %{with python3}
%files -n python%{python3_pkgversion}-%{modname}
%license LICENSE
%doc AUTHORS.rst README.rst
%{python3_sitelib}/*
%endif

%changelog
* Thu Apr 25 2019 Tomas Orsava <torsava@redhat.com> - 17.4.0-10
- Bumping due to problems with modular RPM upgrade path
- Resolves: rhbz#1695587

* Mon Sep 17 2018 Lumír Balhar <lbalhar@redhat.com> - 17.4.0-9
- Get rid of unversioned Python dependencies
- Resolves: rhbz#1628242

* Tue Jul 31 2018 Lumír Balhar <lbalhar@redhat.com> - 17.4.0-8
- Make possible to disable python3 subpackage

* Fri Jul 13 2018 Lumír Balhar <lbalhar@redhat.com> - 17.4.0-7
- Replace tests conditions and make possible to disable them

* Fri Jul 13 2018 Lumír Balhar <lbalhar@redhat.com> - 17.4.0-6
- First version for python27 module

* Mon Jun 25 2018 Petr Viktorin <pviktori@redhat.com> - 17.4.0-5
- Allow Python 2 for build
  see https://hurl.corp.redhat.com/rhel8-py2

* Fri Jun 22 2018 Petr Viktorin <pviktori@redhat.com> - 17.4.0-4
- Remove the python2-hypothesis circular build dependency

* Thu Jun 14 2018 Petr Viktorin <pviktori@redhat.com> - 17.4.0-3
- Remove the python-zope-interface build dependency

* Wed Jan 17 2018 Eric Smith <brouhaha@fedoraproject.org> 17.4.0-2
- Added BuildRequires for python<n>-six.

* Thu Jan 11 2018 Eric Smith <brouhaha@fedoraproject.org> 17.4.0-1
- Updated to latest upstream.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 14 2016 Eric Smith <brouhaha@fedoraproject.org> 16.3.0-1
- Updated to latest upstream.

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 16.1.0-3
- Enable tests

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 16.1.0-2
- Rebuild for Python 3.6
- Disable python3 tests for now

* Sat Sep 10 2016 Eric Smith <brouhaha@fedoraproject.org> 16.1.0-1
- Updated to latest upstream.
- Removed patch, no longer necessary.
- Removed "with python3" conditionals.

* Thu Aug 18 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-6
- Build for Python 3.4 in EPEL7.

* Thu Aug 18 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-5
- Updated based on Fedora package review (#1366878).
- Fix check section, though tests can not be run for EPEL7.
- Add patch to skip two tests with keyword collisions.

* Tue Aug 16 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-4
- Fix python2 BuildRequires.

* Mon Aug 15 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-3
- Updated based on Fedora package review (#1366878).

* Sun Aug 14 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-2
- Updated based on Fedora package review (#1366878).

* Sat Aug 13 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-1
- Initial version.
