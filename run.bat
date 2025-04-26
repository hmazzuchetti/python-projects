@echo off
echo Running Video Modification Bot with Poetry...
"C:\Users\henri\AppData\Roaming\Python\Scripts\poetry.exe" run python main.py
if %ERRORLEVEL% NEQ 0 (
    echo Falling back to regular Python...
    python main.py
)
pause