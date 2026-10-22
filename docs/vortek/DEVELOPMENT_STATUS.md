# VortekSlicer development status

Last verified: 2026-10-22, America/Regina.

## Current branches and source

- Active branch: `codex/vortek-product-identity`.
- Product identity commit: `f5e9d1ae4c9babd98c3a46e99b46f486c7caaf87`.
- Protocol ownership fix: `8f8e7c12a057ebee7ce381b9aa12ef3c9bdf836d`.
- Application updater guard: `393bc00b1896047906569833dcbf00433ce91962`.
- Windows CLI stream preservation: `de090f4456`.
- Upstream G-code configuration-header compatibility: `0f431e3bf3`.
- Configuration selection regression test: `ce09e1d7b9`.
- Windows artifact/check integration: `b5704f61a3`.
- Windows CI Python-fixture integration: `a9ab64cc96`.
- Windows association path-capacity/failure guard: `bf4f8ddd49`.
- Portable path directory check: `5bafb60b9f`.
- Product diagnostic/support destinations: `3472ffa022`.
- Bundled-Python project limit: `ce04347a92` (separate build correction).
- Verified offline wx source support, fixture and CI integration: `6b1fe70131`.
- Preserved validation branch: `codex/windows-build-validation` at `9714136543`.
- Earlier profile-tool correction: `dcd5382b5c`; build records: `75f87f5d1e`, `9714136543`.
- Source synchronization baseline: `04684c58f935fc5beaba4d5959dcd7741c6a22d1`.
- Pinned upstream: `8d69fa3e5a9d5424899b0f9c2aaceb4af61c2c38`.
- Their baseline trees match: `110cf80a49c2b4dc3e35fe4bfa97f5eaea193d10`.
- Local main remains `b3a0c8bd407c3de1ff1f9962eccc3dabd1e12f18`.
- Origin: `https://github.com/PrairieBoss/VortekSlicer.git`.
- Upstream: `https://github.com/OrcaSlicer/OrcaSlicer.git`.

Product work is based on the synchronized source plus the preserved validation
commits. It has not bypassed main. Use `git log -5 --oneline` for subsequent
record commits. No development PR has been opened or merged.

## Active workstreams

| Workstream | Current result | Next useful action |
| --- | --- | --- |
| Windows build | All 32 dependency targets passed; product application build started with GUI/CAD/tests enabled | Resolve application compile/test/install results |
| Branding | Product names, captions, splash version, About credit, Windows metadata implemented | Compile GUI, inspect layout, supply verified Vortek graphics |
| Configuration isolation | Separate normal/portable/viewer/credential identities; safer Windows associations implemented | Runtime co-installation and account tests against disposable data |
| Packaging | Distinct NSIS/CPack identity configured for x64/ARM64; unsafe inherited MSIX staging blocked | Build internal NSIS/portable candidate after application validation |
| QA | Fourteen focused fork tests and four welcome JavaScript tests passed; standalone console and dependency configuration checks passed | Application tests and functional slicing after dependencies finish |
| Maintenance | Architecture, backlog, build procedure and PR draft prepared | Keep records aligned with observed results and open reviewable PRs when authenticated |

The product changes are **implemented but not runtime-validated**. They do not
establish a working GUI or production-ready slicer. The current execution
strategy allows independent workstreams to proceed despite build blockers.

## Implemented product behavior

`version.inc` now identifies VortekSlicer and Vortek Manufacturing. Generated
identity constants drive application-data keys, configuration/viewer names,
Windows file ProgIDs, credential service, portable directory, and resources.
The translation domain remains `OrcaSlicer`, as do internal build targets,
launcher/DLL names, profile formats, icons, and splash graphics.
The generated homepage identifies the fork repository for diagnostic build
links, issue reports and CPack metadata; diagnostic exports use Vortek filenames.

Normal Windows configuration uses the VortekSlicer application identity.
Portable mode recognizes `VortekSlicer-data` and ignores upstream's generic
`data_dir`. No automatic Orca configuration, preset, or account migration was
added. Explicit `--datadir` remains a caller override; do not point it at an
existing OrcaSlicer installation's data.

