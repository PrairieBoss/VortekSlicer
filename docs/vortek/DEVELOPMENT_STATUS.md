# VortekSlicer development status

Last verified: 2026-10-21, America/Regina.

## Current branches and source

- Active branch: `codex/vortek-product-identity`.
- Product identity commit: `f5e9d1ae4c9babd98c3a46e99b46f486c7caaf87`.
- Protocol ownership fix: `8f8e7c12a057ebee7ce381b9aa12ef3c9bdf836d`.
- Application updater guard: `393bc00b1896047906569833dcbf00433ce91962`.
- Configuration selection regression test: `ce09e1d7b9`.
- Windows artifact/check integration: `b5704f61a3`.
- Product diagnostic/support destinations: `3472ffa022`.
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
| Windows build | All 27 generated archive downloads hash-verified; OpenSSL and CURL built/installed; OCCT compiling | Finish remaining dependencies |
| Branding | Product names, captions, splash version, About credit, Windows metadata implemented | Compile GUI, inspect layout, supply verified Vortek graphics |
| Configuration isolation | Separate normal/portable/viewer/credential identities; safer Windows associations implemented | Runtime co-installation and account tests against disposable data |
| Packaging | Distinct NSIS/CPack identity configured for x64/ARM64; unsafe inherited MSIX staging blocked | Build internal NSIS/portable candidate after application validation |
| QA | Eleven focused fork tests passed, including native compile/run, filesystem fixtures and resource compilation | Application tests and functional slicing after dependencies finish |
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
URL disassociation also checks ownership before clearing a handler. The normal
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
VS2026 installation (11/11, 6.808 seconds); this did not change the VS2022
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

Active command: `build_win.bat -d --vs 2022 -j 2`, with the normal documented
environment (no `_CL_` override for other dependencies). Log:
`build-validation-logs/dependencies-all-cache.log`; exit checkpoint:
`build-validation-logs/dependencies-all-cache.exit`. CURL completed and OCCT
is compiling at this checkpoint. No second heavy build runs concurrently.

Static inspection of the pinned CPython archive found additional bootstrap
downloads in `PCbuild/get_externals.bat`: bzip2, SQLite, xz, zlib, libffi and
OpenSSL binaries. They use version tags via `get_external.py` and provide no
archive SHA-256 pins there. They are not covered by the 27-archive CMake audit.
Review source provenance/checksums before recovering these through an alternate
route; do not silently seed unverified archives or disable required modules.

The ignored historical trees `build-archive-20261021/` and
`deps/build-archive-20261021/` remain intact, as does the download cache.
The application archive contains a resources junction and an older executable;
that executable is not evidence for the synchronized/product branch.

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
| Fork identity suite | 11/11 passed with VS2022/Windows SDK active; latest focused run 5.247 seconds |
| Existing Windows CI step | Extracted batch step passed locally with VS2026, 11/11; four package-variable fixtures passed; no GitHub run |
| Native probes | Generated identity compiled and ran; real association helper/query compiled against fake Win32 APIs |
| Windows resources | Actual generated `.rc` compiled with Windows SDK `rc.exe` |
| Package configuration | Actual CPack config generated for x64 and ARM64; separate identities and preserved license reference verified |
| MSIX guard | Refused before staging; existing sentinel preserved |
| Configuration startup selection | Production selection code with fake wx path provider and real temporary filesystem; normal, fork-portable, upstream-portable and explicit override cases passed |
| Windows build-script suite | Earlier 192 passes/30 optional LLVM-related failures; not rerun without a relevant change |
| Source checks | Diff whitespace and changed-file credential-pattern scans passed |
| Complete product compilation | Not reached |
| GUI, slicing, preview, G-code, project round trip | Not runtime-validated |
| Installer and clean-machine deployment | Not built/run |

Fork logs: `build-validation-logs/product-identity-tests.log` and
`build-validation-logs/script-tests-product.log` (combined discovery). These focused
checks are separate from app compilation, live registry/credential behavior,
visual QA, and physical printer validation. No physical printer was operated.

Pinned baseline [CI run 36739271100](https://github.com/PrairieBoss/VortekSlicer/actions/runs/36739271100)
reported successful Windows build-script tests and Windows x64 application
unit tests. Its Windows portable/installer/MSIX artifacts exist, but predate
all product changes and could not be materialized for local smoke tests.
They must not be presented as validation of this branch.

## GitHub and pending reviews

[PR #2](https://github.com/PrairieBoss/VortekSlicer/pull/2) was last verified
open/draft, mergeable at the expected sync head, with four successful returned
workflows. The connected integration rejected marking it ready as inaccessible
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

1. Check whether the full dependency command completed. Inspect its exit file
   and log; do not launch another heavy build while it is running.
2. Apply the shell environment in [WINDOWS_BUILD.md](WINDOWS_BUILD.md), then run
   `build_win.bat -d --vs 2022 -j 2`. Preserve the successful targets and all 27
   hash-verified archives. Scope any `/Z7` workaround to the build process and
   document the exact invocation; do not modify global compiler settings.
3. After all dependencies pass, run
   `build_win.bat -s --vs 2022 -j 2 --run-tests -i`. Record application compilation,
   tests, translations, and installation separately.
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
