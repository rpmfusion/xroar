Name:           xroar
Version:        0.34.8
Release:        3%{?dist}
Summary:        A Dragon 32, Dragon 64 and Tandy CoCo emulator
License:        GPLv2+
URL:            http://www.6809.org.uk/xroar/
Source0:        http://www.6809.org.uk/xroar/download/%{name}-%{version}.tar.gz
Source1:        http://www.6809.org.uk/dragon/dragon.rom
Source2:        %{name}.desktop
Source3:        %{name}-minifirm.desktop
Source4:        %{name}.appdata.xml
BuildRequires:  gcc
BuildRequires:  gtk2-devel
BuildRequires:  gtkglext-devel
BuildRequires:  SDL2-devel
BuildRequires:  libsndfile-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  zlib-devel
BuildRequires:  texinfo
BuildRequires:  texinfo-tex
BuildRequires:  libicns-utils
BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme


%description
XRoar is a Dragon 32, Dragon 64 and Tandy CoCo emulator. It uses standard
cassette images (".cas" files) and virtual diskettes (".dsk" or ".vdk" files)
but has its own snapshot format at the moment (no ".pak" file support).

ROM images of the firmware are required for full emulation but a 3rd party
minimal firmware is included.


%prep
%setup -q


%build
%configure --without-oss
%make_build

# Build docs
make html
make pdf


%install
%make_install DEB_BUILD_OPTIONS=nostrip

# Install ROM 
install -d -m 755 %{buildroot}%{_datadir}/%{name}/roms
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/%{name}/roms/dragon-minifirm.rom

# Extract Mac OS X icons
icns2png -x src/macosx/%{name}.icns 

# Install icons
for i in 16 32 48 128; do
  install -d -m 755 %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
  install -m 644 %{name}_${i}x${i}x32.png \
    %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

# Install desktop files
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE2}

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE3}

# Install AppData file
install -d -m 755 %{buildroot}%{_datadir}/metainfo
install -p -m 644 %{SOURCE4} %{buildroot}%{_datadir}/metainfo
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.appdata.xml

rm -f %{buildroot}%{_infodir}/dir


%files
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-minifirm.desktop
%{_datadir}/metainfo/%{name}.appdata.xml
%{_infodir}/%{name}*
%{_mandir}/man1/%{name}.1*
%license COPYING.GPL COPYING.LGPL-2.1
%doc ChangeLog README
%doc doc/%{name}.html doc/%{name}-screens.png doc/%{name}-timebandit-af.png
%doc doc/%{name}.pdf


%changelog
* Tue Jun 26 2018 Andrea Musuruane <musuruan@gmail.com> - 0.34.8-3
- Added gcc dependency
- Dropped obsolete scriptlets
- Added AppData file

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.34.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Aug 25 2017 Andrea Musuruane <musuruan@gmail.com> - 0.34.8-1
- Upgrade to 0.34.8

* Tue Mar 21 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.34.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 03 2017 Andrea Musuruane <musuruan@gmail.com> - 0.34.7-1
- Upgrade to 0.34.7

* Sun Dec 18 2016 Andrea Musuruane <musuruan@gmail.com> - 0.34.6-1
- Upgrade to 0.34.6

* Sat Oct 08 2016 Andrea Musuruane <musuruan@gmail.com> - 0.34.5-1
- Upgrade to 0.34.5

* Sat Aug 27 2016 Andrea Musuruane <musuruan@gmail.com> 0.34.3-1
- Upgrade to 0.34.3

* Sat Aug 13 2016 Andrea Musuruane <musuruan@gmail.com> 0.34.1-1
- Upgrade to 0.34.1

* Mon Aug 08 2016 Andrea Musuruane <musuruan@gmail.com> 0.34-1
- Upgrade to 0.34

* Sun May 24 2015 Andrea Musuruane <musuruan@gmail.com> 0.33.1-1
- Upgrade to 0.33.1

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 0.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Apr 25 2014 Andrea Musuruane <musuruan@gmail.com> 0.32-1
- Upgrade to 0.32

* Fri Dec 06 2013 Andrea Musuruane <musuruan@gmail.com> 0.31.1-1
- Upgrade to 0.31.1
- Updated Source0 and URL

