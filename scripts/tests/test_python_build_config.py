"""Configure the real Python dependency recipe without building dependencies."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class TestPythonBuildConfig(unittest.TestCase):
    def test_windows_python_preserves_explicit_project_parallelism(self):
        for limit in (None, "", "1", "2"):
            with self.subTest(limit=limit), tempfile.TemporaryDirectory() as directory:
                work = Path(directory)
                script = work / "configure.cmake"
                script.write_text(f'''
set(WIN32 TRUE)
set(MSVC_VERSION 1944)
set(CMAKE_SYSTEM_PROCESSOR AMD64)
set(CMAKE_SIZEOF_VOID_P 8)
function(ExternalProject_Add name)
    file(WRITE "${{CMAKE_CURRENT_BINARY_DIR}}/external-args.txt" "${{ARGN}}")
endfunction()
include("{ROOT.as_posix()}/deps/python3/python3.cmake")
''', encoding="utf-8")
                environment = os.environ.copy()
                environment.pop("CMAKE_BUILD_PARALLEL_LEVEL", None)
                if limit is not None:
                    environment["CMAKE_BUILD_PARALLEL_LEVEL"] = limit
                result = subprocess.run(
                    [os.environ.get("CMAKE", "cmake"), "-P", str(script)],
                    cwd=work, env=environment, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                arguments = (work / "external-args.txt").read_text().split(";")
                command = arguments[arguments.index("BUILD_COMMAND") + 1:
                                    arguments.index("INSTALL_COMMAND")]
                if limit:
                    self.assertEqual(command[-2:], ["-M", "/m:" + limit])
                else:
                    self.assertNotIn("-M", command)
                    self.assertFalse(any(arg.startswith("/m:") for arg in command))
                # Parallelism must not disable modules or change release ABI.
                self.assertIn("--no-tkinter", command)
                self.assertNotIn("--no-ssl", command)
                self.assertNotIn("--no-ctypes", command)
                self.assertEqual(command[command.index("-c") + 1], "Release")


if __name__ == "__main__":
    unittest.main()
