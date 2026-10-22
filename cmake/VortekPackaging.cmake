# Fork-facing package identity; upstream targets, executable names and licenses
# remain unchanged so dependency and launcher contracts keep working.
set(CPACK_PACKAGE_NAME "${SLIC3R_APP_NAME}")
set(CPACK_PACKAGE_VENDOR "${SLIC3R_APP_VENDOR}")
set(CPACK_PACKAGE_INSTALL_DIRECTORY "${SLIC3R_APP_KEY}")
set(CPACK_PACKAGE_INSTALL_REGISTRY_KEY "${SLIC3R_APP_KEY}")
set(CPACK_PACKAGE_FILE_NAME "${SLIC3R_APP_NAME}_Windows_Installer_V${SoftFever_VERSION}")
if(WIN32)
    if(CMAKE_SYSTEM_PROCESSOR STREQUAL "ARM64")
        string(APPEND CPACK_PACKAGE_FILE_NAME "_arm64")
    else()
        string(APPEND CPACK_PACKAGE_FILE_NAME "_x64")
    endif()
endif()
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "VortekSlicer is a Vortek Manufacturing fork of OrcaSlicer for FDM printers")
set(CPACK_PACKAGE_HOMEPAGE_URL "${SLIC3R_APP_HOMEPAGE}")
set(CPACK_NSIS_DISPLAY_NAME "${SLIC3R_APP_NAME}")
set(CPACK_NSIS_PACKAGE_NAME "${SLIC3R_APP_NAME}")
set(CPACK_PACKAGE_EXECUTABLES "orca-slicer;${SLIC3R_APP_NAME}")
# Distinct from upstream's upgrade identity; never uninstall OrcaSlicer.
string(UUID CPACK_WIX_UPGRADE_GUID NAMESPACE 6ba7b811-9dad-11d1-80b4-00c04fd430c8
       NAME "https://github.com/PrairieBoss/VortekSlicer" TYPE SHA1 UPPER)
