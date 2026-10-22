# VortekSlicer product identity

VortekSlicer retains OrcaSlicer's slicing implementation, source targets,
launcher/DLL contract, profile formats, resource layout, and translation
catalogs. Product-facing names and persistent identities are separate from
those internal compatibility names. This keeps the fork's integration surface
small enough to review against upstream changes.

## Identity source

`version.inc` supplies the product name, application-data key, vendor, homepage and
translation domain. CMake generates `libslic3r_version.h`; GUI code, native
resources, configuration filenames, and credential storage consume it.

| Surface | Vortek identity |
| --- | --- |
| Display name and full application name | `VortekSlicer` |
| Application-data key | `VortekSlicer` |
| Vendor | `Vortek Manufacturing` |
| Product repository/support destination | `https://github.com/PrairieBoss/VortekSlicer` |
| G-code viewer identity | `VortekSlicerGcodeViewer` |
| Portable data directory | `VortekSlicer-data` |
| Windows model-file ProgID | `VortekSlicer.Project.1` |
| Credential-store service | `VortekSlicer/Auth` |
| Translation domain | `OrcaSlicer` |
| Internal launcher and DLL | `orca-slicer.exe`, `OrcaSlicer.dll` |

The native main-window caption, project captions, splash version text, About
version text, Windows product metadata, and manifest use the fork identity.
The About dialog adds an explicit derivative-work credit and retains upstream
credits and copyright text. Existing icons and splash graphics remain upstream
assets; no unverified Vortek logo is substituted.
Troubleshooting build/issue links and package metadata use the product
homepage. Exported log/debug archive names use the application key. Upstream
documentation, component links and attribution retain their original targets.

The existing G-code producer table recognizes both `SLIC3R_APP_NAME` and
upstream OrcaSlicer/BambuStudio headers. Rebranding does not change that table,
the slicing algorithms, printer settings, or project format.

## Local configuration and credentials

`GUI_App::init_app_config()` sets the wx application name from the fork key.
On a normal Windows launch, wx therefore selects the VortekSlicer application
data directory instead of OrcaSlicer's. Presets, caches, logs, and other paths
derived from `Slic3r::data_dir()` follow that choice. AppConfig generates
`VortekSlicer.conf` for JSON configuration or `VortekSlicer.ini` for the legacy
configuration mode. The viewer's key is separate as well.

Portable mode recognizes `VortekSlicer-data` beside the executable. The
upstream generic `data_dir` folder is deliberately ignored, including when a
user puts a fork executable beside an existing OrcaSlicer portable install.
An explicit `--datadir` still takes precedence. That is a caller-controlled
override, not a migration mechanism: it must never point at production
OrcaSlicer data during testing.

The cloud agent uses a separate OS credential-store service. Its existing
account identifier, encryption, token-file format, backend, and HTTP protocol
remain unchanged. Fallback credential files live below the selected config
directory. No test reads real credentials or migrates an existing account.

There is no automatic OrcaSlicer profile/configuration/account import. A future
migration must copy selected data into a new fork directory, preserve the
source, and explicitly address credentials and file associations.

## Windows shell integration

File-association checks, registration, and removal use the fork's ProgID.
Association removal first verifies that the current value is a string owned
by this application. A foreign owner, missing key, read failure, or failed
delete produces no successful-removal result. The query path likewise checks
the read result and value type before comparing the value.

`RegDeleteKeyExW` uses the process's default view selector instead of passing
an unrelated full-access mask. Microsoft documents the parameter as a
[registry-view selector](https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regdeletekeyexw).
The focused tests substitute Win32 calls and exercise these cases without
changing HKCU or HKLM.

Automatic `orcaslicer://` registration is retained only when the application
key is actually `OrcaSlicer`. VortekSlicer does not take over an installed
OrcaSlicer's login or download links at startup or after closing Preferences.
The existing explicit protocol-association controls remain available. Browser
cloud login and model-download link behavior require separate runtime
acceptance and a supported callback decision before distribution.
Protocol removal also checks that the currently registered command belongs
to this executable before clearing it; a foreign or packaged handler is kept.

The normal application-update entry point returns before requesting upstream
OrcaSlicer installer metadata. Manual checks queue an explanatory message on
the GUI event loop; automatic checks do not show a dialog. Printer/profile
updates are not disabled. Provider-directed forced upgrades remain a separate
integration concern rather than a verified fork update channel.

Instance checking retains upstream's executable-path hash. Distinct install
paths and separate lock/cache directories distinguish the products without
changing the IPC protocol.

## Packaging boundaries

`cmake/VortekPackaging.cmake` overrides product-facing CPack values immediately
before `include(CPack)`. The existing NSIS generator, resource files,
executable contract, license installation, and build system are reused.
The install directory, uninstall registry identity, shortcut label, package
name, and WiX upgrade GUID differ from upstream. The upgrade GUID is stable
for the fork and shared by its architecture variants.

The build-tree install directory still uses upstream's `build/OrcaSlicer`
name; that is an internal staging path, not the system installation identity.
The packaged shortcut label is VortekSlicer while its target remains
`orca-slicer.exe`.

The inherited MSIX manifest claims upstream's publisher, protocols, execution
alias, migration ProgID, and AppData virtualization exclusion. The MSIX script
therefore rejects fork builds before checking an executable or modifying a
staging directory. Enabling MSIX requires a reviewed fork manifest, verified
publisher, assets, and safe staging behavior. NSIS configuration does not imply
an installer has been built or tested.

The existing Windows workflow derives artifact labels and installer upload
paths from `version.inc`. Internal install staging remains `OrcaSlicer`.
MSIX build/upload steps run only for the upstream repository/product identity;
fork builds can produce NSIS/portable artifacts without invoking that route.
The Windows build-script check job also runs the focused native identity suite,
and its path filters include the fork package module and identity test file.

## Verification boundary

`scripts/tests/test_product_identity.py` configures the actual header, native
resource, and manifest templates. With MSVC/Windows SDK on PATH it compiles
identity constants and registry probes and compiles the Windows resource.
It also generates CPack configuration for x64 and ARM64 and checks MSIX's
early refusal preserves an existing staging sentinel.
The startup selection and config-file functions are compiled against a fake
wx path provider and real temporary filesystem fixtures to verify directory
choice, explicit overrides and preservation of upstream portable data.

These checks validate configuration, isolated native behavior, and resource
compilation. They do not compile the wx GUI, validate real registry behavior,
prove visual layout, run account login, or establish functional slicing.
