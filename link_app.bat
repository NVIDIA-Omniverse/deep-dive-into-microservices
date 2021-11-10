@echo off

@REM Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
@REM
@REM NVIDIA CORPORATION and its licensors retain all intellectual property
@REM and proprietary rights in and to this software, related documentation
@REM and any modifications thereto.  Any use, reproduction, disclosure or
@REM distribution of this software and related documentation without an express
@REM license agreement from NVIDIA CORPORATION is strictly prohibited.

call "%~dp0tools\packman\python.bat" %~dp0tools\scripts\link_app.py %*
if %errorlevel% neq 0 ( goto Error )

:Success
exit /b 0

:Error
exit /b %errorlevel%