Windows association queries handle read errors and non-string values before
comparing them. Removal checks ownership and uses the proper default view
selector. Automatic `orcaslicer://` takeover is prevented for the fork.
The credential service is `VortekSlicer/Auth`; tests access no live credentials.
URL disassociation also checks ownership before clearing a handler. File
association changes now pass executable-path capacity in characters and abort
on failed/truncated lookup. Portable discovery requires a directory: a regular
file named `VortekSlicer-data` is preserved and ignored. Both regressions were
reproduced before their fixes; the native fixtures passed afterward. The normal
application updater entry point returns before requesting upstream installer
metadata; a manual check queues an explanatory dialog. Profile update logic
is unchanged. Provider-directed forced upgrades still require review.

CPack keeps the upstream NSIS system but separates installation, uninstallation,
upgrade identity and shortcut labels. The inherited MSIX script refuses to
stage under OrcaSlicer's publisher/Store identity and preserves existing staging
on that failure. It is not yet a supported Vortek MSIX packaging route.
The existing Windows workflow now uses product-aware artifact names/installer
paths, skips upstream-only MSIX packaging for the fork, and runs the focused
native suite in its build-script check job. These workflow changes were not
executed on GitHub. Its extracted batch step passed locally using the existing
VS2026 installation (11/11, latest run 5.963 seconds, plus the Python build
fixture in 0.204 seconds); this did not change the VS2022
application build. The PowerShell variable step passed local product/architecture
fixtures for Vortek/Orca names and x64/ARM64. No toolchain was installed.

See [product architecture](../HLSD/vortek-product-identity.md) for exact mappings
and compatibility decisions. No slicing-engine logic, printer settings,
production profiles, licenses, or original attribution were removed or changed.

## Build recovery and observed environment

The configured toolchain remains VS2022 17.14.37, MSBuild 17.14.51,
MSVC 19.44.35228.0/x64, Windows SDK 10.0.26100.0, and CMake 4.3.2.
Use one MSBuild project at a time and two compiler jobs. No new major toolchain
was installed and no global network, PATH, or security setting was changed.

DNS checks in the execution subprocess failed for `github.com`,
`api.github.com`, and `www.microsoft.com`; localhost resolved. No process proxy
variables were set. This does not prove the host's normal network is broken:
the in-app browser reached GitHub and downloaded Assimp. Host VPN/proxy/DNS
configuration was not changed.

The official Assimp 5.4.3 archive was downloaded through the browser to
`C:/Users/Tech/Downloads/assimp-5.4.3.tar.gz`. Its SHA-256 exactly matched
`66dfbaee288f2bc43172440a55d0235dfc7bf885dda6435c038e8000e79582cb`
from `deps/Assimp/Assimp.cmake`, then it was copied into the existing cache.

The resumed dependency build reported completion of Assimp, Boost, Eigen,
CGAL, Cereal, Draco, and Expat. The previously built ZLIB is preserved.
The resumed log is `build-validation-logs/dependencies-recovered.log`.
No obsolete Eigen BLAS/LAPACK workaround was introduced.

The pinned FFmpeg archive was subsequently recovered with the normal browser
link click/download flow and hash-verified:

- Cache: `deps/DL_CACHE/FFMPEG/ffmpeg-n7.0.3-31-g9b6ffd74b5-win64-orca-shared-7.0.zip`.
- Source: pinned GitHub release asset in `deps/FFMPEG/FFMPEG.cmake`.
- SHA-256: `e65916020ddb9ef84b2666dfbcbfc9b1d67f69d15b4a66db53754637bf2d498c`.

Earlier direct/background and download-media attempts failed or timed out.
The normal browser control succeeded. Python 3.12.13, Qhull 8.0.2, the pinned
SolveSpaceLib snapshot, and wxInspector 1.0.0 were also recovered from their
configured sources and individually verified before cache placement.
A generated-download audit verified all 27 pinned SHA-256 archive hashes and
found no missing archive downloads. Secondary downloads during third-party
builds may still need network access; this audit does not certify those.

