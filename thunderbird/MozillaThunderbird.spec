#
# spec file for package MozillaThunderbird
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#               2006-2019 Wolfgang Rosenauer <wr@rosenauer.org>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define mainversion 68.0
%define version_postfix b2
%define update_channel release
%define releasedate 20190522150740

%bcond_without mozilla_tb_kde4
%bcond_with    mozilla_tb_valgrind
%bcond_without mozilla_tb_optimize_for_size

Name:           MozillaThunderbird
BuildRequires:  Mesa-devel
BuildRequires:  alsa-devel
BuildRequires:  autoconf213
BuildRequires:  dbus-1-glib-devel
BuildRequires:  fdupes
%if 0%{?suse_version} <= 1320
BuildRequires:  gcc7-c++
%else
BuildRequires:  gcc-c++
%endif
BuildRequires:  cargo
#BuildRequires:  hunspell-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libcurl-devel
BuildRequires:  libidl-devel
BuildRequires:  libnotify-devel
BuildRequires:  memory-constraints
BuildRequires:  mozilla-nspr-devel >= 4.19
BuildRequires:  mozilla-nss-devel >= 3.36.6
BuildRequires:  python-devel
BuildRequires:  python2-xml
# Rust version bump for packaging changes only, Firefox can build with older rust
# Upstream Firefox ESR 60.x presumes rust-1.24
# openSUSE and SLE use improved packaging in rust >= 1.30
# Use RUSTFLAGS="--cap-lints allow" to allow building, see below
BuildRequires:  rust >= 1.34
BuildRequires:  startup-notification-devel
BuildRequires:  unzip
BuildRequires:  update-desktop-files
BuildRequires:  xorg-x11-libXt-devel
BuildRequires:  xz
BuildRequires:  yasm
BuildRequires:  zip
BuildRequires:  rust-cbindgen
BuildRequires:  nodejs10 >= 8.11
BuildRequires:  nasm
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  pkgconfig(gdk-x11-2.0)
BuildRequires:  pkgconfig(glib-2.0) >= 2.22
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gtk+-2.0) >= 2.18.0
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.4.0
BuildRequires:  pkgconfig(gtk+-unix-print-2.0)
BuildRequires:  pkgconfig(gtk+-unix-print-3.0)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(libpulse)
%if %{with mozilla_tb_valgrind}
BuildRequires:  pkgconfig(valgrind)
%endif
%if 0%{?suse_version} > 1320
BuildRequires:  llvm-clang-devel >= 3.9.0
%else
# this covers the workaround to compile on Leap 42 in OBS
BuildRequires:  clang4-devel
%endif
# libavcodec is required for H.264 support but the
# openSUSE version is currently not able to play H.264
# therefore the Packman version is required
# minimum version of libavcodec is 53
Recommends:     libavcodec-full >= 0.10.16
Version:        %{mainversion}
Release:        0
Provides:       MozillaThunderbird-devel = %version
Obsoletes:      MozillaThunderbird-devel < %version
Provides:       thunderbird = %{version}
Provides:       appdata()
Provides:       appdata(thunderbird.appdata.xml)
%if %{with mozilla_tb_kde4}
# this is needed to match this package with the kde4 helper package without the main package
# having a hard requirement on the kde4 package
%define kde_helper_version 6
Provides:       mozilla-kde4-version = %{kde_helper_version}
%endif
Summary:        The Stand-Alone Mozilla Mail Component
License:        MPL-2.0
Group:          Productivity/Networking/Email/Clients
Url:            http://www.mozilla.org/products/thunderbird/
Source:         http://ftp.mozilla.org/pub/thunderbird/releases/%{version}%{version_postfix}/source/thunderbird-%{version}%{version_postfix}.source.tar.xz
Source1:        thunderbird.desktop
Source3:        mozilla.sh.in
Source4:        l10n-%{version}%{version_postfix}.tar.xz
Source6:        suse-default-prefs.js
Source8:        thunderbird-rpmlintrc
Source9:        thunderbird.appdata.xml
Source10:       create-tar.sh
Source11:       compare-locales.tar.xz
Source12:       kde.js
Source13:       https://ftp.mozilla.org/pub/thunderbird/releases/%{version}%{version_postfix}/source/thunderbird-%{version}%{version_postfix}.source.tar.xz.asc
Source14:       http://ftp.mozilla.org/pub/thunderbird/releases/%{version}/KEY#/%{name}.keyring
# Gecko/Toolkit
Patch1:         mozilla-nongnome-proxies.patch
Patch2:         mozilla-kde.patch
Patch3:         mozilla-ntlm-full-path.patch
Patch4:         mozilla-openaes-decl.patch
Patch6:         mozilla-reduce-files-per-UnifiedBindings.patch
Patch7:         mozilla-aarch64-startup-crash.patch
Patch8:         mozilla-bmo1555530.patch
Patch15:        mozilla-bmo1005535.patch
Patch18:        mozilla-s390-bigendian.patch
Patch19:        mozilla-s390-context.patch
Patch20:        mozilla-ppc-altivec_static_inline.patch
Patch21:        mozilla-reduce-rust-debuginfo.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
PreReq:         coreutils fileutils textutils /bin/sh
Recommends:     libcanberra0
Recommends:     libpulse0
### build options
%ifarch aarch64 ppc ppc64 ppc64le s390 s390x ia64 %arm
%define crashreporter 0
%else
%define crashreporter 1
%endif
%define has_system_cairo 0
# TODO: Reactivate this!
%define localize 0
# TODO: Setting this to 0 does NOT use gcc just yet
%define clang_build 1
### build options end
%define __provides_exclude ^lib.*\\.so.*$
%define __requires_exclude ^(libmoz.*|liblgpllibs.*|libxul.*|libldap.*|libldif.*|libprldap.*)$
Requires:       mozilla-nspr >= %(rpm -q --queryformat '%%{VERSION}' mozilla-nspr)
Requires:       mozilla-nss >= %(rpm -q --queryformat '%%{VERSION}' mozilla-nss)
Conflicts:      thunderbird-esr
%define progname thunderbird
%define progdir %{_prefix}/%_lib/thunderbird
%define libgssapi libgssapi_krb5.so.2
%define desktop_file_name thunderbird

