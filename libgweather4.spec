#
# Conditional build:
%bcond_without	apidocs		# gi-docgen generated API documentation
%bcond_without	vala		# Vala API
%bcond_without	libsoup3	# libsoup3/geocode-glib2 instead of libsoup 2.x/geocode-glib

Summary:	Library to access weather information from online services for numerous locations
Summary(pl.UTF-8):	Biblioteka dostępu do informacji pogodowych z serwisów internetowych dla różnych miejsc
Name:		libgweather4
Version:	4.4.4
Release:	3
License:	GPL v2+
Group:		X11/Libraries
Source0:	https://download.gnome.org/sources/libgweather/4.4/libgweather-%{version}.tar.xz
# Source0-md5:	42c548a6d45f79c2120b0a0df8a74e68
URL:		https://wiki.gnome.org/Projects/LibGWeather
%if %{with libsoup3}
BuildRequires:	geocode-glib2-devel
%else
BuildRequires:	geocode-glib-devel
%endif
BuildRequires:	gettext-tools >= 0.18
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.6}
BuildRequires:	glib2-devel >= 1:2.68.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
%if %{with libsoup3}
BuildRequires:	libsoup3-devel >= 3.0.0
%else
BuildRequires:	libsoup-devel >= 2.44.0
%endif
BuildRequires:	libxml2-devel >= 1:2.6.30
BuildRequires:	meson >= 0.57.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	python3 >= 1:3
BuildRequires:	python3-pygobject3 >= 3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala >= 2:0.18.0}
BuildRequires:	xz
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	glib2 >= 1:2.68.0
Requires:	glib2 >= 1:2.68.0
%if %{with libsoup3}
Requires:	libsoup3 >= 3.0.0
%else
Requires:	libsoup >= 2.44.0
%endif
Requires:	libxml2 >= 1:2.6.30
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libgweather is a library to access weather information from online
services for numerous locations.

%description -l pl.UTF-8
libgweather to biblioteka pozwalająca na dostęp do informacji
pogodowych z serwisów internetowych dla różnych miejsc.

%package devel
Summary:	Header files for libgweather
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libgweather
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.68.0
%if %{with libsoup3}
Requires:	libsoup3-devel >= 3.0.0
%else
Requires:	libsoup-devel >= 2.44.0
%endif
Requires:	libxml2-devel >= 1:2.6.30

%description devel
Header files for libgweather.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libgweather.

%package static
Summary:	Static libgweather library
Summary(pl.UTF-8):	Statyczna biblioteka libgweather
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libgweather library.

%description static -l pl.UTF-8
Statyczna biblioteka libgweather.

%package apidocs
Summary:	libgweather API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libgweather
Group:		Documentation
BuildArch:	noarch

%description apidocs
libgweather API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libgweather.

%package -n vala-libgweather4
Summary:	libgweather API for Vala language
Summary(pl.UTF-8):	API biblioteki libgweather dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.18.0
BuildArch:	noarch

%description -n vala-libgweather4
libgweather API for Vala language.

%description -n vala-libgweather4 -l pl.UTF-8
API biblioteki libgweather dla języka Vala.

%prep
#%setup -q
%setup -q -n libgweather-%{version}

%build
%meson \
	-Denable_vala=%{!?with_vala:false}%{?with_vala:true} \
	-Dgtk_doc=%{__true_false apidocs} \
	%{!?with_libsoup3:-Dsoup2=true} \
	-Dzoneinfo_dir=%{_datadir}/zoneinfo

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libgweather-4.0 $RPM_BUILD_ROOT%{_gidocdir}
%endif

# just a copy of es
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/es_ES

# libgweather-4.0 and libgweather-4.0-locations domains
%find_lang libgweather-4.0 --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%glib_compile_schemas

%postun
/sbin/ldconfig
%glib_compile_schemas

%files -f libgweather-4.0.lang
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_libdir}/libgweather-4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgweather-4.so.0
%dir %{_libdir}/libgweather-4
%{_libdir}/libgweather-4/Locations.bin
%{_datadir}/glib-2.0/schemas/org.gnome.GWeather4.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.GWeather4.gschema.xml
%dir %{_datadir}/libgweather-4
%{_datadir}/libgweather-4/Locations.xml
%{_datadir}/libgweather-4/locations.dtd
%{_libdir}/girepository-1.0/GWeather-4.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgweather-4.so
%{_includedir}/libgweather-4.0
%{_pkgconfigdir}/gweather4.pc
%{_datadir}/gir-1.0/GWeather-4.0.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libgweather-4.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/libgweather-4.0
%endif

%if %{with vala}
%files -n vala-libgweather4
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gweather4.vapi
%{_datadir}/vala/vapi/gweather4.deps
%endif
