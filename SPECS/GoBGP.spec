# Go binaries don't generate debug source files
%global debug_package %{nil}

Name:           gobgp
Version:        4.3.0
Release:        1%{?dist}
Summary:        BGP implementation in Go

License:        Apache-2.0
URL:            https://github.com/osrg/gobgp
Source0:        https://github.com/osrg/gobgp/archive/refs/tags/v%{version}.tar.gz
Source1:        gobgpd.conf

BuildRequires:  golang
BuildRequires:  git
BuildRequires:  systemd-rpm-macros

Requires:       systemd
Requires(pre):  shadow-utils

%global goipath github.com/osrg/gobgp

%description
GoBGP is an open source BGP implementation designed for modern
networking environments.

%prep
%autosetup -n gobgp-%{version}
# Fix gobgpd path in service file
sed -i 's|/usr/bin/gobgpd|/usr/sbin/gobgpd|g' tools/contrib/centos/gobgpd.service

%build
go env -w GOPATH=%{_builddir}/go
mkdir -p %{_builddir}/go/src/$(dirname %{goipath})
ln -sf %{_builddir}/gobgp-%{version} %{_builddir}/go/src/%{goipath}

cd %{_builddir}/go/src/%{goipath}
go build -v -o gobgpd ./cmd/gobgpd
go build -v -o gobgp  ./cmd/gobgp

%install
install -D -m 0755 %{_builddir}/go/src/%{goipath}/gobgpd %{buildroot}%{_sbindir}/gobgpd
install -D -m 0755 %{_builddir}/go/src/%{goipath}/gobgp  %{buildroot}%{_bindir}/gobgp
install -D -m 0644 tools/contrib/centos/gobgpd.service %{buildroot}%{_unitdir}/gobgpd.service
install -D -m 0640 %{SOURCE1} %{buildroot}%{_sysconfdir}/gobgpd/gobgpd.conf

%pre
getent group gobgpd >/dev/null || groupadd -r gobgpd
getent passwd gobgpd >/dev/null || \
    useradd -r -g gobgpd -d /var/lib/gobgpd -s /sbin/nologin \
    -c "GoBGP Routing Daemon" gobgpd
exit 0

%post
%systemd_post gobgpd.service

%preun
%systemd_preun gobgpd.service

%postun
%systemd_postun_with_restart gobgpd.service

%files
%license LICENSE
%{_sbindir}/gobgpd
%{_bindir}/gobgp
%{_unitdir}/gobgpd.service
%dir %{_sysconfdir}/gobgpd
%config(noreplace) %attr(0640, root, gobgpd) %{_sysconfdir}/gobgpd/gobgpd.conf

%changelog
* Thu Mar 12 2026 Ryosuke Nakayama <ryosuke.nakayama@ryskn.com> - 4.3.0-1
- Update to 4.3.0

* Sun Jan 19 2026 Ryosuke Nakayama <ryosuke.nakayama@ryskn.com> - 4.2.0-1
- Initial package
- Add systemd service file
