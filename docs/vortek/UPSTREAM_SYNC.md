# Maintaining the upstream baseline

PR #2 carries synchronization commit
`04684c58f935fc5beaba4d5959dcd7741c6a22d1`, matching the tree of upstream
`8d69fa3e5a9d5424899b0f9c2aaceb4af61c2c38`. It is still unmerged in the
latest recorded check. Until it is merged, base product development on that
verified synchronization history, as the current feature branch does.
Do not recreate product work from the older main or merge historical PR #1
unchanged.

## Integrating the pending work

Restore repository write authentication first. Recheck PR #2's exact source
and destination commits, required checks, mergeability and review state. Use a
normal merge preserving the synchronization history; do not squash or rewrite
shared commits to work around authentication. Verify the merged result before
updating local main:

```powershell
git status --short
git fetch origin
git switch main
git merge --ff-only origin/main
git merge-base --is-ancestor 04684c58f935fc5beaba4d5959dcd7741c6a22d1 HEAD
```

Start these commands only from a clean working tree. If the ancestry check
fails, inspect the actual merge instead of forcing/resetting main. Switch back
to `codex/vortek-product-identity` for the saved product changes. Push preserved
branches and open reviewable PRs against the synchronized main. Keep the
profile-tool correction independently reviewable from product identity.
Do not automatically merge product changes without the required validation.

## Later upstream updates

With a clean working tree and synchronized main, prepare each later update on
a fresh integration branch:

```powershell
git remote -v
git fetch origin
git fetch upstream
git switch -c codex/upstream-sync-YYYYMMDD origin/main
git merge --no-ff upstream/main
```

Confirm `upstream` still names the official OrcaSlicer repository and record
the exact fetched upstream commit. Resolve conflicts narrowly, inspect the
diff and run checks appropriate to the updated subsystems. Preserve upstream
licenses, attribution, profiles and project-format compatibility. Never
silently replace fork identities with upstream data/package/update identities.

In particular inspect changes to `version.inc`, generated identity/resources,
GUI startup/config paths, credentials, Windows shell integration, translation
catalog names, CPack, MSIX, and Windows CI artifact handling. Keep executable
contract and upstream compatibility identifiers separate from product-facing
labels. Re-run focused identity/resource/package checks and the full Windows
build/test workflow when dependencies permit; then perform the relevant
[release acceptance](RELEASE_ACCEPTANCE.md) checks on the resulting executable.

Open a synchronization PR with exact baseline/head commits, conflict decisions,
test results and known limitations. Merge through normal GitHub review; never
force-push or bypass main when write access is unavailable. Update the
authoritative status/backlog after integration. Download-cache provenance and
old local binaries are not validation of the new source.
