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

.\build_win.bat -d --vs 2022 -j 2
if ($LASTEXITCODE -ne 0) { throw 'Dependency build failed; inspect its first error.' }
```

The single-project setting limits nested MSBuild projects. The batch script's
`-j 2` separately sets `CL_MPCount=2` for compiler parallelism. An initial run
with `CMAKE_BUILD_PARALLEL_LEVEL=2` stalled at MSBuild's system-check stage;
the serial-project retry progressed. The exact cause of that stall was not
established. Do not run multiple heavy builds concurrently.

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

## Downloads and local outputs

Dependency archives stay in `deps/DL_CACHE/`. CMake verifies their pinned
hashes. A clean build still needs network access for archives that are absent
or invalid; the previous cache is not a complete set for this source revision.
The first observed missing archive is Assimp 5.4.3. Local DNS resolution of
`github.com` and `api.github.com` failed in this execution environment.
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
the ordered continuation steps.