The next observed problem was an OpenSSL compiler stall: compiling its first
translation unit with `/Zi /FS` stalled, including with a fresh PDB path, while
the same translation unit compiled with `/Z7`. A process-local `_CL_=/Z7`
override built the libraries and tool/test executables. The generated install
rule then failed because `/Z7` embeds debug symbols instead of producing the
standalone static-library PDB it unconditionally copied. Only the ignored
OpenSSL generated Makefile was adjusted to copy `ossl_static.pdb` if it exists;
no dummy PDB was created. The targeted build/install then exited zero.
See the exact scoped workaround in [WINDOWS_BUILD.md](WINDOWS_BUILD.md).
This is an environment-specific debug-storage workaround, not a tracked source
patch or established diagnosis of the host's PDB service.

Logs: `build-validation-logs/openssl-z7.log` (initial install failure) and
`build-validation-logs/openssl-z7-install.log` (successful target). The installed
OpenSSL reports 1.1.1w; a `/MT` native probe linked both static libraries, checked
the SHA-256 of `abc`, and created/freed a TLS context (exit zero). This is not
the complete upstream OpenSSL test suite or a live TLS/network test.
Probe: `build-validation-logs/openssl-link-probe.log`.

The resumed dependency build completed OCCT, GLEW, OpenCSG, OpenCV, Blosc,
OpenEXR, TBB, OpenVDB, PNG, SLVS, libnoise and JPEG. Together with the earlier
14 targets and the subsequently completed Python, Qhull, GMP, MPFR, wxWidgets
and wxInspector targets, all 32 dependency targets have now completed successfully. GMP and MPFR are repository-supplied
Windows binary copy targets, not ExternalProject compilations. Logs:
`dependencies-resume-20261022.log`, `dependencies-after-python-20261022.log`,
`qhull-20261022.log`, `gmp-20261022.log`, and `mpfr-20261022.log`.
The first resumed command was interrupted after Python's C1902 failure; the
second stopped at wxWidgets' network clone failure. Successful targets and
partial objects remain preserved.

OpenCV's installed static `opencv_world` library compiled/linked with the same
contract the application uses. A native probe passed PNG encode/decode equality
and an image threshold/count check. Logs: `opencv-probe-configure.log`,
`opencv-probe-build.log`, and `opencv-probe-run.log` (zero exit checkpoint).
This establishes selected installed-library behavior, not application slicing.

wxWidgets' Git clone was blocked by execution DNS. The required `v3.3.2` name
is a branch, not a tag; official GitHub data resolved it to commit
`88f3483ca546fbf4ad732e1acd94cc930935077a`. The preserved checkout was its parent,
and the only changed file was recovered through the authenticated read connector.
A fresh export reconstructed the exact official root tree and verified all
7,406 parent/submodule files against Git blob hashes. No archived generated wx
libraries were copied. The optional `ORCA_WXWIDGETS_SOURCE_DIR` recipe path now
accepts a verified source export and removes download/update steps; the normal
online recipe is preserved. Three CMake tests passed in 5.423 seconds, including
executing offline download/update targets and rejecting five incomplete inputs.
Log: `wx-config-tests-20261022.log`. Provenance is in
`DEPENDENCY_CACHE_PROVENANCE.json`.

The first offline configure then required WebView2 SDK 1.0.3485.44. Its archived
NuGet package matched the exact SHA-256 pinned by wxWidgets and was freshly
extracted into the new build's expected package directory. The offline wx target
compiled and installed in 3 minutes 21 seconds (exit zero).
The full dependency command then completed wxInspector and exited zero in
28 seconds. Logs: `wx-offline-sdk-20261022.log` and
`dependencies-final-20261022.log`, with matching zero exit checkpoints.

The active command is now `build_win.bat -s --vs 2022 -j 2 --run-tests -i`,
using the normal environment plus the process-local extra configure option
`ORCA_SLICER_CMAKE_ARGS=-DSLIC3R_MSVC_PDB=OFF`. This supported option avoids
requiring compiler PDB service operation; no installed compiler setting changed.
GUI, CAD and tests remain enabled. Log:
`build-validation-logs/application-vortek-resume-20261022.log`; exit checkpoint:
`build-validation-logs/application-vortek-resume-20261022.exit`.
The first `application-vortek-20261022.log` build was intentionally interrupted
to include the corrected configuration import object. MSBuild repeated the
unfinished core compiler batch; completed dependency and auxiliary projects
were reused. Do not interrupt another unfinished batch merely for a source edit;
let it finish, then use an incremental build for already compiled changes.
The resumed command has compiled the corrected Config source; no full
application/test/install completion result exists yet. No second heavy build
runs concurrently. Configuration's optional uv 0.11.21 download failed on DNS;
upstream permits the build to continue without that optional package installer.
No unverified substitute was provided. Its absence must remain visible in the
packaging/runtime acceptance record.

