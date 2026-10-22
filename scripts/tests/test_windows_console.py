"""Exercise the production Windows console helper with real CRT redirection."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(os.name == "nt" and shutil.which("cl"), "MSVC developer environment not active")
class TestWindowsConsole(unittest.TestCase):
    def test_cli_preserves_redirected_streams_with_or_without_a_console(self):
        source = (ROOT / "src/OrcaSlicer.cpp").read_text(encoding="utf-8")
        start = source.index("void attach_console_on_demand(){")
        end = source.index("void CLI::print_help(", start)
        # Only the boost stream clear calls are aliased; the production helper
        # uses real Windows console APIs and real CRT stdin/stdout/stderr.
        code = r'''
#include <windows.h>
#include <io.h>
#include <cstdio>
#include <iostream>
#include <string>
namespace boost { namespace nowide { using std::cout; using std::cerr; using std::cin; } }
''' + source[start:end] + r'''
int main(int argc, char**) {
    if (argc > 1) fclose(stderr); // Exercise a missing stream beside valid pipes.
    attach_console_on_demand();
    std::string input;
    std::getline(std::cin, input);
    std::cout << "stdout:" << input << std::endl;
    std::cerr << "stderr:preserved" << std::endl;
    return _fileno(stderr) >= 0 ? 0 : 1;
}
'''
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            (work / "console.cpp").write_text(code, encoding="utf-8")
            result = subprocess.run(["cl", "/nologo", "/EHsc", "/std:c++17",
                                     "console.cpp", "/Fe:console.exe"],
                                    cwd=work, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            hidden = subprocess.STARTUPINFO()
            hidden.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            hidden.wShowWindow = 0
            for flags in (subprocess.CREATE_NEW_CONSOLE, subprocess.CREATE_NO_WINDOW):
                with self.subTest(creationflags=flags):
                    result = subprocess.run([str(work / "console.exe")], input="pipe input\n",
                                            cwd=work, capture_output=True, text=True, timeout=15,
                                            startupinfo=hidden, creationflags=flags)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, "stdout:pipe input\n")
                    self.assertEqual(result.stderr, "stderr:preserved\n")
            with (work / "stdout.txt").open("w") as out, (work / "stderr.txt").open("w") as err:
                result = subprocess.run([str(work / "console.exe")], stdin=subprocess.DEVNULL,
                                        stdout=out, stderr=err, timeout=15, startupinfo=hidden,
                                        creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.assertEqual(result.returncode, 0)
            self.assertEqual((work / "stdout.txt").read_text(), "stdout:\n")
            self.assertEqual((work / "stderr.txt").read_text(), "stderr:preserved\n")
            result = subprocess.run([str(work / "console.exe"), "missing-stderr"],
                                    input="partial input\n", cwd=work, capture_output=True,
                                    text=True, timeout=15, startupinfo=hidden,
                                    creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "stdout:partial input\n")


if __name__ == "__main__":
    unittest.main()
