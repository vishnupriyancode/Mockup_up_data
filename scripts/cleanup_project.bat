@echo off
title Project Cleanup Tool
color 0A

:menu
cls
echo ========================================
echo         PROJECT CLEANUP TOOL
echo ========================================
echo.
echo Choose cleanup option:
echo.
echo 1. Clean Old Duplicate Files
echo 2. Clean Old Reference Files
echo 3. Clean Old Validation Scripts
echo 4. Full Project Cleanup
echo 5. Exit
echo.
echo ========================================
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto clean_duplicates
if "%choice%"=="2" goto clean_references
if "%choice%"=="3" goto clean_validation
if "%choice%"=="4" goto full_cleanup
if "%choice%"=="5" goto exit
goto invalid_choice

:clean_duplicates
cls
echo ========================================
echo    CLEANING OLD DUPLICATE FILES
echo ========================================
echo.
echo This will remove old duplicate generation scripts
echo that have been replaced by consolidated_generator.bat
echo.
echo Files to be removed:
echo - Old .bat files (9 files)
echo - Old .py files (4 files)
echo - Old .md files (8 files)
echo.
echo Total: 21 files
echo.
set /p confirm="Proceed? (y/N): "
if /i not "%confirm%"=="y" goto menu

echo.
echo Starting duplicate cleanup...
echo.

REM Remove old batch files
del /q generate_all_scenarios.bat 2>nul
del /q generate_exclusion.bat 2>nul
del /q generate_negative.bat 2>nul
del /q generate_positive.bat 2>nul
del /q generate_wgs_all.bat 2>nul
del /q generate_wgs_combined.bat 2>nul
del /q generate_wgs_exclusion.bat 2>nul
del /q generate_wgs_negative.bat 2>nul
del /q generate_wgs_positive.bat 2>nul
del /q generate_wgs_positive_split.bat 2>nul

REM Remove old Python scripts
del /q generate_wgs_format.py 2>nul
del /q generate_separate_jsons.py 2>nul
del /q generate_output_json.py 2>nul
del /q create_project_report.py 2>nul

REM Remove old documentation
del /q USAGE_GUIDE.md 2>nul
del /q QUICK_START_COMMANDS.md 2>nul
del /q WGS_FORMAT_USAGE_GUIDE.md 2>nul
del /q SEPARATE_JSONS_USAGE.md 2>nul
del /q WGS_POSITIVE_SPLIT_COMMAND.md 2>nul
del /q WGS_SPLIT_PAYLOADS_SUMMARY.md 2>nul
del /q IMPLEMENTATION_SUMMARY.md 2>nul
del /q PROBLEM_ANALYSIS_AND_SOLUTION.md 2>nul

echo ✓ Duplicate cleanup completed
pause
goto menu

:clean_references
cls
echo ========================================
echo    CLEANING OLD REFERENCE FILES
echo ========================================
echo.
echo This will remove old reference files
echo that have been consolidated into MASTER_REFERENCE.md
echo.
echo Files to be removed:
echo - QUICK_REFERENCE.md
echo - QUICK_REFERENCE_CONSOLIDATED.md
echo - CONSOLIDATED_README.md
echo - MOCKGEN_CLI_README.md
echo - PROBABILITY_COMMANDS_QUICK_REFERENCE.md
echo.
set /p confirm="Proceed? (y/N): "
if /i not "%confirm%"=="y" goto menu

echo.
echo Starting reference cleanup...
echo.

del /q QUICK_REFERENCE.md 2>nul
del /q QUICK_REFERENCE_CONSOLIDATED.md 2>nul
del /q CONSOLIDATED_README.md 2>nul
del /q MOCKGEN_CLI_README.md 2>nul
del /q PROBABILITY_COMMANDS_QUICK_REFERENCE.md 2>nul

echo ✓ Reference cleanup completed
pause
goto menu

:clean_validation
cls
echo ========================================
echo    CLEANING OLD VALIDATION SCRIPTS
echo ========================================
echo.
echo This will remove old validation scripts
echo that have been consolidated into data_validation.py
echo.
echo Files to be removed:
echo - compare_scenarios.py
echo - verify_generation.py
echo - test_format_generation.py
echo.
set /p confirm="Proceed? (y/N): "
if /i not "%confirm%"=="y" goto menu

echo.
echo Starting validation cleanup...
echo.

del /q compare_scenarios.py 2>nul
del /q verify_generation.py 2>nul
del /q test_format_generation.py 2>nul

echo ✓ Validation cleanup completed
pause
goto menu

:full_cleanup
cls
echo ========================================
echo        FULL PROJECT CLEANUP
echo ========================================
echo.
echo This will perform ALL cleanup operations:
echo - Remove duplicate files
echo - Remove old references
echo - Remove old validation scripts
echo.
echo WARNING: This action cannot be undone!
echo.
set /p confirm="Proceed with full cleanup? (y/N): "
if /i not "%confirm%"=="y" goto menu

echo.
echo Starting full cleanup...
echo.

call :clean_duplicates
call :clean_references
call :clean_validation

echo.
echo ========================================
echo         FULL CLEANUP COMPLETE!
echo ========================================
echo.
echo Your project is now clean and organized!
echo.
echo Remaining essential files:
echo ✓ consolidated_generator.py
echo ✓ consolidated_generator.bat
echo ✓ MASTER_REFERENCE.md
echo ✓ user_input.json
echo ✓ master.json
echo ✓ requirements.txt
echo ✓ src/ directory
echo.
pause
goto menu

:invalid_choice
echo.
echo Invalid choice! Please enter a number between 1 and 5.
pause
goto menu

:exit
echo.
echo Thank you for using the Project Cleanup Tool!
echo.
pause
exit
