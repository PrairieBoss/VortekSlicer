# Draft: establish isolated VortekSlicer product and package identity

Target: synchronized `main` after upstream synchronization PR #2 is merged.
Source branch: `codex/vortek-product-identity`.
Do not open against the obsolete main baseline or merge automatically.

VortekSlicer previously shared OrcaSlicer's product name, configuration key,
Windows associations, credential service and installer identity. The fork now
uses its own identities while retaining upstream binary names, profile/project
formats, translation catalogs, licenses and attribution.

Generated identity drives native captions, splash/About text, Windows metadata,
normal/portable/viewer configuration, model ProgIDs, credential service and
CPack/NSIS metadata. Association changes verify ownership and decline failed or
truncated executable paths. Portable discovery ignores a same-named regular
file. The fork avoids upstream protocol takeover and normal installer-update
checks; inherited MSIX staging is blocked before changes. Support/diagnostic
links identify the fork. The web welcome page applies the native name to two
translated text nodes, preserving all 15 locale dictionaries and navigation.

Separate corrections preserve redirected Windows CLI streams and retain
upstream generated G-code headers for configuration import. Build corrections
bound CPython's inner project parallelism and allow verified offline wx source
exports while preserving the normal upstream checkout. The existing Windows
workflow runs focused checks and uses product-aware artifact names.

Validation:

- All 32 Windows dependency targets completed successfully with VS2022.
  Local PDB workarounds, verified caches, exact wx commit/submodules, WebView2
  archive hash and commands are documented in WINDOWS_BUILD.md and the cache
  provenance record; a clean-checkout build has not been established.
- Fourteen focused identity/native/resource tests pass with VS2022. The full
  changed Config test file passed MSVC syntax checking; execution is pending.
- The current extracted Windows CI step passed locally with VS2026: 23 tests
  across identity, Python/wx configuration, console handling and welcome JS.
  This is not a hosted CI result.
- Staged Python 3.12.13 passed selected isolated runtime checks. OpenSSL/OpenCV
  installed-library probes, actual wx path resolution, WebView2 detection and
  the launcher's OpenGL >=3.3 probe passed independently of the application.

The product application is still compiling with GUI/CAD/tests enabled and
SLIC3R_MSVC_PDB=OFF. No current product executable, GUI workflow, slicing/export,
project round trip, live association/credential behavior, installer operation
or clean-machine deployment is claimed. The optional pinned uv package
installer is unavailable through current execution DNS. Existing upstream
icons/splash remain until verified Vortek assets are selected. There is no
automatic account/configuration migration; cloud callbacks and provider upgrade
handling still need runtime acceptance. Public release is outside this PR.

The earlier profile-tool correction, build changes and product changes remain
separate commits. Review them independently after normal upstream integration;
do not squash or bypass the synchronization history.
