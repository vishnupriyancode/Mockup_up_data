@echo off
title Consolidated Mock Data Generator
color 0A

:menu
cls
echo ========================================
echo     CONSOLIDATED MOCK DATA GENERATOR
echo ========================================
echo.
echo Choose an option:
echo.
echo 1. Generate All Scenarios (All Models)
echo 2. Generate Positive Scenarios
echo 3. Generate Negative Scenarios  
echo 4. Generate Exclusion Scenarios
echo 5. Generate WGS Format Scenarios
echo 6. Generate Combined Output
echo 7. Generate Project Report
echo 8. List Available Models
echo 9. Help
echo 0. Exit
echo.
echo ========================================
set /p choice="Enter your choice (0-9): "

if "%choice%"=="1" goto all_scenarios
if "%choice%"=="2" goto positive_scenarios
if "%choice%"=="3" goto negative_scenarios
if "%choice%"=="4" goto exclusion_scenarios
if "%choice%"=="5" goto wgs_scenarios
if "%choice%"=="6" goto combined_output
if "%choice%"=="7" goto project_report
if "%choice%"=="8" goto list_models
if "%choice%"=="9" goto help
if "%choice%"=="0" goto exit
goto invalid_choice

:all_scenarios
cls
echo ========================================
echo    GENERATING ALL SCENARIOS
echo ========================================
echo.
set /p wgs="Use WGS format? (y/n): "
set /p count="Number of records (1-10, default 1): "
set /p split="Generate separate files? (y/n): "

if "%wgs%"=="y" (
    if "%split%"=="y" (
        python src/mockgen/consolidated_generator.py --all --wgs --count %count% --split
    ) else (
        python src/mockgen/consolidated_generator.py --all --wgs --count %count%
    )
) else (
    if "%split%"=="y" (
        python src/mockgen/consolidated_generator.py --all --count %count% --split
    ) else (
        python src/mockgen/consolidated_generator.py --all --count %count%
    )
)
pause
goto menu

:positive_scenarios
cls
echo ========================================
echo    GENERATING POSITIVE SCENARIOS
echo ========================================
echo.
set /p model="Model name (or press Enter for all): "
set /p wgs="Use WGS format? (y/n): "
set /p count="Number of records (1-10, default 1): "
set /p split="Generate separate files? (y/n): "

if "%model%"=="" (
    if "%wgs%"=="y" (
        if "%split%"=="y" (
            python src/mockgen/consolidated_generator.py --positive --wgs --count %count% --split
        ) else (
            python src/mockgen/consolidated_generator.py --positive --wgs --count %count%
        )
    ) else (
        if "%split%"=="y" (
            python src/mockgen/consolidated_generator.py --positive --count %count% --split
        ) else (
            python src/mockgen/consolidated_generator.py --positive --count %count%
        )
    )
) else (
    if "%wgs%"=="y" (
        if "%split%"=="y" (
            python src/mockgen/consolidated_generator.py --positive --model %model% --wgs --count %count% --split
        ) else (
            python src/mockgen/consolidated_generator.py --positive --model %model% --wgs --count %count%
        )
    ) else (
        if "%split%"=="y" (
            python src/mockgen/consolidated_generator.py --positive --model %model% --count %count% --split
        ) else (
            python src/mockgen/consolidated_generator.py --positive --model %model% --count %count%
        )
    )
)
pause
goto menu

:negative_scenarios
cls
echo ========================================
echo    GENERATING NEGATIVE SCENARIOS
echo ========================================
echo.
set /p model="Model name (or press Enter for all): "
set /p wgs="Use WGS format? (y/n): "
set /p count="Number of records (1-10, default 1): "
set /p split="Generate separate files? (y/n): "

if "%model%"=="" (
    if "%wgs%"=="y" (
        if "%split%"=="y" (
            python src/mockgen/consolidated_generator.py --negative --wgs --count %count% --split
        ) else (
            python src/mockgen/consolidated_generator.py --negative --wgs --count %count%
        )
    ) else (
        if "%split%"=="y" (
            python src/mockgen/consolidated_generator.py --negative --count %count% --split
        ) else (
            python src/mockgen/consolidated_generator.py --negative --count %count%
        )
    )
) else (
    if "%wgs%"=="y" (
        if "%split%"=="y" (
            python src/mockgen/consolidated_generator.py --negative --model %model% --wgs --count %count% --split
        ) else (
            python src/mockgen/consolidated_generator.py --negative --model %model% --wgs --count %count%
        )
    ) else (
        if "%split%"=="y" (
            python src/mockgen/consolidated_generator.py --negative --model %model% --count %count% --split
        ) else (
            python src/mockgen/consolidated_generator.py --negative --model %model% --count %count%
        )
    )
)
pause
goto menu

