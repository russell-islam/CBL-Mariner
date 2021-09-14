Summary:        QEMU is a machine emulator and virtualizer
Name:           qemu-kvm
Version:        5.2.0
Release:        1%{?dist}
License:        GPLv2 AND GPLv2+ AND CC-BY AND BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://www.qemu.org/
Source0:        https://download.qemu.org/qemu-%{version}.tar.xz
Source1:        65-kvm.rules
Patch0:         CVE-2021-20181.patch
Patch1:         CVE-2021-20203.patch
Patch2:         CVE-2021-20255.patch
Patch3:         CVE-2021-3392.patch
Patch4:         CVE-2021-3416.patch
BuildRequires:  alsa-lib-devel
BuildRequires:  glib-devel
BuildRequires:  ninja-build
BuildRequires:  pixman-devel
BuildRequires:  python3-devel
BuildRequires:  python3-xml
BuildRequires:  zlib-devel
Requires:       alsa-lib
Requires:       cyrus-sasl
Requires:       pixman

%description
QEMU is a generic and open source machine & userspace emulator and virtualizer.

%global debug_package %{nil}

%package -n qemu-img
Summary:        QEMU command line tool for manipulating disk images
Group:          Development/Tools
Requires:       glib
Requires:       libstdc++
Requires:       pixman

%description -n qemu-img
This package provides a command line tool for manipulating disk images.

%prep
%setup -q -n qemu-%{version}
%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# Remove invalid flag exposed by binutils 2.36.1
sed -i "/LDFLAGS_NOPIE/d" configure

%build

%ifarch aarch64
   QEMU_ARCH=aarch64-softmmu
%else
   QEMU_ARCH=x86_64-softmmu
%endif

./configure \
 --prefix="%{_prefix}" \
 --libdir="%{_libdir}" \
 --audio-drv-list=alsa \
 --disable-libxml2     \
 --enable-tcg          \
%ifarch aarch64
 --extra-cflags="%{optflags} -fPIC" \
%endif
 --target-list=$QEMU_ARCH &&
unset QEMU_ARCH &&
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_libdir}/udev
install -d %{buildroot}%{_libdir}/udev/rules.d
install -D -m0644 %{SOURCE1} %{buildroot}%{_libdir}/udev/rules.d

chgrp kvm  %{buildroot}%{_libexecdir}/qemu-bridge-helper &&
chmod 4750 %{buildroot}%{_libexecdir}/qemu-bridge-helper

ln -sv qemu-system-`uname -m` %{buildroot}%{_bindir}/qemu
chmod 755 %{buildroot}%{_bindir}/qemu

%check
testsPassed=true
make check-unit
if [ $? -ne 0 ]; then
    testsPassed=false
fi
make check-qtest
if [ $? -ne 0 ]; then
    testsPassed=false
fi
make check-speed
if [ $? -ne 0 ]; then
    testsPassed=false
fi
make check-qapi-schema
if [ $? -ne 0 ]; then
    testsPassed=false
fi
make check-block
if [ $? -ne 0 ]; then
    testsPassed=false
fi
make check-tcg
if [ $? -ne 0 ]; then
    testsPassed=false
fi
make check-softfloat
if [ $? -ne 0 ]; then
    testsPassed=false
fi
make check-acceptance
if [ $? -ne 0 ]; then
    testsPassed=false
fi
if [ "$testsPassed" = false ] ; then
    echo 'One (or more) tests failed. Check log for further details'
    (exit 1)
