# Windows Development Setup

## 1. Hardware and operating system

- 64-bit Windows 10 or Windows 11
- 16 GB RAM minimum; 32 GB recommended
- 23 GB free disk minimum; allow additional space for multiple build configurations
- 64-bit CPU

## 2. Install Visual Studio 2022

Install Visual Studio Community 2022 with the **Desktop development with C++** workload and recommended components.

```powershell
winget install --id Microsoft.VisualStudio.2022.Community --exact `
  --override "--wait --passive --norestart --add Microsoft.VisualStudio.Workload.NativeDesktop --includeRecommended" `
  --accept-package-agreements --accept-source-agreements
```

If winget cannot complete, use Microsoft's Visual Studio 2022 bootstrapper and select the same workload in Visual Studio Installer. Keep VS2022 side-by-side if a newer Visual Studio is already installed.

The audited installation was Visual Studio Community 2022 17.14.37. A newer supported 17.x servicing release is acceptable, but record the Visual Studio, MSBuild, MSVC, and SDK versions with any build report.

Required component categories:

- MSVC v143 x64/x86 build tools
- Windows 10 or Windows 11 SDK
- C++ CMake tools for Windows
- Core desktop C++ features

## 3. Install command-line prerequisites

```powershell
winget install --id Kitware.CMake --exact
winget install --id StrawberryPerl.StrawberryPerl --exact
winget install --id Git.Git --exact
```

Git LFS is included by current Git for Windows packages. Verify it explicitly:

```powershell
git lfs version
```

Ninja is optional:

```powershell
winget install --id Ninja-build.Ninja --exact
```

## 4. Fix PATH ordering

Strawberry Perl ships its own CMake. Identify the standalone Kitware CMake directory without hard-coding a local path:

```powershell
$kitwareCMake = Join-Path $env:ProgramFiles 'CMake\bin'
$kitwareCMake
```

Ensure that directory appears on PATH before Strawberry Perl's bundled `c\bin` directory.

Open a new terminal and verify:

```powershell
where.exe cmake
cmake --version
```

The VortekSlicer baseline is CMake 4.3.x. Do not patch the repository to accept the wrong PATH entry.

## 5. Clone and create a feature branch

```powershell
$sourceRoot = Join-Path $env:USERPROFILE 'source'
New-Item -ItemType Directory -Path $sourceRoot -Force | Out-Null
Set-Location $sourceRoot
git clone https://github.com/PrairieBoss/VortekSlicer.git
Set-Location .\VortekSlicer
git remote add upstream https://github.com/SoftFever/OrcaSlicer.git
git fetch --all --prune
git switch --create feature/windows-baseline origin/main
```

Do not develop directly on `main`.

## 6. Verify Visual Studio 2022

From **x64 Native Tools Command Prompt for VS 2022**:

```bat
where msbuild
msbuild -version
where cl
cl
where cmake
cmake --version
```

MSBuild must report major version 17. If major version 18 is selected, the shell is using VS2026 and is not the validated VortekSlicer baseline.

If `cl` is missing after initialization, close terminals that were previously initialized for a different Visual Studio version and open a fresh **x64 Native Tools Command Prompt for VS 2022**. Do not hard-code a versioned MSVC path into repository files.

## 7. Build

Follow [BUILD.md](BUILD.md). Keep the first build clean and retain the complete build log when troubleshooting:

```bat
build_release_vs.bat > build-windows.log 2>&1
```

Do not commit local logs, dependency downloads, or generated build trees.

## 8. Validate

After the build reports success, verify the installed tree and run the profile validator:

```powershell
Test-Path .\build\OrcaSlicer\orca-slicer.exe
Test-Path .\build\OrcaSlicer\OrcaSlicer.dll
Test-Path .\build\OrcaSlicer\WebView2Loader.dll
.\build\src\Release\OrcaSlicer_profile_validator.exe --path .\resources\profiles
git status --short
```

Expected results are `True` for each path, validator exit code 0, and no tracked source/configuration changes. The 2026-08-05 baseline met all of these checks.
