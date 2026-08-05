# VortekSlicer Engineering Changelog

This changelog records fork build-environment and maintenance changes. It is separate from OrcaSlicer's user-facing release notes.

## Unreleased

### Added

- Windows build baseline documentation.
- Windows setup and dependency inventory.
- Build decision log with alternatives, risk, and removal guidance.
- Known-issues record for CMake PATH ordering, Schannel revocation, VS2026 dependency failures, memory pressure, and skipped fork CI.
- Project-structure policy that preserves the upstream OrcaSlicer monorepo layout.

### Repository configuration

- Confirmed `origin` as `https://github.com/PrairieBoss/VortekSlicer.git`.
- Configured `upstream` as `https://github.com/SoftFever/OrcaSlicer.git`.
- Created feature branch `codex/windows-build-baseline` from `origin/main`.

### Validation status

- Repository restored from an empty/incomplete working checkout without source changes.
- Clean VS2026 dependency configuration succeeded with CMake 4.3.2 and Windows SDK 10.0.26100.0.
- First dependency build diagnosed Windows Schannel certificate-revocation failure.
- Clean diagnostic retry completed 21 dependency targets and separated an independent host/network WebView2 transport failure from the VS2026 Eigen shared LAPACK link limitation.
- Installed Visual Studio Community 2022 17.14.37 side-by-side with VS2026 using the Desktop development with C++ workload.
- Completed a VS2022 Release dependency build of all 23 targets from an absent `deps\build`, retaining only the SHA-256-verified download cache and applying no source or CMake patches.
- Verified wxWidgets 3.3.2 with its SHA-256-pinned WebView2 1.0.3485.44 SDK and verified Eigen 5.0.1 shared/static BLAS and LAPACK outputs.
- Completed the clean Release application build and portable install in 31 minutes 48 seconds.
- Verified `build\OrcaSlicer\orca-slicer.exe`, `OrcaSlicer.dll`, `WebView2Loader.dll`, OCCT runtime libraries, resources, and MSVC runtime files.
- Ran `OrcaSlicer_profile_validator.exe` against all repository profiles with exit code 0.
- Confirmed that repository changes remain documentation-only; no upstream source or build configuration was modified.
