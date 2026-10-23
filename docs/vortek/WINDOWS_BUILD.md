# VortekSlicer Windows validation

This fork uses the upstream `build_win.bat` workflow. See the
[official Windows guide](https://github.com/OrcaSlicer/OrcaSlicer/wiki/how_to_build_windows)
for its full option reference. This document records the locally exercised
configuration; it does not certify an application build.

## Source and prerequisites

The validation source is synchronization commit
`04684c58f935fc5beaba4d5959dcd7741c6a22d1`, whose tree matches upstream
`8d69fa3e5a9d5424899b0f9c2aaceb4af61c2c38`. Keep fork changes on feature
branches until the synchronization PR has been merged through GitHub.

Tools observed on 2026-10-21:

| Component | Observed version |
| --- | --- |
| Visual Studio Community 2022 | 17.14.37516.0, product release 17.14.37 |
| MSBuild | 17.14.51 |
| MSVC, x64 host and target | 19.44.35228.0, toolset directory 14.44.35207 |
| Windows SDK selected by CMake | 10.0.26100.0 |
| CMake used by the build script | 4.3.2 |
| Python used for profile tests | CPython 3.14.6 |

The standalone CMake is installed under `Tools/CMake/bin` beside this checkout.
`where.exe cmake` also finds Strawberry Perl's CMake 3.29.2 first. The upstream
batch script selects the standalone copy for its own subprocesses; this does
not change global PATH. Python for profile tooling is distinct from the
application's required bundled Python 3.12.13 dependency.

## Conservative build commands

Run in PowerShell from the repository root. All environment settings below
apply only to the current shell and its subprocesses.

```powershell
$buildTemp = Join-Path (Get-Location) 'build-validation-temp'
New-Item -ItemType Directory -Path $buildTemp -Force | Out-Null
$env:TEMP = $buildTemp
$env:TMP = $buildTemp
$env:TMPDIR = $buildTemp
$env:CMAKE_BUILD_PARALLEL_LEVEL = '1'
$env:MSBUILDDISABLENODEREUSE = '1'
$env:LC_ALL = 'C'
$env:LC_CTYPE = 'C'
$env:LANG = 'C'

# This host's six-entry, independently Git-tree-verified CPython cache.
# See DEPENDENCY_CACHE_PROVENANCE.json; a clean checkout may fetch normally.
$env:EXTERNALS_DIR = Join-Path (Get-Location) 'deps\DL_CACHE\python3\externals'
$env:PYTHON = 'C:\Python314\python.exe'

.\build_win.bat -d --vs 2022 -j 2
if ($LASTEXITCODE -ne 0) { throw 'Dependency build failed; inspect its first error.' }
```

The single-project setting limits nested MSBuild projects. The batch script's
`-j 2` separately sets `CL_MPCount=2` for compiler parallelism. An initial run
with `CMAKE_BUILD_PARALLEL_LEVEL=2` stalled at MSBuild's system-check stage;
the serial-project retry progressed. The exact cause of that stall was not
established. Do not run multiple heavy builds concurrently.
The bundled-Python recipe now propagates a positive explicit
`CMAKE_BUILD_PARALLEL_LEVEL=N` to PCbuild as `-M /m:N`; PCbuild would otherwise
start an unbounded nested MSBuild. Reconfigure if changing this limit, because
the external build command captures it at CMake configuration time. Empty or
unset values retain upstream's default behavior. Four configuration fixtures
passed and the actual generated command was checked with the one-project limit.

Only after **all** dependencies complete, run the application build and tests:

```powershell
.\build_win.bat -s --vs 2022 -j 2 --run-tests -i
if ($LASTEXITCODE -ne 0) { throw 'Application build, tests, translations, or install failed.' }
```

That second command is the next application-build step from the checked-out
script; it has not completed locally on the synchronized source. Expected
paths are `build/src/Release/orca-slicer.exe` and the installed `build/OrcaSlicer/`
directory. Their existence alone would not prove slicing or GUI functionality.

For targeted dependency diagnosis, the existing script supports:

```powershell
.\build_win.bat -d -t dep_ZLIB --vs 2022 -j 2
```

This command completed on the synchronized source. Its cached archive passed
the upstream SHA-256 verification; ZLIB compiled and installed. Its generated
`example.exe` also completed successfully. Run that sample from a temporary
working directory because it writes `foo.gz`.

The continuation recovered Assimp 5.4.3 through the browser, verified its
upstream-pinned SHA-256, and resumed this same procedure. Assimp, Boost, Eigen,
CGAL, Cereal, Draco, and Expat completed. FFmpeg, Python, Qhull, SolveSpaceLib, and wxInspector archives were subsequently
recovered and verified as well. All 27 generated archive pins pass a cache audit.
Retain successful build stamps; third-party bootstrap downloads are separate.
Six CPython bootstrap archives were then recovered at the exact official
commits behind its requested version tags. Their 1,322 file blobs and complete
Git trees matched the official repositories before use; the resulting archive
SHA-256 hashes and provenance are saved in
[DEPENDENCY_CACHE_PROVENANCE.json](DEPENDENCY_CACHE_PROVENANCE.json).
CPython did not supply archive checksum pins for these secondary downloads.
Its actual `get_externals.bat --no-tkinter` passed against the cache without
downloading. This does not establish a compiled Python runtime.

## Checks available before the full application build

With the temporary-directory settings above:

```powershell
python -m unittest discover -s scripts/tests -t scripts
python scripts/orca_profile_tool.py check
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/test_build_win.ps1
git diff --check
```

The PowerShell switch affects that process only. No execution-policy registry
setting was changed. The profile tests initially encountered access-denied
errors in the sandbox's default temporary directory; using the repository's
ignored build-temporary directory resolved that problem.

The build-script suite covers optional toolchains as well as MSVC. On this
host it reported 192 passes and 30 failures; failing cases depend on absent
Visual Studio `clang-cl` or a standalone `C:/Program Files/LLVM` installation.
Do not report the complete suite as green or install LLVM merely to disguise
the missing coverage. Review those cases when that toolchain is available.

The existing profile unit test exposed a Windows-only warning-path separator
mismatch. The fork normalizes that diagnostic with `Path.as_posix()`; profile
values, identifiers, slicing code, and file contents are unaffected.

For focused product identity/configuration/packaging checks, activate the
already-installed VS2022 compiler and SDK for the test process:

```powershell
cmd.exe /d /c 'call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul && python -m unittest discover -s scripts/tests -p test_product_identity.py -v'
```

Use the writable temporary-directory settings above. This suite passed all
twelve tests, including native compile/run, configuration filesystem fixtures
and resource compilation. If no
developer environment is active, native probes are explicitly skipped; do not
count that as full native coverage. The suite never writes live associations,
credentials, or user config. Its CPack fixtures configure packages but do not
install or publish anything.
The combined `unittest discover -s scripts/tests -t scripts` run after these
changes completed 274 tests with VS2022 active: 273 passed and the existing
developer-local Bambu clone case was skipped (146.812 seconds). See
`build-validation-logs/script-tests-product.log` and its zero exit checkpoint.
The later Python project-limit correction has its own four-case CMake fixture:

```powershell
python -m unittest discover -s scripts/tests -p test_python_build_config.py -v
```

It passed separately. The recorded 274-test combined run predates this test
and the executable-path regression test; the current twelve-test native
identity suite passed independently after both path-safety fixes.

## Downloads and local outputs

Dependency archives stay in `deps/DL_CACHE/`. CMake verifies their pinned
hashes. A clean build still needs network access for archives that are absent
or invalid; all 27 generated archive pins were verified at this checkpoint.
The first missing archive, Assimp 5.4.3, has been recovered and hash-verified.
The remaining generated archives have also been recovered. DNS resolution of
`github.com`, `api.github.com`, and
`www.microsoft.com` failed in subprocesses; browser access worked for Assimp.
This distinction matters: do not diagnose the whole host network as broken.
Do not disable TLS verification, reuse incompatible compiled dependencies, or
remove a required dependency to work around this restriction.

The ignored `build-validation-logs/` directory contains local command logs and
exit-code files. An interrupted command may have no exit-code file: absence
does not mean success. These outputs are evidence for the current checkout,
not application distributions.

The previous trees were archived as `build-archive-20261021/` and
`deps/build-archive-20261021/`. Both are ignored and contain no Git-tracked
files. The former contains a resources junction into the source tree and an
older application build. They were retained rather than recursively deleted;
the archived executable is not evidence for this synchronized revision.

See [development status](DEVELOPMENT_STATUS.md) for the current blockers and
the ordered continuation steps. That record also identifies the pinned CI
Windows packages and successful remote unit-test job. Artifact transfer into
the local workspace failed, so those packages have not been smoke-tested here.

## Local OpenSSL debug-symbol workaround

OpenSSL stalled compiling with `/Zi /FS`, including with a fresh PDB path. The
same source compiled with `/Z7`; the host PDB service's root cause is unresolved.
For this target only, the following process-local override produced the static
libraries and tool/test executables. Those test executables were not run as a
complete test suite.

```powershell
$env:_CL_ = '/Z7'
.\build_win.bat -d -t dep_OpenSSL --vs 2022 -j 2 --no-configure
```

MSVC reads `_CL_` after command-line flags, so its `/Z7` supersedes `/Zi` and
stores symbols in the object/library files. The first install then failed
copying the absent `ossl_static.pdb`. With this confirmed failure only, the
following adjustment was applied to the ignored generated Makefile. It does
not change a tracked dependency recipe or manufacture a PDB.

```powershell
@'
from pathlib import Path
path = Path('deps/build/dep_OpenSSL-prefix/src/dep_OpenSSL/makefile')
lines = path.read_bytes().splitlines(keepends=True)
matches = [i for i, line in enumerate(lines) if b'copy.pl" ossl_static.pdb' in line]
assert len(matches) == 1, 'Unexpected OpenSSL install rule; inspect manually'
i = matches[0] - 1
old = b'@if "$(SHLIBS)"==""'
new = old + b' if exist ossl_static.pdb'
if new not in lines[i]:
    assert old in lines[i], 'Unexpected OpenSSL install guard'
    lines[i] = lines[i].replace(old, new, 1)
    path.write_bytes(b''.join(lines))
'@ | python -
.\build_win.bat -d -t dep_OpenSSL --vs 2022 -j 2 --no-configure
Remove-Item Env:\_CL_
```

The second command exited zero. An installed-library probe linked `libssl.lib`
and `libcrypto.lib`, verified SHA-256 for `abc`, and created/freed a TLS context.
CURL subsequently compiled and installed against this dependency. This local
workaround has not established a clean-checkout build or full OpenSSL test
result. Re-extraction replaces the generated Makefile adjustment; logs and
the active dependency command are recorded in the status file.

## Bundled Python debug-symbol workaround

The normal Python build reached MSVC C1902 (program database manager mismatch).
The installed compiler/PDB DLL file versions matched, so the host service's root
cause remains unresolved. A target-scoped object-symbol override built and
installed Python 3.12.13 without changing installed toolchain files:

```powershell
$env:_CL_ = '/Z7'
.\build_win.bat -d -t dep_python3 --vs 2022 -j 2 --no-configure
Remove-Item Env:\_CL_
```

Use the normal environment above, including `EXTERNALS_DIR` and `PYTHON`.
Unlike OpenSSL, Python required no generated install-rule adjustment. The staged
64-bit interpreter passed isolated startup, SSL/ctypes imports, zlib/bz2/lzma
round trips, and an in-memory SQLite create/insert/query. This validates the
staged interpreter and selected modules, not the complete Python test suite.
Logs: `python-z7-20261022.log` and `python-runtime-20261022.log` in the build log
directory, both with zero exit checkpoints.

## Verified offline wxWidgets source

wxWidgets uses Git rather than one of the 27 hash-pinned archive downloads.
Its upstream recipe names branch `v3.3.2`, not a tag. On 2026-10-22 the official
branch resolved to `88f3483ca546fbf4ad732e1acd94cc930935077a`, tree
`36690131b619fe14706f8429c38d242abd304d2f`. The archived checkout was its parent
`db1005db3dea2c37a46fb455a9a02e37aa360751`, not the required complete revision.
GitHub's commit response identifies one changed file,
`build/cmake/wxWidgetsConfig.cmake.in`, blob
`2593c045b89b9fd191b8a27adf8c5247602acb59`.

The source cache was reconstructed from the archived Git objects and that
exact official blob. The resulting Git root tree matched the official commit;
every exported file was checked against its Git blob hash. Required catch,
pcre and libwebp exports matched their parent gitlinks. No generated build
outputs were copied. Commit, tree, submodule hashes and file counts are recorded
in `DEPENDENCY_CACHE_PROVENANCE.json`; this is Git-content verification, not an
upstream archive SHA-256 claim.

The optional `ORCA_WXWIDGETS_SOURCE_DIR` cache variable supplies a verified source
tree without Git download/update operations. It requires the main source and
all three required submodules at configure time. Its presence checks do not
verify provenance: audit the supplied revision and file contents first. The
normal online checkout remains unchanged when the option is empty.

```powershell
$env:ORCA_DEPS_CMAKE_ARGS = '-DORCA_WXWIDGETS_SOURCE_DIR=C:/Vortek_Manufacturing/Tools/VortekSlicer/deps/DL_CACHE/wxWidgets/88f3483ca546fbf4ad732e1acd94cc930935077a'
.\build_win.bat -d -t dep_wxWidgets --vs 2022 -j 2
```

The path is persisted in `deps/build/CMakeCache.txt`. To return to the online
recipe, configure with `-DORCA_WXWIDGETS_SOURCE_DIR=` through the same extra-args
variable; merely clearing the environment does not clear a CMake cache entry.
The three focused CMake tests preserve the default Git recipe, execute offline
download/update targets with a path containing spaces without changing source
files, and reject each missing required source component. Run with:

```powershell
python -m unittest discover -s scripts/tests -p test_wxwidgets_build_config.py -v
```

The first offline wx configure then reached its secondary NuGet dependency.
`webview2.nuget` in the archived build matched the required WebView2 SDK
1.0.3485.44 SHA-256
`bc09150b179246ac90189649b13be8e6b11b3ac200e817e18df106e1f3cf489e`.
That verified archive was copied into `deps/DL_CACHE/wxWidgets/` and freshly
extracted into the new wx build's default
`libs/webview/packages/Microsoft.Web.WebView2.1.0.3485.44` directory. No archived
compiled wx libraries were reused. A clean build must likewise stage this
verified SDK package or retrieve it normally; the source override alone does
not supply secondary dependencies.

## Current application build

All dependency targets completed with the final standard dependency command.
The application build uses the supported option below to avoid the confirmed
host PDB issue while preserving GUI, CAD and tests:

```powershell
$env:ORCA_SLICER_CMAKE_ARGS = '-DSLIC3R_MSVC_PDB=OFF'
.\build_win.bat -s --vs 2022 -j 2 --run-tests -i
```

This disables compiler PDB generation for this CMake build, not core features.
The process environment and existing CMake cache must be recorded for a
reproduction. The optional uv 0.11.21 download failed DNS during configuration;
upstream allows continuing without it. No alternative uv was substituted.
Compilation/test/install completion must be checked in the authoritative status
record rather than inferred from successful dependency builds.

## Verified optional uv recovery

The pinned Windows uv 0.11.21 archive is now cached at
`deps/DL_CACHE/uv/0.11.21/uv-x86_64-pc-windows-msvc.zip`. Browser-backed
retrieval reached the official HTTPS release when local execution DNS could
not. The 23,452,481-byte archive matched the `CMakeLists.txt` SHA-256 pin
before and after transfer, and its ZIP integrity check passed. No TLS setting
or dependency version changed.

To restore it into a fresh application build tree from this verified cache:

```powershell
$uvArchive = 'deps/DL_CACHE/uv/0.11.21/uv-x86_64-pc-windows-msvc.zip'
$uvExpected = 'ace861f360c6de2babedc1607d0f454b6b09a820dbc8182dc15af927e4df9589'
if ((Get-FileHash -LiteralPath $uvArchive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $uvExpected) {
    throw 'Pinned uv archive hash mismatch'
}
Expand-Archive -LiteralPath $uvArchive -DestinationPath 'build/.uv/0.11.21' -Force
```

The normal configure step detects `build/.uv/0.11.21/uv.exe` without downloading.
An already configured application needs a configuration pass after the active
compiler batch completes to capture its path and enable its install rule.
The current executable was also copied into
`build/src/Release/tools/uv/uv.exe`, the existing runtime fallback location.
Do not copy binaries into the source resources junction.

`uv --version` reports 0.11.21. An isolated, offline `uv venv` using the staged
CPython 3.12.13 succeeded, and that environment passed SSL/ctypes/SQLite imports.
Its cache and environment live only under `build-validation-temp/`.
Logs: `uv-cache-20261022.log` and `uv-runtime-20261022.log`, both exit zero.
Archive/executable hashes are in `DEPENDENCY_CACHE_PROVENANCE.json`.
This validates selected tool/runtime behavior, not application discovery,
package installation, or the final package layout.
