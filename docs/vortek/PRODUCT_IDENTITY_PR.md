# Draft: establish isolated VortekSlicer product and package identity

Target: synchronized `main` after upstream synchronization PR #2 is merged.
Source branch: `codex/vortek-product-identity`.
Do not open against the obsolete main baseline or merge automatically.

VortekSlicer previously used OrcaSlicer's application-data key, Windows
associations, credentials namespace, and installer identity. This change
introduces a separate product identity while retaining upstream build targets,
launcher/DLL names, profiles, translation catalogs, and attribution.

The fork now supplies its name and vendor to generated resources and GUI
captions. Normal and portable configuration, model-file ProgIDs, credential
storage, and package upgrade identities are separated from OrcaSlicer.
Association changes also stop when executable-path lookup fails or truncates,
and portable discovery preserves a same-named regular file. Removing an
association checks its current owner; automatic upstream URL
protocol takeover is prevented. The existing MSIX script fails before staging
a fork under OrcaSlicer's publisher/Store identity.
Diagnostic/support links and archive names identify the fork. Existing Windows
CI uses product-aware installer/artifact names, skips upstream-only MSIX, and
runs the focused native tests in its build-script check job.

Validation: twelve focused tests pass with VS2022 and Windows SDK active. They
include generated identity/resource checks, C++ compile/run probes, mocked
registry ownership/error cases, Windows resource compilation, x64/ARM64 CPack
configuration, the MSIX early-failure staging-preservation check, and actual
startup/config-file selection code with isolated filesystem fixtures.
`git diff --check` passes.
The earlier extracted CI batch step passed locally with the installed VS2026
toolchain: eleven identity checks and the Python build fixture. The current
twelve-test identity suite passed with VS2022 after the later path-safety fixes.
The PowerShell package-variable step passed four product/architecture fixtures.
No GitHub workflow run has validated these changes yet.
The combined script suite ran 274 tests with VS2022 active: 273 passed and
one existing developer-local Bambu clone test was skipped (146.812 seconds).
An isolated later Windows build correction propagates an explicit CMake project
limit to bundled Python's nested MSBuild. Its separate four-case configuration
test passed. Keep that build fix independently reviewable from branding.

The product identity changes are **implemented but not runtime-validated**. The
fresh dependency build progressed after recovering a hash-verified Assimp
archive; all 27 generated archive pins are now cached and verified, but the full
dependency build is still incomplete. OpenSSL and CURL passed after a documented
local `/Z7`/generated-install-rule workaround for OpenSSL's PDB stall. No GUI/slicing,
live registry/credential behavior, installer operation, or clean-machine test
has been claimed. Upstream CI evidence predates this product code.
Six secondary CPython archives also passed complete official Git-tree/content
verification, and its actual bootstrap script used that cache without downloads.
The archive provenance record distinguishes those checks from upstream-supplied
SHA-256 pins. Bundled Python 3.12.13 has now compiled/staged with a scoped `/Z7`
workaround and passed selected runtime checks; OpenCV passed an installed-library
probe. The optional offline wx source recipe passed three CMake tests, and its
recovered source tree/submodules and WebView2 SDK passed provenance verification.
All 32 dependency targets have completed successfully, including wx and wxInspector.
The application build has started with GUI/CAD/tests enabled and the documented
PDB option disabled; it has no completion result yet. The optional uv installer
is unavailable due to execution DNS.

Existing upstream icons/splash graphics remain until verified Vortek assets
are available. The normal updater entry point is guarded from requesting upstream installers.
Provider-directed forced upgrades and browser cloud-login callback behavior
remain release-review items. There is no automatic configuration/account migration,
and MSIX remains disabled for the fork. Public release is outside this PR.

The earlier profile-tool correction and build records remain separate commits
in this branch's ancestry. Review those independently or split them into a
preceding validation PR after synchronization; do not squash upstream history.
