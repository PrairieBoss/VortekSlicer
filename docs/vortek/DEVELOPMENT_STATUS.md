# VortekSlicer development status

Last verified: 2026-10-21, America/Regina.

## Baseline and branch

- Current roadmap phase: **Phase 3, Windows build validation, externally blocked**.
- Working branch: `codex/windows-build-validation`.
- Synchronization/source baseline: `04684c58f935fc5beaba4d5959dcd7741c6a22d1`.
- Latest code fix: `dcd5382b5c94c2fe382059206e9499bee5a84c10`.
- Canonical upstream source: `8d69fa3e5a9d5424899b0f9c2aaceb4af61c2c38`.
- Baseline source trees both resolve to `110cf80a49c2b4dc3e35fe4bfa97f5eaea193d10`.
- Local `main` remains `b3a0c8bd407c3de1ff1f9962eccc3dabd1e12f18`.
- Origin remains `https://github.com/PrairieBoss/VortekSlicer.git`.
- Upstream remote now uses `https://github.com/OrcaSlicer/OrcaSlicer.git`.

The validation branch adds a narrow Windows profile-warning diagnostic fix
and these engineering records. No production slicing logic, printer profiles,
application branding, or licensing notices have been changed. Use
`git log -3 --oneline` for the latest local milestone commits.

## Repository recovery