%description
Mozilla Thunderbird is a redesign of the Mozilla Mail component. It is
written using the XUL user interface language and designed to be
cross-platform. It is a stand-alone application instead of part of the
Mozilla application suite.

%if %localize

%package translations-common
Summary:        Common translations for MozillaThunderbird
Group:          System/Localization
Provides:       locale(%{name}:ar;ca;cs;da;de;el;en_GB;es_AR;es_ES;fi;fr;hu;it;ja;ko;nb_NO;nl;pl;pt_BR;pt_PT;ru;sv_SE;zh_CN;zh_TW)
PreReq:         %{name} = %{mainversion}
Obsoletes:      %{name}-translations < %{version}-%{release}

%description translations-common
This package contains several optional languages for the user interface
of MozillaThunderbird.


%package translations-other
Summary:        Extra translations for MozillaThunderbird
Group:          System/Localization
Provides:       locale(%{name}:ast;be;bg;bn_BD;br;et;eu;fy_NL;ga_IE;gd;gl;he;hr;hy_AM;id;is;lt;nn_NO;pa_IN;rm;ro;si;sk;sl;sq;sr;ta_LK;tr;uk;vi)
PreReq:         %{name} = %{mainversion}
Obsoletes:      %{name}-translations < %{version}-%{release}

%description translations-other
This package contains several optional languages for the user interface
of MozillaThunderbird.
%endif

%if %crashreporter
%package buildsymbols
Summary:        Breakpad buildsymbols for %{name}
Group:          Development/Debug

%description buildsymbols
This subpackage contains the Breakpad created and compatible debugging
symbols meant for upload to Mozilla's crash collector database.
%endif

%prep
%if %localize

# If generated incorrectly, the tarball will be ~270B in
# size, so 1MB seems like good enough limit to check.
MINSIZE=1048576
if (( $(stat -c%s "%{SOURCE4}") < MINSIZE)); then
    echo "Translations tarball %{SOURCE7} not generated properly."
    exit 1
fi
%endif
%setup -n thunderbird-%{version} -q -b 4 -b 11
# xulrunner patches
%patch1 -p1
%patch2 -p1
%if %{with mozilla_tb_kde4}
%patch3 -p1
%endif
%patch4 -p1
%ifarch %ix86
%patch6 -p1
%endif
%patch7 -p1
%patch8 -p1
%ifarch %ix86
#%patch9 -p1
#%patch10 -p1
%endif
%ifarch ppc ppc64 s390 s390x
%patch15 -p1
#%patch16 -p1
%patch18 -p1
%patch19 -p1
%endif
%patch20 -p1
%patch21 -p1

