# Build Notes and Decision Log

This file records build-engineering decisions for the permanent VortekSlicer development environment. Entries state why an action was required, alternatives, risk, and whether it should later be removed.

## 2026-08-04 — Establish fork baseline

**Decision:** Use `PrairieBoss/VortekSlicer` as `origin`, `SoftFever/OrcaSlicer` as `upstream`, and perform work on `codex/windows-build-baseline` created from `origin/main`.

**Why:** This preserves the user's fork as the development authority while keeping upstream updates fetchable and reviewable.

**Alternatives considered:** Branch directly from upstream; merge upstream into the fork immediately; work directly on `main`.

**Risk:** At audit time, `origin/main` was 518 commits behind `upstream/main`. Build results describe the fork baseline, not current upstream.

**Remove later:** No. Re-evaluate the divergence before feature development and integrate upstream in a dedicated branch/PR.

## 2026-08-04 — Preserve upstream repository layout

**Decision:** Do not introduce a nested `upstream/`, duplicate `src/`, or patch-stack repository layout.

**Why:** OrcaSlicer is already a large monorepo with established `src`, `deps`, `resources`, `scripts`, and CI paths. Mirroring it inside another hierarchy would make merges and build instructions harder.

**Alternatives considered:** Reorganize into `upstream/`, `patches/`, `branding/`, and a second `src/`; maintain the fork as a patch queue over an untouched checkout.

**Risk:** Vortek-specific changes will coexist with upstream files and require disciplined commits.

**Remove later:** No. Add `branding/` only when real branding assets exist; add `patches/` only if an external patch queue becomes necessary.

## 2026-08-04 — CMake baseline and PATH order

**Decision:** Require CMake 4.3.x and require it to appear before Strawberry Perl's `c\bin` on PATH.

**Why:** The fork's Windows CI pins CMake `~4.3.0`. The active shell initially resolved Strawberry's CMake 3.29.2, and the root CMake configuration explicitly rejects this PATH ordering outside CI.

**Alternatives considered:** Continue with CMake 3.29.2; patch the project check; hard-code a machine-local CMake path in project files.

**Risk:** Future upstream CI may update the 4.3.x pin.

**Remove later:** Update the documented version when upstream changes its CI pin. Do not remove the PATH-order check.

## 2026-08-04 — TLS revocation failure

**Decision:** Treat `CRYPT_E_NO_REVOCATION_CHECK` as a Windows/network environment failure, not a source problem.

**Why:** CMake and Windows curl failed against several GitHub URLs using Schannel; Windows curl succeeded with `--ssl-revoke-best-effort`, and PowerShell's HTTPS client succeeded. CMake configuration and local compilation were already healthy.

**Alternatives considered:** Repair CRL/OCSP reachability; prefetch with a verified downloader; disable CMake TLS verification; patch dependency URLs.

**Risk:** Disabling TLS verification weakens transport security. The diagnostic retry was scoped to CMake archive downloads whose committed SHA-256 hashes were verified first.

**Remove later:** The exception must not become a default script setting. Remove it from the host after certificate revocation access is repaired.

## 2026-08-04 — Reject VS2026 as the initial baseline

**Decision:** Install and validate Visual Studio 2022 before considering source/build patches for VS2026.

**Why:** A clean VS2026 dependency build completed 21 dependency targets but did not finish. wxWidgets' nested WebView2 NuGet transfer first encountered an independent host/network failure, and Eigen 5.0.1 then reproduced a VS2026 shared LAPACK link failure. The fork's scheduled Windows CI jobs were skipped, so no fork CI evidence validated VS2026.

**Alternatives considered:** Add Eigen flags to disable unused BLAS/LAPACK/shared targets; pre-stage WebView2 and continue on VS2026; merge all 518 upstream commits; install VS2022 side-by-side.

**Risk:** VS2022 adds disk usage and another maintained toolchain. It is nevertheless the lower-risk compatibility baseline.

**Remove later:** Revisit only after upstream or a focused Vortek branch validates VS2026 end to end.

## 2026-08-04 — Memory guidance

**Decision:** Document 32 GB RAM as recommended even though upstream lists 16 GB as minimum.

**Why:** On a 15.7 GB usable-memory machine, the VS2026 dependency attempt reached roughly 50 build processes and only 0.3 GB free physical memory. The successful VS2022 dependency build fell below 1 GB free, and the successful application build reached approximately 0.5 GB free while compiling `libslic3r`.

**Alternatives considered:** Patch upstream parallel flags immediately; accept paging; require 32 GB.

**Risk:** A hard 32 GB requirement would exclude otherwise viable developer machines.

**Remove later:** Keep 16 GB as minimum and 32 GB as recommendation until a tested limited-parallelism launcher is available.

## 2026-08-05 — Adopt the validated VS2022 baseline

**Decision:** Use Visual Studio Community 2022 17.14.37, MSBuild 17.14.51, MSVC 19.44.35228 (toolset 14.44.35207), Windows SDK 10.0.26100.0, and CMake 4.3.2 as the measured Windows x64 baseline.

**Why:** With `deps\build` absent and only the hash-verified `deps\DL_CACHE` retained, the dependency build completed all 23 targets, including wxWidgets/WebView2 and Eigen's shared LAPACK library. A clean Release application build and install then completed in 31 minutes 48 seconds, and the built profile validator passed all repository profiles.

**Alternatives considered:** Patch Eigen or wxWidgets for VS2026; make VS2019 the baseline; use Ninja Multi-Config; modify upstream CMake or C++ sources.

**Risk:** VS2022 servicing updates may change the exact MSVC toolset while remaining within the supported 17.x family. CMake, MSVC, and SDK versions must be recorded when investigating a regression.

**Remove later:** Keep VS2022 as the baseline until a separate, clean, end-to-end validation supports a successor. Update exact measured versions after intentional revalidation; do not silently broaden support.

## 2026-08-05 — Keep host workarounds out of repository scripts

**Decision:** Do not add hard-coded CMake, Visual Studio, MSVC, or local download paths to the repository. Keep the audited host's TLS exception and compiler-PATH correction process-local.

**Why:** The supported build script succeeds unchanged when supplied a correct VS2022 environment. The observed problems were host PATH/TLS state, not project configuration defects.

**Alternatives considered:** Add a Vortek-only wrapper with machine paths; modify `build_release_vs.bat`; disable TLS verification in CMake; commit downloaded WebView2 artifacts.

**Risk:** Developers must verify their shell before building. The upstream batch script also does not consistently stop at every failed subcommand, so logs and expected outputs must be checked.

**Remove later:** The host-only workarounds should be removed when PATH initialization and certificate-revocation access are repaired. Reconsider a wrapper only if it can discover tools without local paths, preserve upstream behavior, and add tested error propagation.