Static inspection of the pinned CPython archive found additional bootstrap
downloads in `PCbuild/get_externals.bat`: bzip2, SQLite, xz, zlib, libffi and
OpenSSL binaries. They use version tags via `get_external.py` and provide no
archive SHA-256 pins there. They are not covered by the 27-archive CMake audit.
All six were recovered from the official `python/cpython-source-deps` and
`python/cpython-bin-deps` repositories at the exact commits resolved from those
tags. Every file matched the official Git blob hash, and the complete trees
reconstructed to the official Git tree hashes (1,322 files total). Archive
SHA-256 hashes were recorded after that verification in
[DEPENDENCY_CACHE_PROVENANCE.json](DEPENDENCY_CACHE_PROVENANCE.json); they are
not presented as upstream-provided archive checksums. ZIPs and extracted trees
remain under `deps/DL_CACHE/python3/externals/`.

The actual pinned `PCbuild/get_externals.bat --no-tkinter` then exited zero using
all six cached entries with no downloads. Log:
`build-validation-logs/python-externals-offline.log`. This was bootstrap validation.
The recipe now passes `-M /m:N` when a positive
`CMAKE_BUILD_PARALLEL_LEVEL=N` is explicitly set, preventing CPython's default
unbounded `/m` from overriding the outer project's limit. A CMake fixture
passed unset/empty/one/two-job cases; the reconfigured real project contains
`--no-tkinter -M /m:1`. No required SSL or ctypes module was disabled.

The normal Python build subsequently reached C1902 (program database manager
mismatch). Installed compiler/PDB file versions matched; the host service's
root cause remains unresolved. A target-scoped `_CL_=/Z7` build installed the
64-bit Python 3.12.13 runtime in 2 minutes 3 seconds with no compile errors.
The staged interpreter then passed isolated startup, ssl/ctypes imports,
zlib/bz2/lzma round trips, and an in-memory SQLite create/insert/select. Logs:
`python-z7-20261022.log` and `python-runtime-20261022.log`, both exit zero.
Python needed no generated install-rule modification. This is selected runtime
validation, not the complete Python test suite.

The ignored historical trees `build-archive-20261021/` and
`deps/build-archive-20261021/` remain intact, as does the download cache.
The application archive contains a resources junction and an older executable;
that executable is not evidence for the synchronized/product branch.

The Windows CLI console helper was also reproduced discarding redirected
stdout/stderr: a native probe exited zero but both captured streams were empty.
The helper now preserves existing CRT streams and binds only missing streams
when a console is needed. It rejects unbound GUI descriptors before calling
`_get_osfhandle`, following Microsoft's CRT API contract. A native regression
fixture passed pipe input/output with a hidden console and with no console,
file output plus NUL input, and a missing-stderr case beside preserved pipes
(2.289 seconds). Only Boost's stream clear calls are aliased in that fixture;
Windows/CRT operations are real. Logs: `console-probe-before.log` (expected
failure) and `console-tests-20261022.log` (exit zero). The existing Windows CI
step includes this fixture. The full product executable is still compiling.

A separately linked installed-wxWidgets probe confirmed that the generated
Vortek app key and the Orca app key resolve to distinct user-data directories.
It created no directories and opened no configuration files. Logs:
`wx-path-probe-configure.log`, `wx-path-probe-build.log`, and
`wx-path-probe-run.log`, zero exit checkpoint. A read-only query through the
repository's WebView2 loader found installed runtime 155.0.4283.62 (HRESULT zero);
no runtime installation was needed or attempted. Log:
`webview-runtime-20261022.log`. These are prerequisite/native API checks, not
full GUI startup or co-installation verification.