%build
# no need to add build time to binaries
modified="$(sed -n '/^----/n;s/ - .*$//;p;q' "%{_sourcedir}/%{name}.changes")"
DATE="\"$(date -d "${modified}" "+%%b %%e %%Y")\""
TIME="\"$(date -d "${modified}" "+%%R")\""
find . -regex ".*\.c\|.*\.cpp\|.*\.h" -exec sed -i "s/__DATE__/${DATE}/g;s/__TIME__/${TIME}/g" {} +
#
%if %{with mozilla_tb_kde4}
kdehelperversion=$(cat toolkit/xre/nsKDEUtils.cpp | grep '#define KMOZILLAHELPER_VERSION' | cut -d ' ' -f 3)
if test "$kdehelperversion" != %{kde_helper_version}; then
  echo fix kde helper version in the .spec file
  exit 1
fi
%endif
export SUSE_ASNEEDED=0
export MOZ_BUILD_DATE=%{releasedate}
export MOZILLA_OFFICIAL=1
export BUILD_OFFICIAL=1
%if %{update_channel} == "esr"
export MOZ_ESR=1
%endif
%if 0%{?suse_version} <= 1320
export CC=gcc-7
%endif
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%if 0%{?suse_version} > 1320
export CFLAGS="$CFLAGS -fno-delete-null-pointer-checks"
%endif
%ifarch ppc64 ppc64le
%if 0%{?clang_build} == 0
export CFLAGS="$CFLAGS -mminimal-toc"
%endif
%endif
%ifarch %arm
export CFLAGS="${CFLAGS/-g / }"
%endif
%ifarch %ix86 %arm
# Limit RAM usage during link
export LDFLAGS="${LDFLAGS} -Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif
export CXXFLAGS="$CFLAGS"
export RUSTFLAGS="--cap-lints allow"
%ifarch %{arm}
export RUSTFLAGS="-Cdebuginfo=0 --cap-lints allow"
%endif
export MOZCONFIG=$RPM_BUILD_DIR/mozconfig
# -g might be part of RPM_OPT_FLAGS, depending on the debuginfo setting in prj config
# gcc lacks a an explicit -noop, so use something similar to make sure -g
# is not forced into CFLAGS
export MOZ_DEBUG_FLAGS="-pipe"
#
# Limit RAM usage to avoid OOM
%limit_build -m 1500
cat << EOF > $MOZCONFIG
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZ_MILESTONE_RELEASE=1
%if 0%{?suse_version} > 1320
%ifarch i586
mk_add_options MOZ_MAKE_FLAGS=-j1
%else
mk_add_options MOZ_MAKE_FLAGS=%{?jobs:-j%jobs}
%endif
%endif
mk_add_options MOZ_OBJDIR=$RPM_BUILD_DIR/obj
ac_add_options --enable-application=comm/mail
ac_add_options --enable-calendar
ac_add_options --prefix=%{_prefix}
ac_add_options --libdir=%{progdir}
ac_add_options --includedir=%{_includedir}
ac_add_options --disable-tests
ac_add_options --disable-debug
ac_add_options --enable-alsa
# gcc7 (boo#104105)
%if 0%{?suse_version} > 1320
ac_add_options --enable-optimize="-g -O2"
%endif
%ifarch %ix86 %arm
%if 0%{?suse_version} > 1230
#ac_add_options --disable-optimize
%endif
%endif
%ifarch %arm
ac_add_options --disable-elf-hack
%endif
%ifarch x86_64
%if 0%{?suse_version} >= 1550
ac_add_options --disable-elf-hack
%endif
%endif
ac_add_options --enable-default-toolkit=cairo-gtk3
%if 0%{?suse_version} >= 1550
ac_add_options --disable-gconf
%endif
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
#ac_add_options --with-system-jpeg
ac_add_options --with-system-zlib