[PR #2](https://github.com/PrairieBoss/VortekSlicer/pull/2) is still open and
draft. Its head, base, expected synchronization commit, and mergeability were
verified. All four returned PR workflows completed successfully: Build all,
Check profiles, Shellcheck, and Check locale. The normal two-parent local
synchronization merge is identical to the pinned upstream source.

The connected GitHub integration can read the repository but returned
`FORBIDDEN: Resource not accessible by integration` when asked to mark PR #2
ready for review. The CLI's PrairieBoss token is invalid. No merge was
performed, and `main` was not bypassed or updated directly.

[PR #1](https://github.com/PrairieBoss/VortekSlicer/pull/1) remains an open
draft at `24efa9b85ef206cd659df8ba317f4f969d7cdc59`. Preserve it as historical
documentation; do not merge its obsolete build instructions unchanged.
No new PR has been opened in this session. A push of the validation branch
was attempted and failed with `getaddrinfo() thread failed to start`; the
milestone commits remain local until network and authentication are restored.

The previous ignored build trees, approximately 12.96 GiB and 9.62 GiB,
were moved to dated ignored archives. A resource junction in the application
tree and old validation outputs were preserved. The 0.42 GiB download cache
was retained. More than 500 GB of disk space was available before this work.
These archives remain a deferred cleanup item, not reclaimed disk space.

## Verified results

| Category | Result |
| --- | --- |
| Source baseline | Sync tree equals pinned upstream tree; working tree initially clean |
| Dependency configuration | Passed with VS2022, MSVC 19.44, SDK 10.0.26100.0, CMake 4.3.2 |
| Complete dependency build | Blocked on missing Assimp archive and unavailable network DNS; stopped retries |
| Targeted ZLIB dependency | Compiled and installed successfully with one MSBuild project and two compiler jobs |
| ZLIB sample | Compression, decompression, gzip, dictionary, and inflate checks exited 0 |
| Profile tree check | 66 vendors; 0 files with errors; 0 files with warnings |
| Profile tool unit tests | Passed after fix: 263 run, 262 passed, 1 existing upstream skip, no failures |
| Windows build-script suite | 192 passed, 30 failed; optional clang-cl/standalone LLVM unavailable |
| Pinned baseline CI | Windows build-script tests and Windows x64 application unit-test job passed |
| Pinned baseline CI packaging | Windows x64 portable, installer, and MSIX artifacts exist; not run locally |
| Application compilation | Not reached on synchronized source |
| Application unit tests | Not built or run |
| Startup, GUI, import, slicing, preview, G-code, project round trip | Not validated on synchronized source |
| Packaging and clean-machine deployment | Not attempted |

The profile suite originally failed because its temporary directories were not
writable. With a writable repository-local temporary directory, 263 tests ran:
one failed on Windows path separators and one was skipped by an existing
upstream guard for an unavailable developer-local BambuStudio clone. The
existing regression test and the complete 263-test suite pass after normalizing
the obsolete-key warning's relative path to forward slashes. The full passing
run took 84.092 seconds. No tests were disabled for this fix.

Local evidence lives in ignored `build-validation-logs/`: dependency logs,
ZLIB logs, profile check, profile unit tests, and build-script suite output.
The full dependency attempt was interrupted after confirming the missing
archive and DNS failure; it must not be counted as a successful build.

### Remote CI evidence

[Build all run 36739271100](https://github.com/PrairieBoss/VortekSlicer/actions/runs/36739271100)
belongs to sync head `04684c58f935fc5beaba4d5959dcd7741c6a22d1`.
Its returned job metadata reports success for Windows build-script tests and
Windows x64 application unit tests. Its Windows build steps include successful
application compilation, system preset cache generation, installer creation,
portable packaging, and MSIX packaging. This is remote baseline evidence,
not a local reproduction or validation of the later diagnostic fix.

The nonexpired x64 portable artifact is
`OrcaSlicer_Windows_PR2_x64_portable`, artifact ID `11115708140`, size
251052784 bytes, SHA-256 digest
`66b23e89da215ef6f47b88e080436192ef841306c33947846dc9c827dd024e08`.
Retrieval through the connected GitHub service returned a file reference, but
materialization into this workspace failed with `download failed`. No local
portable archive or application was obtained, and no executable from this CI
run was launched. If artifact transfer becomes available before a local build
can finish, use this exact artifact for additional baseline smoke tests,
verify its digest, and keep its results separate from local build evidence.

## Active blockers and required intervention

1. **Build network:** the build process cannot resolve `github.com` or
   `api.github.com`. Assimp 5.4.3 is the first missing download, and the old
   cache contains only 21 nonempty archives. Restore permitted network/DNS
   access for normal pinned dependency downloads; more missing archives may
   follow. No source workaround is justified.
2. **GitHub writes:** restore an authorized GitHub integration or CLI login
   before marking PR #2 ready, merging it normally, pushing milestones, and
   opening development PRs. Reverify PR conditions immediately before merging.
3. **Optional-toolchain test coverage:** the build-script suite assumes
   clang-cl/LLVM installations absent here. This does not establish a failure
   of the chosen MSVC baseline, but the full suite is not green.

No new application executable or distribution package was produced. The
fresh dependency artifact is `deps/build/OrcaSlicer_dep/usr/local/lib/zlib.lib`.
An older executable under the archived build is not the current product.

## Exact continuation

1. Restore build-process network access, then run the PowerShell environment
   setup and dependency command in [Windows validation](WINDOWS_BUILD.md).
   Keep the fresh `deps/build/` tree and verified download cache; do not clean
   successful work solely to retry a failed download.
2. Finish all dependency targets. Record the first meaningful failure if one
   occurs; do not reinstate the obsolete Eigen BLAS/LAPACK workaround.
3. Run `build_win.bat -s --vs 2022 -j 2 --run-tests -i` in that same configured
   shell. Record compilation, tests, translations, and install independently.
4. Use isolated application data to smoke-test startup, model import, a simple
   20 mm cube, transforms, printer/filament selection, slicing, preview, G-code
   export, project save/reopen, and shutdown. Do not send output to a printer.
5. Only after that baseline is usable, implement isolated Vortek branding and
   application-data identity on a separate feature branch.

When network and authentication are restored, also push the local validation
branch with `git push -u origin codex/windows-build-validation` and open a
reviewable PR against the synchronized `main`. Its commits separate the
profile-warning fix from the build-validation records. Do not merge that
development PR automatically.

Independently, after GitHub write access is restored, mark PR #2 ready and
merge it with a normal merge only if its head remains the expected sync
commit, target remains `main`, checks pass, and conflicts are absent. Fetch
origin and update local `main` by fast-forward only. Keep PR #1 separate.

## Prioritized backlog and acceptance gates

- **Now:** resolve external blockers, finish dependency/application builds,
  run upstream tests and functional smoke tests, then validate branding and
  separate user configuration. Refresh docs from those actual results.
- **Next:** document verified profile creation using upstream profile tools,
  produce an internal portable/installer candidate using upstream packaging,
  and validate resources, DLLs, attribution, and upgrade/uninstall behavior.
  No Vortek printer or material settings have been invented or shipped.
- **Later:** adapt the existing Windows CI only where the fork needs it;
  document upstream synchronization, support boundaries, and release checks.
- **Experimental:** AI and manufacturing-system integrations remain outside
  initial product acceptance.

Release readiness is **not established**. The synchronized application has
not yet compiled or run locally, is not Vortek-branded, and has no tested
distribution artifact. Required acceptance evidence still includes functional
slicing, configuration isolation, representative tests, packaging and
clean-machine validation, preserved licenses, and a reviewed internal
candidate. Public release still requires explicit approval.