fi

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/qemu-system-*
%{_bindir}/elf2dmp
%{_bindir}/qemu-edid
%{_bindir}/qemu-ga
%{_bindir}/qemu-pr-helper
%{_bindir}/qemu
%{_libdir}/*
%{_libexecdir}/*
%{_datadir}/*
%{_bindir}/qemu-storage-daemon

%files -n qemu-img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd

%changelog
* Mon Aug 23 2021 Muminul Islam <muislam@microsoft.com> - 5.2.0-1
- Updated to 5.2.0 version

* Mon Aug 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.2.0-35
- Patched CVE-2021-3682.

* Tue Jul 06 2021 Henry Li <lihl@microsoft.com> - 4.2.0-34
- Patch CVE-2021-3546

* Tue Jun 22 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.2.0-33
- Mark CVE-2020-27661 as nopatch

* Thu Jun 17 2021 Nicolas Ontiveros <niontive@microsoft.com> - 4.2.0-32
- Patch CVE-2021-20221
- Patch CVE-2021-3527

* Mon Jun 07 2021 Henry Beberman <henry.beberman@microsoft.com> - 4.2.0-31
- Patch CVE-2021-20181

* Tue May 11 2021 Andrew Phelps <anphel@microsoft.com> - 4.2.0-30
- Remove LDFLAGS_NOPIE to compile with binutils 2.36.1

* Wed Apr 07 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 4.2.0-29
- Patch CVE-2021-3392 and CVE-2021-3409.

* Tue Mar 30 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 4.2.0-28
- Patch CVE-2021-3416. Added test modules under check section.

* Tue Mar 23 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 4.2.0-27
- Patch CVE-2021-20255

* Fri Mar 19 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 4.2.0-26
- Patch CVE-2021-20203

* Mon Feb 08 2021 Rachel Menge <rachelmenge@microsoft.com> - 4.2.0-25
- Update CVE-2020-17380

* Wed Jan 13 2021 Henry Li <niontive@microsoft.com> - 4.2.0-24
- Update CVE-2020-15469

* Fri Dec 11 2020 Nicolas Ontiveros <niontive@microsoft.com> - 4.2.0-23
- Patch CVE-2020-27821

* Tue Dec 08 2020 Nicolas Ontiveros <niontive@microsoft.com> - 4.2.0-22
- Patch CVE-2020-25723

* Tue Nov 17 2020 Daniel McIlvaney <damcilva@microsoft.com> - 4.2.0-21
- Backport fix for CVE-2018-12617 from 5.0.0

* Mon Nov 16 2020 Daniel McIlvaney <damcilva@microsoft.com> - 4.2.0-20
- Noatch CVE-2020-12829, only affects SuperH and PowerPC emulation

* Wed Nov 11 2020 Henry Li <lihl@microsoft.com> - 4.2.0-19
- Patch CVE-2020-13361
- Patch CVE-2020-11869
- Patch CVE-2020-14415
- Patch CVE-2020-15859
- Patch CVE-2020-13362
- Patch CVE-2020-25742
- Patch CVE-2020-25743
- Patch CVE-2020-15469
- Patch CVE-2020-24352

* Fri Oct 30 2020 Thomas Crain <thcrain@microsoft.com> - 4.2.0-18
- Patch CVE-2018-19665
- Remove nopatch files for CVE-2016-7161, CVE-2015-7504, CVE-2017-5931,
  CVE-2017-14167, as NIST data for those has been corrected

* Thu Oct 29 2020 Ruying Chen <v-ruyche@microsoft.com> - 4.2.0-17
- Patch CVE-2020-13791.

* Thu Oct 29 2020 Joe Schmitt <joschmit@microsoft.com> - 4.2.0-16
- Patch CVE-2020-13800.
- Patch CVE-2020-14364.

* Wed Oct 28 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.2.0-15
- Add patch for CVE-2020-13253.
- Add patch for CVE-2020-13754.
- Adding back regular %%setup as %%autosetup fails on the *.nopatch files.

* Tue Oct 27 2020 Henry Li <lihl@microsoft.com> - 4.2.0-14
- Add patch for CVE-2020-10702
- Add patch for CVE-2020-10761
- Use autosetup

* Tue Sep 29 2020 Daniel McIlvaney <damcilva@microsoft.com> - 4.2.0-13
- Nopatch CVE-2015-7504, it was fixed in 2.5.0
- Nopatch CVE-2017-5931, it was fixed in 2.9.0
- Nopatch CVE-2017-14167, it was fixed in 2.11.0

* Mon Sep 28 2020 Daniel McIlvaney <damcilva@microsoft.com> - 4.2.0-12
- Nopatch CVE-2016-7161, it was fixed in 2.7

* Mon Sep 14 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 4.2.0-11
- Add patch for CVE-2020-15863

* Wed Sep 02 2020 Nicolas Ontiveros <niontive@microsoft.com> - 4.2.0-10
- Add patch for CVE-2020-16092

* Tue Jun 09 2020 Paul Monson <paulmon@microsoft.com> - 4.2.0-9
- Add patch for CVE-2019-20175
- Add patch for CVE-2020-13659

* Thu May 21 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.2.0-8
- Fix CVE-2020-1711 and CVE-2020-7211.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.2.0-7
- Added %%license line automatically

* Fri May  1 2020 Emre Girgin <mrgirgin@microsoft.com> - 4.2.0-6
- Renaming qemu to qemu-kvm

* Tue Apr 21 2020 Emre Girgin <mrgirgin@microsoft.com> - 4.2.0-5
- Fix CVE-2020-11102.
- Ignore CVE-2020-7039.
- Update license and URL.
- License verified.

* Mon Mar 30 2020 Chris Co <chrco@microsoft.com> - 4.2.0-4
- Fix changelog to not define a sha1 macro

* Fri Mar 27 2020 Chris Co <chrco@microsoft.com> - 4.2.0-3
- Add elf2dmp and virtfs-proxy-helper binaries to package
- Delete unused sha1

* Tue Mar 24 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.2.0-2
- Add Qemu KVM support

* Wed Jan 8 2020 Paul Monson <paulmon@microsoft.com> - 4.2.0-1
- Original version for CBL-Mariner.