The configuration-import header guard had a distinct branding regression:
current upstream `; generated by OrcaSlicer` headers were rejected after the
application-name macro changed, although the preview producer table supported
them. The guard now explicitly accepts that upstream header alongside the fork
and legacy headers. The new recognition test failed before the correction and
passed afterward (13/13 identity tests, 8.665 seconds). Logs:
`gcode-compat-before-20261022.log` and `gcode-compat-tests-20261022.log`.
Two full Config regression cases were added to the existing native suite,
covering serialized settings with fork/upstream/legacy headers, optional line
numbers, and rejection of an unrelated producer. The entire changed test file
passed MSVC syntax checking using the generated Release target's includes and
definitions (`config-test-syntax-20261022.log`, exit zero); full native execution
remains pending. The application build must pick up the changed Config object
before runtime compatibility is claimed.

The setup wizard's welcome heading and setup sentence now receive the native
product name after translation. The two-node update preserves all 15 existing
locale dictionaries, credits, artwork, and upstream fallback. It handles native
identity arriving before or after translation; the name is JSON encoded in C++
and inserted as text in JavaScript. Four Node tests passed, including literal
markup/dollar characters, absent elements and both event orders. The production
native loaded-event method also compiled/ran with a fake webview and real JSON
library, checking payload identity and subframe exclusion. Latest focused suite:
14/14 in 15.035 seconds. Logs: `welcome-branding-20261022.log` and
`welcome-identity-tests-20261022.log`. This is **implemented but not runtime-
validated in the application**; visual layout and actual webview event delivery
remain pending. Existing Windows CI includes the welcome test and a narrow PR
path filter for its resources. The original welcome navigation helper remains
intact. No graphics were invented or replaced.

## Verification evidence

| Check | Observed result |
| --- | --- |
| Initial dependency configuration | Passed |
| ZLIB compilation/install and sample | Passed in the earlier validation milestone |
| Resumed dependencies | Assimp, Boost, Eigen, CGAL, Cereal, Draco, Expat, OpenSSL and CURL completed; full dependency build incomplete |
| OpenSSL installed-library probe | Static link, known SHA-256 and TLS-context creation passed; no live network |
| Existing profile tree | Earlier check: 66 vendors, no errors or warnings; profiles unchanged |
| Existing profile-tool suite | Earlier validation: 262 passes, one existing upstream skip |
| Combined script suite after fork changes | 274 run, 273 passed, one existing upstream local-clone skip; 146.812 seconds, exit zero with VS2022 active |
| Fork identity suite | 14/14 passed with VS2022/Windows SDK active; latest run 15.035 seconds, including upstream G-code compatibility and native welcome identity handoff |
| Welcome JavaScript | Four tests passed against all 15 shipped locale dictionaries, including translation event order, literal text and upstream fallback |
| Existing Windows CI step | Updated extracted step passed locally with VS2026: 12 identity tests (9.174 s), Python fixture (0.177 s), wx fixtures (8.513 s); four earlier package-variable fixtures passed; no GitHub run |
| Python build configuration | One test/four environment fixtures passed; actual generated command contains the one-project limit |
| Python external bootstrap | Six exact official Git trees verified; pinned bootstrap script exited zero using only cached entries |
| Bundled Python runtime | Python 3.12.13 compiled/staged with scoped `/Z7`; isolated imports, compression and SQLite checks passed |
| OpenCV installed-library probe | Native static link, PNG round trip and threshold/count passed |
| Offline wx source configuration | 3/3 CMake tests passed; real download/update targets ran without fetching or replacing supplied sources |
| Native probes | Generated identity and real wx path lookup passed; actual console helper preserved real redirected CRT streams; association helper/query used fake Win32 APIs |
| Windows resources | Actual generated `.rc` compiled with Windows SDK `rc.exe` |
| Package configuration | Actual CPack config generated for x64 and ARM64; separate identities and preserved license reference verified |
| MSIX guard | Refused before staging; existing sentinel preserved |
| Configuration startup selection | Production selection code with fake wx path provider and real temporary filesystem; normal, fork-portable, upstream-portable and explicit override cases passed |
| Windows build-script suite | Earlier 192 passes/30 optional LLVM-related failures; not rerun without a relevant change |
| Source checks | Diff whitespace and changed-file credential-pattern scans passed |
| Dependency superbuild | All 32 targets completed; final standard dependency command exited zero |
| Complete product compilation | Started; no completion result yet |
| GUI, slicing, preview, G-code, project round trip | Not runtime-validated |
| Installer and clean-machine deployment | Not built/run |

