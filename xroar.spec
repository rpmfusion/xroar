Name:           xroar
Version:        0.29.5
Release:        1%{?dist}
Summary:        A Dragon 32, Dragon 64 and Tandy CoCo emulator
Group:          Applications/Emulators
License:        GPLv2+
URL:            http://www.6809.org.uk/dragon/xroar.shtml
Source0:        http://www.6809.org.uk/dragon/%{name}-%{version}.tar.gz
Source1:        http://www.6809.org.uk/dragon/dragon.rom
# Hans de Goede
Patch0:         %{name}-0.28-lm.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gtk2-devel
BuildRequires:  gtkglext-devel
BuildRequires:  SDL_image-devel
BuildRequires:  libsndfile-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  texinfo
BuildRequires:  texinfo-tex
BuildRequires:  libicns-utils
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires(post): info
Requires(preun): info


%description
A Dragon 32, Dragon 64 and Tandy CoCo emulator for Unix, Linux, GP32, MacOS X
and Windows32. It uses standard cassette images (".cas" files) and virtual
diskettes (".dsk" or ".vdk" files) but has its own snapshot format at the
moment (no ".pak" file support).

ROM images of the firmware are required for full emulation but a 3rd party
minimal firmware is included.


%prep
%setup -q
%patch0 -p1


%build
%configure
make %{?_smp_mflags} VERBOSE=1

# Build docs
make doc/xroar.txt
make doc/xroar.html
make doc/xroar.pdf

# Generate desktop file
cat >%{name}.desktop <<EOF
[Desktop Entry]
Name=XRoar
GenericName=Dragon 32/64 Emulator
Comment=Emulates the Dragon 32/64 and Tandy CoCo
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;Emulator;
EOF

cat >%{name}-minifirm.desktop <<EOF
[Desktop Entry]
Name=XRoar [Minimal Firmware]
GenericName=Dragon 32/64 Emulator
Comment=Emulates the Dragon 32/64 and Tandy CoCo
Exec=%{name} -extbas %{_datadir}/%{name}/roms/dragon-minifirm.rom
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;Emulator;
EOF


%install
rm -rf %{buildroot}
make install DEB_BUILD_OPTIONS=nostrip \
             DESTDIR=%{buildroot}

# Install ROM 
mkdir -p %{buildroot}%{_datadir}/%{name}/roms
install -pm0644 %{SOURCE1} %{buildroot}%{_datadir}/%{name}/roms/dragon-minifirm.rom

# Extract Mac OS X icons
icns2png -x macosx/%{name}.icns 

# Install icons
for i in 16 32 48 128; do
  install -d -m 755 %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
  install -m 644 %{name}_${i}x${i}x32.png \
    %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

# Install desktop files
desktop-file-install \
  --vendor dribble \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}.desktop

desktop-file-install \
  --vendor dribble \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}-minifirm.desktop


%clean
rm -rf %{buildroot}


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :

touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%preun
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/applications/dribble-%{name}-minifirm.desktop
%{_infodir}/%{name}.info*
%doc ChangeLog COPYING.GPL COPYING.LGPL-2.1 README 
%doc doc/%{name}.txt 
%doc doc/%{name}.html doc/%{name}-screens.png
%doc doc/%{name}.pdf


%changelog
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