:exclusion_scenarios
cls
echo ========================================
echo    GENERATING EXCLUSION SCENARIOS
echo ========================================
echo.
set /p model="Model name (or press Enter for all): "
set /p wgs="Use WGS format? (y/n): "
set /p count="Number of records (1-10, default 1): "
set /p split="Generate separate files? (y/n): "

if "%model%"=="" (
    if "%wgs%"=="y" (
        if "%split%"=="y" (
            python src/mockgen/consolidated_generator.py --exclusion --wgs --count %count% --split
        ) else (
            python src/mockgen/consolidated_generator.py --exclusion --wgs --count %count%
        )
    ) else (
        if "%split%"=="y" (
            python src/mockgen/consolidated_generator.py --exclusion --count %count% --split
        ) else (
            python src/mockgen/consolidated_generator.py --exclusion --count %count%
        )
    )
) else (
    if "%wgs%"=="y" (
        if "%split%"=="y" (
            python src/mockgen/consolidated_generator.py --exclusion --model %model% --wgs --count %count% --split
        ) else (
            python src/mockgen/consolidated_generator.py --exclusion --model %model% --wgs --count %count%
        )
    ) else (
        if "%split%"=="y" (
            python src/mockgen/consolidated_generator.py --exclusion --model %model% --count %count% --split
        ) else (
            python src/mockgen/consolidated_generator.py --exclusion --model %model% --count %count%
        )
    )
)
pause
goto menu

:wgs_scenarios
cls
echo ========================================
echo    GENERATING WGS FORMAT SCENARIOS
echo ========================================
echo.
set /p scenario="Scenario type (positive/negative/exclusion): "
set /p model="Model name (or press Enter for all): "
set /p count="Number of records (1-10, default 1): "
set /p split="Generate separate files? (y/n): "

if "%model%"=="" (
    if "%split%"=="y" (
        python src/mockgen/consolidated_generator.py --%scenario% --wgs --count %count% --split
    ) else (
        python src/mockgen/consolidated_generator.py --%scenario% --wgs --count %count%
    )
) else (
    if "%split%"=="y" (
        python src/mockgen/consolidated_generator.py --%scenario% --model %model% --wgs --count %count% --split
    ) else (
        python src/mockgen/consolidated_generator.py --%scenario% --model %model% --wgs --count %count%
    )
)
pause
goto menu

:combined_output
cls
echo ========================================
echo    GENERATING COMBINED OUTPUT
echo ========================================
echo.
set /p wgs="Use WGS format? (y/n): "

if "%wgs%"=="y" (
    python src/mockgen/consolidated_generator.py --combined --wgs
) else (
    python src/mockgen/consolidated_generator.py --combined
)
pause
goto menu

:project_report
cls
echo ========================================
echo    GENERATING PROJECT REPORT
echo ========================================
echo.
python src/mockgen/consolidated_generator.py --report
pause
goto menu

:list_models
cls
echo ========================================
echo    LISTING AVAILABLE MODELS
echo ========================================
echo.
python src/mockgen/consolidated_generator.py --list
pause
goto menu

:help
cls
echo ========================================
echo              HELP
echo ========================================
echo.
echo This tool consolidates all mock data generation functionality:
echo.
echo - All scenario types (positive, negative, exclusion)
echo - WGS format support
echo - Multiple record generation
echo - Split file generation
echo - Combined output generation
echo - Project reporting
echo.
echo Files generated will be saved in the 'generated_outputs' directory.
echo.
echo For more detailed help, run: python src/mockgen/consolidated_generator.py --help
echo.
pause
goto menu

:invalid_choice
echo.
echo Invalid choice! Please enter a number between 0 and 9.
pause
goto menu

:exit
echo.
echo Thank you for using the Consolidated Mock Data Generator!
echo.
pause
exit
