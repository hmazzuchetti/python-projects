#!/usr/bin/env pwsh

# Run the video modification bot using Poetry
$PoetryPath = "C:\Users\henri\AppData\Roaming\Python\Scripts\poetry.exe"

if (Test-Path $PoetryPath) {
    Write-Host "Running main.py with Poetry..."
    & $PoetryPath run python main.py
} else {
    Write-Host "Poetry not found at $PoetryPath"
    Write-Host "Falling back to regular Python..."
    python main.py
}