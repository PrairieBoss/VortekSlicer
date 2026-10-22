# VortekSlicer Windows release acceptance

No current candidate has passed this checklist. The recorded unit/static
checks do not establish these runtime results. Public release needs approval.
Use the exact reviewed source commit and record the Windows version, compiler,
architecture, input files and output hashes with every candidate.

## Build and package evidence

- Build all pinned dependencies, then run the documented Windows application
  build with `--run-tests -i`. Preserve logs and exit codes; identify any local
  dependency workaround separately from a clean-checkout result.
- Confirm the executable and DLL version metadata identify VortekSlicer and
  Vortek Manufacturing. Check x64 first; ARM64 needs its own build/runtime
  evidence. A configured ARM64 CPack fixture is not an ARM64 application build.
- Confirm the installed tree includes its required DLLs, Python runtime,
  translation catalogs, profiles, resources and `LICENSE.txt`.
- Generate an internal NSIS/portable candidate, record SHA-256 hashes, and
  inspect its actual file list. Do not use the inherited MSIX identity.
- Check on a disposable clean Windows environment with required runtime
  prerequisites. Do not install an untested candidate system-wide on this host.

## Identity and coexistence

- Inspect the main window, loaded-project title, splash version, About dialog,
  diagnostics, shortcuts, executable properties and installer captions.
  Existing upstream graphics are a known incomplete branding item until
  approved Vortek assets are available. Preserve upstream credits/licenses.
- Launch beside a normal OrcaSlicer installation with disposable configurations.
  Verify normal Vortek storage uses its own application-data directory and
  `VortekSlicer.conf`; presets, logs, caches, plugins and fallback credentials
  stay below the selected Vortek directory.
- Put an upstream `data_dir` fixture beside the executable: it must remain
  untouched. Add `VortekSlicer-data`: only that directory should be selected.
  Test `--datadir` with a separate explicit fixture. Never select production data.
- Verify separate credential-store service behavior without real accounts.
  Account import/migration is not supported or implicitly authorized.
- Exercise Windows file-association opt-in and removal. Preserve foreign
  ownership and an existing Orca protocol handler. Verify both apps can launch.
- Normal automatic/manual update checks must offer no Orca installer. Review
  provider-directed upgrade handling and cloud callbacks before enabling an
  account integration. Offline model preparation/slicing must remain usable.
- Test NSIS install/upgrade/uninstall in the disposable environment. Removing
  Vortek must leave Orca's installation, associations and user data intact.

## Core functional workflow

- Use a repository test cube and an existing supported upstream printer profile
  as test fixtures. Record profile identifiers; do not invent production settings.
- Start the GUI, complete first-run printer/filament/process selection, import
  an STL, transform it and prepare the plate without errors.
- Slice the model, inspect layer preview and export G-code. Verify the output
  contains expected nonempty layers, extrusion/toolpath content and the selected
  profile's expected temperature/start/end commands. Do not send it to a printer.
- Save a 3MF project, close/reopen it, and verify model placement and selected
  settings survive. Re-slice and compare meaningful results rather than timestamp
  or build-label differences. Exercise G-code viewing as a separate launch mode.
- Open a compatible OrcaSlicer 3MF copy and import/export preset copies. Confirm
  schema compatibility and preservation of the original fixture files.
- Repeat startup, import, slicing, preview, export and project round trip from
  the packaged candidate. Record crashes, missing resources and visual issues.

Release acceptance requires completed evidence for these workflows, unresolved
failures triaged, reviewed source, a reproducible build, and authorized
distribution. Physical printer operation is outside this checklist.
