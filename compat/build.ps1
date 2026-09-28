$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$taskJdk = (Get-ChildItem .tools/jdk25 -Directory | Select-Object -First 1).FullName
$taskAsm = Join-Path $env:USERPROFILE '.m2/repository/org/ow2/asm/asm/9.9.1/asm-9.9.1.jar'
if (-not (Test-Path $taskAsm)) { throw 'ASM 9.9.1 is required.' }
$taskLibraries=(Get-ChildItem .tools/paper263/libraries -Recurse -Filter '*.jar' | ForEach-Object FullName) -join ';'
& "$taskJdk/bin/javac.exe" -cp ".tools/paper263/versions/26.3/paper-26.3.jar;$taskLibraries" -d .tools/compat-classes compat/BufferCompat.java
if ($LASTEXITCODE -ne 0) { throw 'Compatibility helper compiler failed.' }
& "$taskJdk/bin/javac.exe" -cp $taskAsm compat/PatchMythic.java
if ($LASTEXITCODE -ne 0) { throw 'Patch compiler failed.' }
& "$taskJdk/bin/java.exe" -cp "compat;$taskAsm" PatchMythic MythicMobs-5.13.0.jar release/MythicMobs-5.13.0-local263-r2.jar
if ($LASTEXITCODE -ne 0) { throw 'Patch failed.' }
Get-FileHash release/MythicMobs-5.13.0-local263-r2.jar -Algorithm SHA256
