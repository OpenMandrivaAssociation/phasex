%define     desktop_vendor  sysex
%define     name            phasex
%define     version         0.12.0
%define     beta_version    pre1

%define     release         0.%{beta_version}.3


Name:       %{name}
Version:    %{version}
Release:    %{release}
Summary:    Phase Harmonic Advanced Synthesis EXperiment
Group:      Sound
License:    GPLv2
URL:        http://sysex.net/phasex/

Source0:    %{name}-%{version}-%{beta_version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot 

BuildRequires:  libalsa-devel
BuildRequires:  jackit-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  gtk2-devel
BuildRequires:  perl


%description
Experimental JACK audio / ALSA MIDI softsynth for Linux
with a synth engine built around flexible phase modulation and
flexible oscillator/LFO sourcing.  Modulations include AM, FM, offset
PM, and wave select. It comes equipped with a 12db/octave filter
with two distortion curves, a stereo crossover delay and chorus with
phaser, ADSR envelopes for amplifier and filter, realtime audio input
processing capabilities, velocity/aftertouch sensitivity, and more.


%prep
%setup -q


%build
perl -pi -e 's/AM_LDFLAGS  =/AM_LDFLAGS  = -lgmodule-2.0 -lX11 /g' src/Makefile.am
echo _arch=%{_arch} _target_cpu=%{_target_cpu} _build_arch=%{_build_arch}
aclocal && autoconf && automake && autoheader
%configure %{?build_32bit:--enable-32bit} --enable-arch=%{_target_cpu} CFLAGS=''
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

for s in 16 22 32 48 ; do
    %{__mkdir} -p %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps
    %{__cp} %{buildroot}%{_datadir}/phasex/pixmaps/phasex-icon-${s}x${s}.png \
        %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/phasex-icon.png
done

BASE="Application AudioVideo Audio"
XTRA="X-MandrivaLinux-Multimedia-Sound;"

%{__mkdir} -p %{buildroot}%{_datadir}/applications
desktop-file-install --vendor %{desktop_vendor} \
    --dir %{buildroot}%{_datadir}/applications \
    `for c in ${BASE} ${XTRA} ; do echo "--add-category $c " ; done` \
    $RPM_BUILD_ROOT%{_datadir}/phasex/%{name}.desktop
rm $RPM_BUILD_ROOT%{_datadir}/phasex/%{name}.desktop


%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README INSTALL LICENSE AUTHORS GPL-v2.txt ChangeLog TODO doc/ROADMAP
%{_bindir}/phasex
%dir %{_datadir}/phasex
%dir %{_datadir}/phasex/help
%dir %{_datadir}/phasex/pixmaps
%dir %{_datadir}/phasex/sys-midimaps
%dir %{_datadir}/phasex/sys-patches
%dir %{_datadir}/phasex/sys-samples
%dir %{_datadir}/themes/Phasex-Dark
%dir %{_datadir}/themes/Phasex-Light
%{_datadir}/phasex/patchbank
%{_datadir}/phasex/gtkenginerc
%{_datadir}/phasex/help/*
%{_datadir}/phasex/pixmaps/*
%{_datadir}/phasex/sys-midimaps/*
%{_datadir}/phasex/sys-patches/*
%{_datadir}/phasex/sys-samples/*
%{_datadir}/themes/Phasex-Dark/*
%{_datadir}/themes/Phasex-Light/*
%{_datadir}/applications/%{desktop_vendor}-phasex.desktop
%{_datadir}/icons/hicolor/*/apps/phasex-icon.png

