# VortekSlicer actionable backlog

The authoritative current results and blockers are in
[DEVELOPMENT_STATUS.md](DEVELOPMENT_STATUS.md). This backlog ranks remaining
work by product value and dependencies.

| Priority | Task | Dependency | Acceptance evidence |
| --- | --- | --- | --- |
| 1 | Finish the active dependency build, starting with OCCT | OpenSSL/CURL passed; no concurrent heavy build | Target exits recorded; preserve successful stamps |
| 2 | Build and validate bundled Python when its target is reached | Six external trees verified; offline bootstrap passed; explicit project limit fixed | Python 3.12.13 stages correctly with required modules; native integration tests pass |
| 3 | Compile/install the product branch and run application tests | Complete dependencies | Application, tests, translations, and install results recorded independently |
| 4 | Test clean startup and co-installation | Product executable | Orca and Vortek config directories remain distinct; original data unchanged |
| 5 | Test cube import, transforms, slice, preview, G-code, and project round trip | Working GUI | Saved test project/G-code and documented results, no physical print |
| 6 | Runtime-test the updater guard; review forced upgrades and cloud callbacks | Product executable; provider integration review | Normal checks offer no upstream installer; login does not seize Orca's protocol |
| 7 | Apply verified Vortek icon/splash/About assets | Existing approved brand assets | Resource compilation and visual checks at common Windows scaling values |
| 8 | Finish visible branding without replacing compatibility identifiers | GUI and localization checks | Main flows identify Vortek; required upstream credits remain |
| 9 | Build an internal NSIS/portable candidate | Tested install tree | Separate install/uninstall behavior, complete DLL/resources/license layout |
| 10 | Document and verify profile import/creation | Working validator and slicer | Malformed fixtures fail; verified settings round-trip; no invented production profiles |
| 11 | Enable isolated MSIX packaging only if needed | Verified publisher/assets and reviewed manifest | Distinct identity, protocols, alias, data exclusion, upgrade and uninstall tests |
| 12 | Run the adapted Windows CI on GitHub | Write access; locally checked workflow changes committed | Native identity suite and product-aware NSIS/portable artifacts pass on hosted runners |
| 13 | Validate a clean checkout and clean-machine deployment | Full candidate build | Independent reproducible build and runtime dependencies confirmed |

Independent maintenance tasks:

- Restore GitHub CLI/integration write access; reverify and normally merge
  sync PR #2, then fast-forward local main. Do not merge historical PR #1.
- Push the validation and product-identity branches and prepare reviewable
  PRs after synchronization. Do not merge unvalidated product changes.
- Review the inherited MSIX script's staging-path deletion before enabling it.
- Preserve the archived build trees until their junctions and contents can be
  reviewed for safe cleanup; no cleanup is required to resume the fresh build.
- Record remaining non-Windows desktop/package identities before claiming
  cross-platform product support.

Use [RELEASE_ACCEPTANCE.md](RELEASE_ACCEPTANCE.md) for candidate testing and
[UPSTREAM_SYNC.md](UPSTREAM_SYNC.md) for integration of reviewed updates.

Deferred: AI integration, manufacturing-system integration, and unverified
printer/material presets. Public distribution requires explicit approval.
