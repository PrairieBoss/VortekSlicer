# Runs the real orca-slicer binary, so it needs the built app and resources/, not just build/tests.
# The CI unit-test job only receives build/tests, so the test carries the RequiresApp label that
# scripts/run_unit_tests.sh excludes. Run it with `ctest -C Release -L RequiresApp`. It also exits 77
# (skipped) when the binary is missing.

# Windows uses a Python-only smoke test; the existing Linux checks need bash
# and Linux-only result.json output.
find_program(ORCA_CLI_TEST_PYTHON NAMES python3 python)
if (NOT ORCA_CLI_TEST_PYTHON)
    message(STATUS "python3 not found, not registering the CLI tests")
    return()
endif ()

if (WIN32)
    add_test(NAME cli_roundtrip
        COMMAND "${ORCA_CLI_TEST_PYTHON}" "${CMAKE_CURRENT_SOURCE_DIR}/test_cli_roundtrip.py"
            --binary $<TARGET_FILE:OrcaSlicer>
            --source-root "${CMAKE_SOURCE_DIR}"
            --work-root "${CMAKE_CURRENT_BINARY_DIR}"
            --app-key "${SLIC3R_APP_KEY}")
    set_tests_properties(cli_roundtrip PROPERTIES
        LABELS "CLI;RequiresApp"
        SKIP_RETURN_CODE 77
        TIMEOUT 960)
    return()
endif ()

add_test(NAME cli_strict_mode
    COMMAND bash ${CMAKE_CURRENT_SOURCE_DIR}/test_cli_strict.sh $<TARGET_FILE:OrcaSlicer> ${ORCA_CLI_TEST_PYTHON})
set_tests_properties(cli_strict_mode PROPERTIES
    LABELS "CLI;RequiresApp"
    SKIP_RETURN_CODE 77
    TIMEOUT 900)

add_test(NAME cli_project_missing_keys
    COMMAND bash ${CMAKE_CURRENT_SOURCE_DIR}/test_cli_project_missing_keys.sh $<TARGET_FILE:OrcaSlicer> ${ORCA_CLI_TEST_PYTHON}
        ${CMAKE_SOURCE_DIR}/resources/profiles/BBL)
set_tests_properties(cli_project_missing_keys PROPERTIES
    LABELS "CLI;RequiresApp"
    SKIP_RETURN_CODE 77
    TIMEOUT 900)
