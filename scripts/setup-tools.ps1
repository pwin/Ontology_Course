<#
.SYNOPSIS
    Fetch the third-party tools and ontologies the checker uses into lib/.

.DESCRIPTION
    Nothing in lib/ is redistributed in this repository; each item carries its
    own licence and is fetched from where its owner publishes it. The course can
    be done without any of them: the browser editor is the environment, and the
    measurements are already written into every lesson. This script is for
    re-running the checker, or measuring your own work.

      lib/owl/robot.jar           ROBOT (BSD-3-Clause): the OWL API, HermiT and the
                                  OWL 2 profile checker in one jar. About 82 MB. Needs Java 17+.
      lib/gist/gistCore.ttl       gist 14 (CC-BY-4.0, Semantic Arts)
      lib/gist/gistBFO.ttl        gistBFO (CC-BY-4.0, Semantic Arts)
      lib/gist/gistToGufoTypes.ttl, gistToGufoIndividuals.ttl   gistUFO (Semantic Arts)
      lib/gufo/gufo.ttl           gUFO (CC-BY-4.0, NEMO / UFES)
      lib/bfo/bfo-core.ttl        BFO 2020 core (CC-BY-4.0, BFO Consortium)

    The Python packages come from PyPI:  pip install -r scripts/requirements.txt

.EXAMPLE
    ./scripts/setup-tools.ps1
    ./scripts/setup-tools.ps1 -SkipRobot      # the ontologies only
#>
param(
    [switch]$SkipRobot,
    [string]$RobotUrl = "https://github.com/ontodev/robot/releases/latest/download/robot.jar"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$lib = Join-Path $root "lib"

function Fetch([string]$url, [string]$target) {
    $dir = Split-Path -Parent $target
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
    if (Test-Path $target) { Write-Host "  have   $target"; return }
    Write-Host "  fetch  $url"
    Invoke-WebRequest -Uri $url -OutFile $target -UseBasicParsing
    Write-Host "  wrote  $target"
}

Write-Host "Ontologies (CC-BY-4.0, each from its owner's repository)"
Fetch "https://raw.githubusercontent.com/semanticarts/gist/develop/ontologies/gistCore.ttl" (Join-Path $lib "gist/gistCore.ttl")
Fetch "https://raw.githubusercontent.com/semanticarts/gistBFO/develop/gistBFO.ttl" (Join-Path $lib "gist/gistBFO.ttl")
Fetch "https://raw.githubusercontent.com/semanticarts/gistUFO/develop/ontologies/gistToGufoTypes.ttl" (Join-Path $lib "gist/gistToGufoTypes.ttl")
Fetch "https://raw.githubusercontent.com/semanticarts/gistUFO/develop/ontologies/gistToGufoIndividuals.ttl" (Join-Path $lib "gist/gistToGufoIndividuals.ttl")
Fetch "https://raw.githubusercontent.com/semanticarts/gist/develop/validation/shapes/ontologyShapes.ttl" (Join-Path $lib "gist/ontologyShapes.ttl")
Fetch "http://purl.obolibrary.org/obo/bfo/2020/bfo-core.ttl" (Join-Path $lib "bfo/bfo-core.ttl")

$gufo = Join-Path $lib "gufo/gufo.ttl"
if (-not (Test-Path $gufo)) {
    New-Item -ItemType Directory -Path (Split-Path -Parent $gufo) -Force | Out-Null
    Write-Host "  fetch  http://purl.org/nemo/gufo  (as Turtle)"
    Invoke-WebRequest -Uri "http://purl.org/nemo/gufo" -Headers @{ Accept = "text/turtle" } -OutFile $gufo -UseBasicParsing
    Write-Host "  wrote  $gufo"
} else { Write-Host "  have   $gufo" }

if (-not $SkipRobot) {
    Write-Host "ROBOT (BSD-3-Clause; needs Java 17 or newer, https://adoptium.net)"
    Fetch $RobotUrl (Join-Path $lib "owl/robot.jar")
    try { & java -version 2>&1 | Select-Object -First 1 | ForEach-Object { Write-Host "  java   $_" } }
    catch { Write-Warning "Java was not found on PATH; ROBOT needs it." }
}

Write-Host ""
Write-Host "Then:  pip install -r scripts/requirements.txt"
Write-Host "       python scripts/check_lessons.py"