ac_add_options --with-l10n-base=$RPM_BUILD_DIR/l10n
ac_add_options --disable-updater
#ac_add_options --with-system-png # no apng support
#ac_add_options --enable-system-hunspell
ac_add_options --enable-startup-notification
ac_add_options --enable-official-branding
ac_add_options --disable-necko-wifi
ac_add_options --enable-update-channel=%{update_channel}
%if %has_system_cairo
ac_add_options --enable-system-cairo
ac_add_options --with-unsigned-addon-scopes=app
%endif
%if ! %crashreporter
ac_add_options --disable-crashreporter
%endif
%if %{with mozilla_tb_valgrind}
ac_add_options --disable-jemalloc
ac_add_options --enable-valgrind
%endif
EOF

%ifarch ppc64 s390x s390
# NOTE: Currently, system-icu is too old, so we can't build with that,
#       but have to generate the .dat-file freshly. This seems to be a
#       less fragile approach anyways.
# ac_add_options --with-system-icu
echo "Generate big endian version of config/external/icu/data/icud58l.dat"
./mach python intl/icu_sources_data.py .
ls -l config/external/icu/data
rm -f config/external/icu/data/icudt*l.dat
%endif

./mach build

%install
cd $RPM_BUILD_DIR/obj
make -C comm/mail/installer STRIP=/bin/true MOZ_PKG_FATAL_WARNINGS=0
# copy tree into RPM_BUILD_ROOT
mkdir -p %{buildroot}%{progdir}
cp -rf $RPM_BUILD_DIR/obj/dist/thunderbird/* \
       %{buildroot}%{progdir}
%if %{with mozilla_tb_kde4}
# install kde.js
install -m 644 %{SOURCE12} %{buildroot}%{progdir}/defaults/pref/kde.js
# make sure that instantApply is true by default
# (TODO: mozilla-kde.patch needs to be improved to really not load kde.js in non-KDE envs)
echo 'pref("browser.preferences.instantApply", true);' > %{buildroot}%{progdir}/defaults/pref/all-thunderbird.js
%endif
# build additional locales
%if %localize
truncate -s 0 %{_tmppath}/translations.{common,other}
sed -r '/^(ja-JP-mac|en-US|$)/d;s/ .*$//' $RPM_BUILD_DIR/thunderbird-%{version}/comm/mail/locales/shipped-locales \
    | xargs -P 8 -n 1 -I {} /bin/sh -c '
	locale=$1
   	pushd $RPM_BUILD_DIR/compare-locales
	PYTHONPATH=lib \
	  scripts/compare-locales -m ../l10n-merged/$locale \
	  ../thunderbird-%{version}/comm/mail/locales/l10n.ini ../l10n $locale
	popd
	LOCALE_MERGEDIR=$RPM_BUILD_DIR/l10n-merged/$locale \
            make -C comm/mail/locales langpack-$locale
        cp -rL dist/xpi-stage/locale-$locale \
           %{buildroot}%{progdir}/extensions/langpack-$locale@thunderbird.mozilla.org
	# remove prefs and profile defaults from langpack
	rm -rf %{buildroot}%{progdir}/extensions/langpack-$locale@thunderbird.mozilla.org/defaults
        # check against the fixed common list and sort into the right filelist
        _matched=0
        for _match in ar ca cs da de el en-GB es-AR es-CL es-ES fi fr hu it ja ko nb-NO nl pl pt-BR pt-PT ru sv-SE zh-CN zh-TW; do
          [ "$_match" = "$locale" ] && _matched=1
        done
        [ $_matched -eq 1 ] && _l10ntarget=common || _l10ntarget=other
	echo %{progdir}/extensions/langpack-$locale@thunderbird.mozilla.org \
	  >> %{_tmppath}/translations.$_l10ntarget
' -- {}
%endif
# overwrite the mozilla start-script and link it to /usr/bin
mkdir --parents %{buildroot}%{_bindir}/
sed "s:%%PREFIX:%{_prefix}:g
s:%%PROGDIR:%{progdir}:g
s:%%APPNAME:thunderbird:g
s:%%PROFILE:.thunderbird:g" \
  %{SOURCE3} > %{buildroot}%{progdir}/%{progname}.sh
chmod 755 %{buildroot}%{progdir}/%{progname}.sh
ln -sf ../..%{progdir}/%{progname}.sh %{buildroot}%{_bindir}/%{progname}
# freedesktop definition
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{SOURCE1} \
               %{buildroot}%{_datadir}/applications/%{desktop_file_name}.desktop
# appdata
mkdir -p %{buildroot}%{_datadir}/appdata
cp %{SOURCE9} %{buildroot}%{_datadir}/appdata/%{desktop_file_name}.appdata.xml
# apply SUSE defaults
sed -e 's,RPM_VERSION,%{mainversion},g
s,GSSAPI,%{libgssapi},g' \
   %{SOURCE6} > suse-default-prefs
cp suse-default-prefs %{buildroot}%{progdir}/defaults/pref/all-opensuse.js
rm suse-default-prefs
# use correct locale for useragent
cat > %{buildroot}%{progdir}/defaults/pref/all-l10n.js << EOF
pref("general.useragent.locale", "chrome://global/locale/intl.properties");
EOF
# remove spurious executable bits
find %{buildroot}%{_libdir}/%{progname}  \
    -name "*.js" -o \
    -name "*.jsm" -o \
    -name "*.rdf" -o \
    -name "*.properties" -o \
    -name "*.dtd" -o \
    -name "*.css" \
    -exec chmod a-x {} +
# remove mkdir.done files from installed base
find $RPM_BUILD_ROOT%{progdir} -type f -name ".mkdir.done" -delete -print
#
for size in 16 22 24 32 48 64 128; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/
  cp %{buildroot}%{progdir}/chrome/icons/default/default$size.png \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{progname}.png
done
%suse_update_desktop_file %{desktop_file_name} Network Email GTK
# excluded files
rm -f %{buildroot}%{progdir}/thunderbird
rm -f %{buildroot}%{progdir}/removed-files
rm -f %{buildroot}%{progdir}/precomplete
rm -f %{buildroot}%{progdir}/updater
rm -f %{buildroot}%{progdir}/updater.ini
rm -f %{buildroot}%{progdir}/update.locale
rm -f %{buildroot}%{progdir}/dictionaries/en-US*
rm -f %{buildroot}%{progdir}/nspr-config
# Some sites use different partitions for /usr/(lib|lib64) and /usr/share.  Since you
# can't create hardlinks across partitions, we'll do this more than once.
%fdupes %{buildroot}%{progdir}
%fdupes %{buildroot}%{_libdir}/mozilla
%fdupes %{buildroot}%{_datadir}
%if %crashreporter
SYMBOLS_NAME="thunderbird-%{mainversion}-%{release}.%{_arch}-%{suse_version}-symbols"
make buildsymbols \
  SYMBOL_INDEX_NAME="$SYMBOLS_NAME.txt" \
  SYMBOL_ARCHIVE_BASENAME="$SYMBOLS_NAME"
if [ -e dist/*symbols.zip ]; then
  mkdir -p %{buildroot}%{_datadir}/mozilla/
  cp dist/*symbols.zip %{buildroot}%{_datadir}/mozilla/
fi
%endif

%clean
rm -rf %{buildroot}
%if %localize
rm -rf %{_tmppath}/translations.*
%endif

%post
%icon_theme_cache_post
exit 0

%postun
%icon_theme_cache_postun
exit 0

%files
%defattr(-,root,root)
%attr(755,root,root) %{progdir}/%{progname}.sh
%dir %{progdir}
%{progdir}/application.ini
%{progdir}/blocklist.xml
%{progdir}/chrome.manifest
%{progdir}/dependentlibs.list
%{progdir}/fonts/
%dir %{progdir}/gtk2
%{progdir}/gtk2/libmozgtk.so
%{progdir}/*.so
%{progdir}/omni.ja
%if %crashreporter
%{progdir}/minidump-analyzer
%endif
%{progdir}/pingsender
%{progdir}/platform.ini
%{progdir}/plugin-container
%{progdir}/thunderbird-bin
# crashreporter files
%if %crashreporter
%{progdir}/crashreporter
%{progdir}/crashreporter.ini
%{progdir}/Throbber-small.gif
%endif
%dir %{progdir}/chrome/
%{progdir}/chrome/icons/
%{progdir}/distribution/
%{progdir}/defaults/
%{progdir}/features/
%{progdir}/isp/
%{_datadir}/appdata/
%{_datadir}/applications/%{desktop_file_name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{progname}.png
%{_bindir}/%{progname}

%if %localize
%files translations-common -f %{_tmppath}/translations.common
%defattr(-,root,root)

%files translations-other -f %{_tmppath}/translations.other
%defattr(-,root,root)
%endif

%if %crashreporter
%files buildsymbols
%defattr(-,root,root)
%{_datadir}/mozilla/
%endif

%changelog