Fork logs: `build-validation-logs/product-identity-portable-20261022.log`,
`build-validation-logs/association-path-before.log`,
`build-validation-logs/portable-file-before.log`, and
`build-validation-logs/script-tests-product.log` (combined discovery). These focused
checks are separate from app compilation, live registry/credential behavior,
visual QA, and physical printer validation. No physical printer was operated.

Pinned baseline [CI run 36739271100](https://github.com/PrairieBoss/VortekSlicer/actions/runs/36739271100)
reported successful Windows build-script tests and Windows x64 application
unit tests. Its Windows portable/installer/MSIX artifacts exist, but predate
all product changes and could not be materialized for local smoke tests.
They must not be presented as validation of this branch.

## Graphics availability

The existing `Variations of Vortek logo design.png` candidate was located, but
the current authenticated file-download helper failed DNS resolution before
materialization. Its artwork has not been inspected or selected for production.
The public `.ca` website lookup also failed DNS resolution; no alternate asset
was recovered. No asset was replaced or invented. Graphics remain an independent pending task;
this does not block compilation or text/configuration work.

## GitHub and pending reviews

[PR #2](https://github.com/PrairieBoss/VortekSlicer/pull/2) was rechecked on
2026-10-22: open/draft, unmerged, mergeable at the expected sync head/base.
The earlier check returned four successful workflows; none validates product
code. Repository read access remains available. No new write was attempted
without evidence of a changed authenticated write connection. The connected integration rejected marking it ready as inaccessible
by integration. CLI authentication was rechecked and its token remains invalid;
no repeated write attempt was made without a changed authentication state.

Human action for CLI recovery: run `gh auth login --hostname github.com --web`
and complete the interactive browser authorization. Alternatively restore a
GitHub connection with the required repository write permissions. Never put
credentials in the repository.

After access is restored, recheck PR #2's exact head/base, required checks and
mergeability; merge normally, fetch origin, and fast-forward local main only.
[PR #1](https://github.com/PrairieBoss/VortekSlicer/pull/1) remains historical:
do not merge its obsolete documentation unchanged.

Then push the preserved validation and product branches and open reviewed PRs.
[PRODUCT_IDENTITY_PR.md](PRODUCT_IDENTITY_PR.md) is the complete local draft.
The profile correction and product changes remain separate commits.
Do not automatically merge the product PR or publish a release.
The exact integration/ongoing maintenance procedure is in
[UPSTREAM_SYNC.md](UPSTREAM_SYNC.md).

## Exact continuation and remaining acceptance

1. Check the `application-vortek-20261022` exit file and log. Do not launch
   another heavy build while it is running. All dependency targets have passed.
2. Apply the shell environment in [WINDOWS_BUILD.md](WINDOWS_BUILD.md), then run
   `build_win.bat -d --vs 2022 -j 2`. Preserve the successful targets and all 27
   hash-verified archives. Scope any `/Z7` workaround to the build process and
   document the exact invocation; do not modify global compiler settings.
   Keep `EXTERNALS_DIR` set to the verified six-entry Python cache on this host.
3. To resume the application build, set
   `$env:ORCA_SLICER_CMAKE_ARGS='-DSLIC3R_MSVC_PDB=OFF'`, then run
   `build_win.bat -s --vs 2022 -j 2 --run-tests -i`. Record application compilation,
   tests, translations, and installation separately. The optional uv package
   installer remains unavailable; do not conflate that with core slicing.
4. Run the isolated startup/import/slice/preview/export/project/co-installation
   checks in [RELEASE_ACCEPTANCE.md](RELEASE_ACCEPTANCE.md). Verify real config paths and preservation
   of an existing Orca installation using disposable fixtures first.
5. Runtime-test the updater guard, review provider-directed forced upgrades and
   cloud callback handling, then finish verified graphics and internal packaging.
   None is a public release.

Independent work can continue on updater safety, approved assets, profile
workflow validation, source maintenance and CI preparation. See the separately
ranked [BACKLOG.md](BACKLOG.md). Release readiness is not established: there is
no current locally built product executable, tested GUI/slicing workflow, or
validated Vortek installer. The initial definition of done remains incomplete.
