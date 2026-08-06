# Building VortekSlicer on Windows

This document defines the supported local Windows build for the VortekSlicer fork. It intentionally follows OrcaSlicer's native build layout and scripts.

## Supported baseline

- Windows 10 or 11, 64-bit
- Visual Studio 2022 (17.x) with **Desktop development with C++** and recommended components
- CMake 4.3.x
- Strawberry Perl
- Git and Git LFS
- At least 23 GB free disk space
- 16 GB RAM minimum; 32 GB is recommended for dependency builds

Validated on 2026-08-05 with Visual Studio Community 2022 17.14.37, MSBuild 17.14.51, MSVC 19.44.35228 (toolset 14.44.35207), Windows SDK 10.0.26100.0, and CMake 4.3.2.

Visual Studio 2026 is not the VortekSlicer baseline. The fork's build script recognizes it, but the clean 2026-08-04 validation reproduced an Eigen 5.0.1 shared LAPACK link limitation. The same run also encountered an independent host/network WebView2 transfer failure. See [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

## Clone and configure remotes

```powershell
git clone https://github.com/PrairieBoss/VortekSlicer.git
Set-Location VortekSlicer
git remote add upstream https://github.com/SoftFever/OrcaSlicer.git
git remote -v
```

Expected topology:

```text
origin    https://github.com/PrairieBoss/VortekSlicer.git
upstream  https://github.com/SoftFever/OrcaSlicer.git
```

Create a feature branch before changing the fork:

```powershell
git switch --create feature/<short-description> origin/main
```

## Verify the shell

Open **x64 Native Tools Command Prompt for VS 2022**. Do not use an ordinary terminal unless it has been initialized with the VS2022 developer environment.

```bat
where cmake
cmake --version
where msbuild
msbuild -version
where cl
cl
where perl
perl -v
git --version
git lfs version
```

Requirements:

- `cmake --version` reports 4.3.x.
- `where cmake` lists the standalone Kitware or VS2022 CMake before Strawberry Perl's bundled CMake.
- MSBuild reports major version 17.
- `cl` identifies an x64 Microsoft compiler.

## Clean Release build

Generated directories are deliberately excluded from Git. For a from-scratch build, remove only these generated paths if they exist:

```powershell
foreach ($path in @('.\build', '.\deps\build')) {
    if (Test-Path -LiteralPath $path) {
        Remove-Item -LiteralPath $path -Recurse -Force -ErrorAction Stop
    }
}
```

Run the upstream-compatible build entrypoint from the repository root:

```bat
build_release_vs.bat
```

The script performs three stages:

1. Configures and builds pinned third-party dependencies under `deps\build`.
2. Configures and builds VortekSlicer under `build`.
3. Runs localization generation and installs the portable tree under `build\OrcaSlicer`.

Useful supported variants:

```bat
build_release_vs.bat deps
build_release_vs.bat slicer
build_release_vs.bat debuginfo
build_release_vs.bat -x
```

- `deps` builds dependencies only.
- `slicer` requires an already successful dependency build.
- `debuginfo` selects `RelWithDebInfo`.
- `-x` uses Ninja Multi-Config; Visual Studio 2022 is the default and the project baseline.

Debug builds are not maintained upstream and are not the reproducibility baseline.

## Expected outputs

After a successful Release build:

```text
build\OrcaSlicer.sln
build\src\Release\orca-slicer.exe
build\OrcaSlicer\
```

The 2026-08-05 validation started with absent `deps\build` and `build` directories and completed all 23 dependency targets. It retained only `deps\DL_CACHE`, whose downloaded archives were rechecked against committed hashes. The clean Release application build and portable install completed in 31 minutes 48 seconds on a 16 GB machine. Build time varies substantially with CPU, memory, storage, network, and cache state.

## Validation

Confirm that the executable and portable install exist, then run the built profile validator. The default Windows release build enables Orca tools but does not enable the full test suite.

```powershell
Test-Path .\build\src\Release\orca-slicer.exe
Test-Path .\build\OrcaSlicer\orca-slicer.exe
Test-Path .\build\OrcaSlicer\WebView2Loader.dll
.\build\src\Release\OrcaSlicer_profile_validator.exe --path .\resources\profiles
git status --short
```

The profile validator returned exit code 0 against all fork profiles during the baseline validation. Launch the installed GUI from `build\OrcaSlicer\orca-slicer.exe` for an interactive smoke test when a desktop session is available; do not use GUI launch as the only automated validation.

For a test-enabled configuration, use a separate build directory and `-DBUILD_TESTS=ON`; do not alter the validated Release tree.

## Network and integrity

The dependency superbuild downloads pinned source archives and validates committed SHA-256 hashes. Normal builds must keep TLS verification enabled.

If CMake fails with `CRYPT_E_NO_REVOCATION_CHECK`, repair Windows certificate revocation access first. `CMAKE_TLS_VERIFY=0` was used only as a process-scoped host workaround during the audited build after verifying that the affected archive downloads had committed SHA-256 hashes. It is not the default procedure for a new machine and must not be committed to a build script.

The upstream batch script may print its completion footer even after an earlier subcommand fails. Treat a successful process exit, an empty fatal-error scan, the expected installed tree, and the profile-validator result as the complete validation set.

See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for installation and [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for troubleshooting.
