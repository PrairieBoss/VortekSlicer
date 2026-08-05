# Known Issues

## Fork is behind upstream

At the 2026-08-04 audit, `origin/main` was 518 commits behind `upstream/main` with no fork-only commits in that comparison.

**Impact:** Fixes and dependency updates in current OrcaSlicer may be absent.

**Recommendation:** Integrate upstream in a dedicated branch and PR after the fork baseline is reproducibly built. Do not combine the upstream sync with build-environment documentation.

## Strawberry Perl CMake shadows Kitware CMake

**Symptom:** `where cmake` lists Strawberry Perl's bundled `c\bin\cmake.exe` first, and `cmake --version` reports 3.29.2 on the audited host.

**Root cause:** Strawberry Perl's `c\bin` precedes the supported CMake installation on PATH.

**Solutions:**

1. Put the standalone Kitware CMake directory before Strawberry on the system PATH (recommended).
2. Use a correctly initialized build shell that prepends the supported CMake directory.
3. Do not remove the repository's PATH-order guard.

## Schannel cannot check certificate revocation

**Symptom:** CMake dependency downloads fail with status 35 and `CRYPT_E_NO_REVOCATION_CHECK`.

**Verified diagnosis:** Windows curl fails normally against the same GitHub URL and succeeds with `--ssl-revoke-best-effort`; PowerShell HTTPS succeeds.

**Solutions:**

1. Restore CRL/OCSP network reachability or correct enterprise proxy/certificate policy (recommended).
2. Securely prefetch archives with a certificate-validating downloader and verify committed SHA-256 hashes.
3. As a last-resort diagnostic only, scope `CMAKE_TLS_VERIFY=0` to the dependency download after confirming every affected archive has a committed hash.

**Risk:** Disabling TLS verification must never become the default workflow.

## Visual Studio 2026 validation blockers

**Status:** Reproduced on VS2026 18.7.3, MSVC 19.51.36248, CMake 4.3.2, Windows SDK 10.0.26100.0.

Two independent failures occurred:

1. wxWidgets 3.3.2 failed downloading WebView2 SDK 1.0.3485.44 from NuGet with status 55.
2. Eigen 5.0.1 built `eigen_lapack_static` but failed linking the shared `eigen_lapack` target with 38 unresolved symbols (`LNK1120`).

The WebView2 status-55 event was a transport/environment failure and is not evidence of compiler incompatibility. The reproducible VS2026 toolchain limitation is Eigen's shared LAPACK link.

**Solutions considered:**

- Build with VS2022 (recommended baseline).
- Disable unused Eigen BLAS/LAPACK/shared artifacts in `deps/Eigen/Eigen.cmake`, with an upstreamable patch and separate VS2022 regression check.
- Pre-stage the hash-verified WebView2 NuGet package for wxWidgets.

Do not label VS2026 supported for VortekSlicer until a clean dependency and application build succeeds.

**Validated resolution:** The unchanged dependency definitions completed all 23 targets under VS2022 17.14.37/MSVC 19.44, including wxWidgets WebView2 and Eigen shared LAPACK. This verifies that a source patch is not required for the supported baseline.

## High memory use during dependency build

**Symptom:** A 16 GB machine pages heavily. The VS2026 dependency attempt reached about 50 processes and 0.3 GB free physical memory. The successful VS2022 dependency build dropped below 1 GB free, and the application build reached approximately 0.5 GB free while compiling `libslic3r`.

**Recommendation:** Use 32 GB RAM when possible. Sixteen GB is a validated minimum on this host, not a comfortable target. A future launcher may add verified parallelism limits; do not patch dependency source to work around host memory.

## Batch completion text is not sufficient validation

**Symptom:** `build_release_vs.bat` can continue to its completion footer after a nested CMake/MSBuild command fails because not every command is followed by an error-level check.

**Impact:** The text `Build completed` by itself is not proof of success.

**Recommendation:** Require a zero process exit, scan the retained log for fatal CMake/compiler/linker errors, verify `build\OrcaSlicer\orca-slicer.exe`, and run the profile validator. A future error-propagation patch should be small, tested across all supported batch modes, and proposed upstream rather than carried as an undocumented fork change.

## Fork GitHub Actions do not validate Windows

Recent scheduled `Build all` runs for the audited fork commit reported Windows jobs as skipped.

**Impact:** A green maintenance workflow or shellcheck is not evidence that the application builds.

**Recommendation:** Add an intentional fork CI policy now that the first local reproducible build is complete, with dependency caching and explicit x64 VS2022 coverage. Keep that work in a separate feature branch and PR.
