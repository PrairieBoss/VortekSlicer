"""Dependency-free configuration checks and small MSVC probes for fork identity.

Run with the VS2022 compiler on PATH to include the native probes. No test
opens the real registry, credential store, or user configuration directories.
"""

import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]


class TestProductIdentity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="vortek_identity_")
        cls.work = Path(cls.temp.name)
        cls.addClassCleanup(cls.temp.cleanup)
        source = ROOT.as_posix()
        script = cls.work / "configure.cmake"
        script.write_text(f'''
include("{source}/version.inc")
set(SLIC3R_BUILD_ID "identity-test")
set(ORCA_CHECK_GCODE_PLACEHOLDERS 0)
set(SLIC3R_RESOURCES_DIR "{source}/resources")
configure_file("{source}/src/libslic3r/libslic3r_version.h.in"
               "${{CMAKE_CURRENT_LIST_DIR}}/libslic3r_version.h" @ONLY)
configure_file("{source}/src/dev-utils/platform/msw/OrcaSlicer.rc.in"
               "${{CMAKE_CURRENT_LIST_DIR}}/OrcaSlicer.rc" @ONLY)
configure_file("{source}/src/dev-utils/platform/msw/OrcaSlicer.manifest.in"
               "${{CMAKE_CURRENT_LIST_DIR}}/OrcaSlicer.manifest" @ONLY)
''', encoding="utf-8")
        subprocess.run([os.environ.get("CMAKE", "cmake"), "-P", str(script)],
                       cwd=cls.work, check=True, capture_output=True, text=True)

    def compile_and_run(self, name, source):
        path = self.work / (name + ".cpp")
        path.write_text(source, encoding="utf-8")
        result = subprocess.run(
            ["cl", "/nologo", "/std:c++17", "/EHsc", str(path),
             "/Fe:" + str(self.work / (name + ".exe")),
             "/Fo:" + str(self.work / (name + ".obj"))],
            cwd=self.work, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        result = subprocess.run([str(self.work / (name + ".exe"))],
                                cwd=self.work, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_generated_resources_have_no_unexpanded_variables(self):
        for name in ("libslic3r_version.h", "OrcaSlicer.rc", "OrcaSlicer.manifest"):
            with self.subTest(resource=name):
                self.assertNotRegex((self.work / name).read_text(), r"@[A-Za-z_]+@")

    def test_windows_manifest_names_the_fork_and_preserves_privileges(self):
        root = ET.parse(self.work / "OrcaSlicer.manifest").getroot()
        ns = {"a": "urn:schemas-microsoft-com:asm.v1",
              "v3": "urn:schemas-microsoft-com:asm.v3"}
        self.assertEqual(root.find("a:assemblyIdentity", ns).get("name"), "VortekSlicer")
        self.assertEqual(root.find("a:description", ns).text, "VortekSlicer")
        privileges = root.find(".//v3:requestedExecutionLevel", ns)
        self.assertEqual(privileges.get("level"), "asInvoker")
        self.assertEqual(privileges.get("uiAccess"), "false")

    def test_windows_metadata_preserves_the_existing_binary_contract(self):
        resource = (self.work / "OrcaSlicer.rc").read_text()
        self.assertIn('VALUE "CompanyName", "Vortek Manufacturing"', resource)
        self.assertIn('VALUE "ProductName", "VortekSlicer"', resource)
        self.assertIn('VALUE "OriginalFilename", "orca-slicer.exe"', resource)
        self.assertIn('/images/OrcaSlicer.ico"', resource)

    def test_cpack_generates_separate_installer_identity_for_both_architectures(self):
        source = ROOT.as_posix()
        upgrade_ids = []
        for architecture in ("x64", "ARM64"):
            with self.subTest(architecture=architecture):
                fixture = self.work / architecture
                fixture.mkdir()
                (fixture / "CMakeLists.txt").write_text(f'''
cmake_minimum_required(VERSION 3.13)
project(IdentityPackage NONE)
include("{source}/version.inc")
set(WIN32 TRUE)
set(CMAKE_SYSTEM_PROCESSOR "{architecture}")
set(CPACK_PACKAGE_VERSION "${{ORCA_VERSION_MAJOR}}.${{ORCA_VERSION_MINOR}}.${{ORCA_VERSION_PATCH}}")
set(CPACK_RESOURCE_FILE_LICENSE "{source}/LICENSE.txt")
include("{source}/cmake/VortekPackaging.cmake")
include(CPack)
''', encoding="utf-8")
                result = subprocess.run(
                    [os.environ.get("CMAKE", "cmake"), "-S", str(fixture),
                     "-B", str(fixture / "build")], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                config = (fixture / "build/CPackConfig.cmake").read_text()
                values = dict(re.findall(r'set\((CPACK_\w+) "([^"\n]*)"\)', config))
                for key in ("CPACK_PACKAGE_NAME", "CPACK_PACKAGE_INSTALL_DIRECTORY",
                            "CPACK_PACKAGE_INSTALL_REGISTRY_KEY", "CPACK_NSIS_DISPLAY_NAME"):
                    self.assertEqual(values[key], "VortekSlicer", key)
                self.assertEqual(values["CPACK_PACKAGE_VENDOR"], "Vortek Manufacturing")
                self.assertEqual(values["CPACK_PACKAGE_EXECUTABLES"], "orca-slicer;VortekSlicer")
                self.assertTrue(values["CPACK_PACKAGE_FILE_NAME"].endswith("_" + architecture.lower()))
                self.assertTrue(values["CPACK_RESOURCE_FILE_LICENSE"].endswith("/LICENSE.txt"))
                self.assertNotEqual(values["CPACK_WIX_UPGRADE_GUID"].lower(),
                                    "058245e8-20e0-4a95-9ab7-1acfe17ad511")
                upgrade_ids.append(values["CPACK_WIX_UPGRADE_GUID"])
        self.assertEqual(upgrade_ids[0], upgrade_ids[1])

    @unittest.skipUnless(shutil.which("powershell.exe"), "Windows PowerShell not available")
    def test_msix_refuses_upstream_identity_before_changing_staging(self):
        staging = self.work / "existing-staging"
        staging.mkdir()
        sentinel = staging / "keep.txt"
        sentinel.write_text("preserve existing staging", encoding="utf-8")
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
             str(ROOT / "scripts/msix/build_msix.ps1"), "-StageOnly", "-StagingDir", str(staging)],
            cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MSIX identity and assets are not configured for this fork", result.stdout + result.stderr)
        self.assertEqual(sentinel.read_text(), "preserve existing staging")

    @unittest.skipUnless(shutil.which("cl"), "MSVC developer environment not active")
    def test_compiled_identity_separates_data_and_preserves_catalogs(self):
        self.compile_and_run("identity", r'''
#include "libslic3r_version.h"
#include <string_view>
using namespace std::literals;
static_assert(SLIC3R_APP_NAME == "VortekSlicer"sv);
static_assert(SLIC3R_APP_FULL_NAME == "VortekSlicer"sv);
static_assert(SLIC3R_APP_KEY == "VortekSlicer"sv);
static_assert(GCODEVIEWER_APP_NAME == "VortekSlicer G-code Viewer"sv);
static_assert(GCODEVIEWER_APP_KEY == "VortekSlicerGcodeViewer"sv);
static_assert(SLIC3R_PORTABLE_DATA_DIR == "VortekSlicer-data"sv);
static_assert(SLIC3R_PROJECT_PROG_ID == "VortekSlicer.Project.1"sv);
static_assert(SLIC3R_SECRET_STORE_SERVICE == "VortekSlicer/Auth"sv);
static_assert(SLIC3R_TRANSLATION_DOMAIN == "OrcaSlicer"sv);
int main() { return 0; }
''')

    @unittest.skipUnless(shutil.which("rc"), "Windows SDK developer environment not active")
    def test_windows_resource_compiles(self):
        result = subprocess.run(["rc", "/nologo", "/fo", "identity.res", "OrcaSlicer.rc"],
                                cwd=self.work, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertGreater((self.work / "identity.res").stat().st_size, 0)

    @unittest.skipUnless(shutil.which("cl"), "MSVC developer environment not active")
    def test_disassociation_preserves_foreign_registry_values(self):
        # Compile the actual production helper against fake Win32 calls. This
        # exercises ownership and failure paths without changing HKCU/HKLM.
        source = (ROOT / "src/slic3r/GUI/GUI_App.cpp").read_text(encoding="utf-8")
        begin = source.index("static bool del_win_registry(")
        end = source.index("\n#endif", begin)
        helper = source[begin:end]
        begin = source.index("bool is_associate_files(std::wstring extend)")
        end = source.index("\n#endif", begin)
        association_query = source[begin:end]
        self.compile_and_run("registry_ownership", r'''
#include "libslic3r_version.h"
#include <cwchar>
#include <cstring>
#include <string>
#include <iostream>
using HKEY = int;
using DWORD = unsigned long;
constexpr int ERROR_SUCCESS = 0, ERROR_FILE_NOT_FOUND = 2, ERROR_ACCESS_DENIED = 5;
constexpr DWORD REG_SZ = 1, REG_DWORD = 4, RRF_RT_ANY = 0;
constexpr HKEY HKEY_CURRENT_USER = 1;
namespace boost { namespace nowide {
std::wstring widen(const char* text) { return std::wstring(text, text + std::strlen(text)); }
} }
static int read_result = ERROR_SUCCESS, delete_result = ERROR_SUCCESS;
static DWORD stored_type = REG_SZ;
static std::wstring stored_value;
static unsigned deletes = 0;
int RegGetValueW(HKEY, const wchar_t*, const wchar_t*, DWORD, DWORD* type,
                 wchar_t* buffer, DWORD*) {
    *type = stored_type;
    std::wcscpy(buffer, stored_value.c_str());
    return read_result;
}
int RegDeleteKeyExW(HKEY, const wchar_t*, DWORD view, DWORD reserved) {
    ++deletes;
    if (view != 0 || reserved != 0) return ERROR_ACCESS_DENIED;
    return delete_result;
}
''' + helper + association_query + r'''
int main() {
    const wchar_t* expected = L"VortekSlicer.Project.1";
    stored_value = L" Orca.Slicer.1";
    if (del_win_registry(0, L"test", expected) || deletes != 0) return 1;
    stored_value = expected;
    stored_type = REG_DWORD;
    if (del_win_registry(0, L"test", expected) || deletes != 0) return 2;
    stored_type = REG_SZ;
    read_result = ERROR_FILE_NOT_FOUND;
    if (del_win_registry(0, L"test", expected) || deletes != 0) return 3;
    read_result = ERROR_ACCESS_DENIED;
    if (del_win_registry(0, L"test", expected) || deletes != 0) return 4;
    read_result = ERROR_SUCCESS;
    delete_result = ERROR_ACCESS_DENIED;
    if (del_win_registry(0, L"test", expected) || deletes != 1) return 5;
    delete_result = ERROR_SUCCESS;
    if (!del_win_registry(0, L"test", expected) || deletes != 2) return 6;
    if (!is_associate_files(L"3mf")) return 7;
    stored_value = L" Orca.Slicer.1";
    if (is_associate_files(L"3mf")) return 8;
    stored_value = expected;
    stored_type = REG_DWORD;
    if (is_associate_files(L"3mf")) return 9;
    stored_type = REG_SZ;
    read_result = ERROR_ACCESS_DENIED;
    if (is_associate_files(L"3mf")) return 10;
    return 0;
}
''')

    @unittest.skipUnless(shutil.which("cl"), "MSVC developer environment not active")
    def test_protocol_removal_preserves_foreign_or_packaged_handlers(self):
        source = (ROOT / "src/slic3r/GUI/GUI_App.cpp").read_text(encoding="utf-8")
        begin = source.index("void GUI_App::disassociate_url(")
        end = source.index("void GUI_App::start_download(", begin)
        helper = source[begin:end]
        self.compile_and_run("protocol_ownership", r'''
#include <string>
#define WIN32 1
static bool packaged = false, owned = false, exists = true;
static unsigned writes = 0;
bool is_running_in_msix() { return packaged; }
struct wxRegKey {
    enum { HKCU };
    wxRegKey(int, const std::wstring&) {}
    bool Exists() { return exists; }
    void operator=(const char*) { ++writes; }
};
struct GUI_App {
    bool check_url_association(std::wstring, std::wstring&) { return owned; }
    void disassociate_url(std::wstring);
};
''' + helper + r'''
int main() {
    GUI_App app;
    app.disassociate_url(L"orcaslicer");
    if (writes != 0) return 1;
    owned = true;
    packaged = true;
    app.disassociate_url(L"orcaslicer");
    if (writes != 0) return 2;
    packaged = false;
    exists = false;
    app.disassociate_url(L"orcaslicer");
    if (writes != 0) return 3;
    exists = true;
    app.disassociate_url(L"orcaslicer");
    if (writes != 1) return 4;
    return 0;
}
''')


if __name__ == "__main__":
    unittest.main()
