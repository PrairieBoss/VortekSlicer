# Project Structure

VortekSlicer retains OrcaSlicer's upstream monorepo layout. This is an intentional compatibility decision.

The 2026-08-05 clean Windows build validated this layout without moving upstream files or adding Vortek-only build wrappers. The only fork-baseline additions are the maintained documents in `docs/`.

```text
VortekSlicer/
├── .github/          GitHub Actions and repository templates
├── cmake/            Shared CMake modules
├── deps/             Pinned external dependency superbuild
├── deps_src/         In-tree third-party and adapted dependency sources
├── docs/             VortekSlicer build and maintenance documentation
├── localization/     Translation sources and generated localization inputs
├── resources/        Profiles, images, configuration, and runtime assets
├── scripts/          Cross-platform build, packaging, and maintenance scripts
├── src/              OrcaSlicer/VortekSlicer application and libraries
├── tests/            Test suites
├── tools/            Small tools bundled by upstream
├── CMakeLists.txt    Main application configuration
└── build_release_vs.bat
```

Generated paths are not project structure and must not be committed:

```text
build/
build-dbg/
build-dbginfo/
deps/build/
deps/build-dbg/
deps/build-dbginfo/
deps/DL_CACHE/
```

## Why there is no nested `upstream/`

Placing the complete OrcaSlicer repository under `upstream/` would require moving thousands of upstream paths and rewriting build/CI assumptions. It would turn routine upstream merges into structural conflicts without improving runtime architecture.

The Git remote already represents upstream cleanly:

```text
origin   PrairieBoss/VortekSlicer
upstream SoftFever/OrcaSlicer
```

## Future Vortek-specific directories

Add directories only when they contain maintained artifacts:

- `branding/` may be added for source branding assets and licensing records.
- `patches/` may be added only if external source patches cannot be represented cleanly as Git commits or CMake patch files near their dependency definitions.
- Vortek runtime resources should normally follow the existing `resources/` conventions.
- Vortek application code should normally remain under the existing `src/` target hierarchy.

Each addition must document ownership, generation steps, licensing, and upstream merge implications.
