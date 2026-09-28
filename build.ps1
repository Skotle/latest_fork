$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$taskMaven = Join-Path $PSScriptRoot '.tools/apache-maven-3.9.11/bin/mvn.cmd'
$taskSource = 'source/mcMMO-c69f1fcc8072cc6ca032d366290b1161f9034a35/pom.xml'
if (-not (Test-Path -LiteralPath $taskMaven)) { throw 'Local Maven is missing; see README.ko.md.' }
if (-not (Test-Path -LiteralPath $taskSource)) { throw 'Pinned release source is missing; see README.ko.md.' }
New-Item -ItemType Directory -Force release | Out-Null
& $taskMaven -B -ntp -s build-settings.xml -f $taskSource '-Daether.connector.connectTimeout=10000' '-Daether.connector.requestTimeout=10000' clean verify *> release/build-release.log
if ($LASTEXITCODE -ne 0) { throw 'Build failed; see release/build-release.log.' }
python assemble.py
if ($LASTEXITCODE -ne 0) { throw 'Package validation failed.' }
Compress-Archive -Path release/extreme/* -DestinationPath release/extreme-plugins.zip -Force
Write-Output 'Created release/extreme-plugins.zip'
