"""Configure the real wxWidgets recipe and exercise offline download steps."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
CMAKE = os.environ.get("CMAKE", "cmake")
REQUIRED = ("CMakeLists.txt", "include/wx/version.h",
            "3rdparty/catch/CMakeLists.txt", "3rdparty/pcre/CMakeLists.txt",
            "3rdparty/libwebp/CMakeLists.txt")


class TestWxWidgetsBuildConfig(unittest.TestCase):
    def configure(self, work, source=None):
        project = work / "project"
        project.mkdir()
        setting = (f'set(ORCA_WXWIDGETS_SOURCE_DIR "{source.as_posix()}" CACHE PATH "")'
                   if source else "")
        (project / "CMakeLists.txt").write_text(f'''
cmake_minimum_required(VERSION 3.20)
project(wx_source_fixture NONE)
include(ExternalProject)
function(orcaslicer_add_cmake_project name)
    ExternalProject_Add(dep_${{name}} ${{ARGN}}
        CONFIGURE_COMMAND "" BUILD_COMMAND "" INSTALL_COMMAND "")
endfunction()
{setting}
include("{ROOT.as_posix()}/deps/wxWidgets/wxWidgets.cmake")
ExternalProject_Add_StepTargets(dep_wxWidgets download update)
''', encoding="utf-8")
        build = work / "build"
        result = subprocess.run([CMAKE, "-S", str(project), "-B", str(build)],
                                capture_output=True, text=True)
        return result, build

    def test_default_preserves_upstream_git_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            result, build = self.configure(Path(directory))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            clone = next(build.rglob("dep_wxWidgets-gitclone.cmake")).read_text()
            self.assertIn("https://github.com/SoftFever/Orca-deps-wxWidgets", clone)
            self.assertIn('checkout "v3.3.2"', clone)
            for module in ("catch", "pcre", "libwebp"):
                self.assertIn("3rdparty/" + module, clone)
            self.assertNotIn("sslVerify=false", clone)

    def test_offline_source_has_no_download_or_update(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            source = work / "verified source with spaces"
            for name in REQUIRED:
                path = source / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# fixture\n", encoding="utf-8")
            sentinel = source / "preserve.txt"
            sentinel.write_text("unchanged", encoding="utf-8")
            result, build = self.configure(work, source)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(list(build.rglob("*-gitclone.cmake")))
            result = subprocess.run([CMAKE, "--build", str(build), "--target",
                                     "dep_wxWidgets-download", "dep_wxWidgets-update"],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(sentinel.read_text(), "unchanged")
            self.assertTrue(all((source / name).is_file() for name in REQUIRED))

    def test_incomplete_offline_tree_fails_before_build(self):
        for missing in REQUIRED:
            with self.subTest(missing=missing), tempfile.TemporaryDirectory() as directory:
                work = Path(directory)
                source = work / "incomplete"
                for name in REQUIRED:
                    if name == missing:
                        continue
                    path = source / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.touch()
                result, _ = self.configure(work, source)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Incomplete ORCA_WXWIDGETS_SOURCE_DIR", result.stdout + result.stderr)
                self.assertIn(missing, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
