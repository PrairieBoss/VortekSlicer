# Windows Dependencies

VortekSlicer uses a two-level dependency model:

1. Host build tools installed on Windows.
2. Third-party C/C++ libraries downloaded and built by `deps/CMakeLists.txt`.

Do not substitute system libraries for the pinned dependency superbuild unless upstream explicitly supports it.

## Host tools

| Tool | Supported baseline | Purpose | Notes |
|---|---:|---|---|
| Windows | Windows 10/11 x64 | Host OS | Upstream requires 64-bit Windows 10 or later. |
| Visual Studio | 2022, current 17.x servicing release | MSVC, MSBuild, IDE | 17.14.37 and MSBuild 17.14.51 were validated. Install Desktop development with C++ and recommended components. |
| MSVC | Supplied by VS2022 | C/C++ compiler | 19.44.35228 / toolset 14.44.35207 was validated. Use the x64 native tools environment. |
| Windows SDK | 10.0.26100.0 validated target | Win32/WinRT headers and libraries | Exact version may advance with VS servicing; record it in build notes. |
| CMake | 4.3.x | Configure/generate/build driver | 4.3.2 was validated and matches fork CI pin `~4.3.0`. Must precede Strawberry CMake on PATH. |
| Git | Current supported Git for Windows | Clone, remotes, ExternalProject Git sources | Git LFS must also be installed even though this commit has no LFS-tracked files. |
| Strawberry Perl | Current 5.x | OpenSSL and build scripts | `perl.exe` must be available; its bundled CMake must not take precedence. |
| Ninja | Optional, 1.12+ known | `-x` Ninja Multi-Config build | Visual Studio generator remains the baseline. |
| Python | Optional for the main build | Profile validation and developer tooling | Python 3 is not listed by upstream as a required Windows compiler prerequisite. |
| OpenSSL CLI | Not used as the linked application library | Diagnostics only | The application builds its own pinned OpenSSL dependency. |
| NSIS | Optional | Installer packaging | Used by CI/CPack, not required for a portable developer build. |

## Key pinned libraries

The authoritative versions and hashes are the files under `deps/`. Important pins at the audited fork commit are:

| Library | Pin | Source definition |
|---|---:|---|
| Boost | 1.84.0 | `deps/Boost/Boost.cmake` |
| OpenSSL | 1.1.1w | `deps/OpenSSL/OpenSSL.cmake` |
| wxWidgets | SoftFever fork tag 3.3.2 | `deps/wxWidgets/wxWidgets.cmake` |
| WebView2 SDK used by wxWidgets | 1.0.3485.44 | wxWidgets nested CMake configuration |
| OCCT | 7.6.0 | `deps/OCCT/OCCT.cmake` |
| Eigen | 5.0.1 | `deps/Eigen/Eigen.cmake` |
| OpenCV | 4.6.0 | `deps/OpenCV/OpenCV.cmake` |
| oneTBB | 2021.5.0 | `deps/TBB/TBB.cmake` |
| Zlib | 1.2.13 | `deps/ZLIB/ZLIB.cmake` |
| libjpeg-turbo | 3.0.1 | `deps/JPEG/JPEG.cmake` |
| GLFW | 3.4 | `deps/GLFW/GLFW.cmake` |
| Draco | 1.5.7 | `deps/Draco/Draco.cmake` |

The repository also contains WebView2 headers and loader libraries under `deps/WebView2`; the installed x64 `WebView2Loader.dll` reports file version 1.0.3351.48. wxWidgets independently downloads NuGet SDK 1.0.3485.44 for its Edge webview build using committed SHA-256 `BC09150B179246AC90189649B13BE8E6B11B3AC200E817E18DF106E1F3CF489E`. These are separate inputs and their differing versions are expected at the audited commit.

## Dependency build behavior

- Downloads are stored under `deps/DL_CACHE`.
- Generated projects and installed dependency artifacts are under `deps/build`.
- The installed prefix is `deps/build/OrcaSlicer_dep/usr/local`.
- The main application discovers this prefix during its CMake configuration.
- Archive downloads use committed SHA-256 hashes; Git dependencies use pinned tags/commits where defined.

The clean 2026-08-05 VS2022 build completed all 23 dependency targets. Important verified outputs include `eigen_blas.dll`, `eigen_lapack.dll`, wxWidgets webview libraries, OCCT runtime DLLs, OpenSSL, Boost, OpenVDB, and the WebView2 loader used by the portable application.

`deps/build` is generator- and toolchain-specific. Never copy a VS2026 dependency tree into a VS2022 build or reuse a tree after switching generator, architecture, or dependency definitions.

## Optional and unsupported combinations

- VS2019 is recognized upstream but is not the VortekSlicer long-term baseline.
- VS2026 is recognized by the fork script but failed the audited clean dependency build. See [KNOWN_ISSUES.md](KNOWN_ISSUES.md).
- Ninja Multi-Config is optional and should be validated separately before being described as the primary workflow.
- ARM64 has separate upstream build paths and CMake constraints; this baseline covers Windows x64 only.
- Debug is not maintained upstream; use Release or RelWithDebInfo.