* Sun Dec 01 2013 Andrea Musuruane <musuruan@gmail.com> 0.31-2
- Removed workaround to link against libm

* Sun Dec 01 2013 Andrea Musuruane <musuruan@gmail.com> 0.31-1
- Upgrade to 0.31
- Dropped cleaning at the beginning of %%install

* Tue Oct 01 2013 Andrea Musuruane <musuruan@gmail.com> 0.30.3-1
- Upgrade to 0.30.3

* Mon Aug 12 2013 Andrea Musuruane <musuruan@gmail.com> 0.29.5-2
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Dropped desktop vendor tag

* Sun Apr 28 2013 Andrea Musuruane <musuruan@gmail.com> 0.29.5-1
- Upgrade to 0.29.5

* Sun Feb 24 2013 Andrea Musuruane <musuruan@gmail.com> 0.29.4-1
- Upgrade to 0.29.4

* Fri Feb 15 2013 Andrea Musuruane <musuruan@gmail.com> 0.29.2-1
- Upgrade to 0.29.2

* Tue Jan 29 2013 Andrea Musuruane <musuruan@gmail.com> 0.29.1-2
- Rebuilt for new texinfo (BZ #868011)

* Fri Jan 04 2013 Andrea Musuruane <musuruan@gmail.com> 0.29.1-1
- Upgrade to 0.29.1
- Disabled PDF generation

* Wed Jun 13 2012 Andrea Musuruane <musuruan@gmail.com> 0.28.1-1
- Upgrade to 0.28.1

* Sun May 13 2012 Andrea Musuruane <musuruan@gmail.com> 0.28-1
- Upgrade to 0.28
- Use converted macosx icons

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Andrea Musuruane <musuruan@gmail.com> 0.27-2
- Fix FTBFS for F16+ with a patch by Hans de Goede

* Sat Oct 01 2011 Andrea Musuruane <musuruan@gmail.com> 0.27-1
- Upgrade to 0.27

* Tue Aug 02 2011 Andrea Musuruane <musuruan@gmail.com> 0.26-1
- Upgrade to 0.26

* Sat Jun 25 2011 Andrea Musuruane <musuruan@gmail.com> 0.25.3-1
- Upgrade to 0.25.3
- Dropped JACK dependency now that pulseaudio is supported

* Fri Oct 15 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.24-2
- Rebuilt for gcc bug

* Sun Sep 12 2010 Andrea Musuruane <musuruan@gmail.com> 0.24-1
- Upgrade to 0.24
- Cosmetic changes

* Sat Dec 05 2009 Andrea Musuruane <musuruan@gmail.com> 0.23b-1
- Upgrade to 0.23b
- Used an upstream patch to fix SDL sound
- Updated icon cache scriptlets
- Packaged more docs

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.21-3
- rebuild for new F11 features

* Wed Jul 30 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.21-2
- rebuild for buildsys cflags issue

* Sat May 10 2008 Andrea Musuruane <musuruan@gmail.com> 0.21-1
- Upgrade to 0.21

* Wed Mar 05 2008 Ian Chapman <packages[AT]amiga-hardware.com> 0.20-1
- Upgrade to 0.20
- Add minimal firmware rom
- Updated license to the new guidelines

* Fri Jun 29 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.19-1
- Upgrade to 0.19
- Minor changes to spec due to new guidelines

* Sat Mar 10 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.18-1
- Upgraded to 0.18
- Significant changes to SPEC as xroar now uses configure
- Convert the icon for the gp32 as a desktop icon
  (instead of using our own)
- Dropped dribble-menus requirement, due to be obsoleted
- Changed .desktop category to Game;Emulator;

* Sun Aug 20 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.17-1
- Upgraded to 0.17

* Sat Aug 12 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.16-1
- Upgraded to 0.16
- Added libsndfile-devel buildrequire for new version

* Mon Jul 17 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.15-2
- Moved icon installation to make it freedesktop compliant
- Added %%post and %%postun sections to update icon cache at installation

* Tue Jul 04 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.15-1
- Upgraded to 0.15
- Moved .desktop generation to %%build section

* Sat Jun 24 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.14-2
- Cosmetic fixes for the Dribble repository

* Mon Jun 05 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.14-1
- Initial Release
