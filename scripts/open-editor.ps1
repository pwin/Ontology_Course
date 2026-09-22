<#
.SYNOPSIS
    Open the Turtle Editor Viewer with a lesson already loaded.

.DESCRIPTION
    The editor is used online, at https://semantechs.co.uk/turtle-editor-viewer/.
    It accepts ?dot=<url> for the file to load and &shapes=<url> for a shapes
    graph opened in a second tab. This script reads a lesson's LOAD IT line, or
    builds a link for any file under lessons/ or data/, and opens it.

.PARAMETER Lesson
    A lesson id such as o47, or the start of a file name.

.PARAMETER File
    A path under lessons/ or data/, when not taking it from a lesson.

.PARAMETER Shapes
    A path under lessons/, opened as a shapes tab.

.PARAMETER List
    Print every lesson with its link without opening anything.

.EXAMPLE
    ./scripts/open-editor.ps1 o47
    ./scripts/open-editor.ps1 -File data/01-vocabulary.ttl -Shapes 10-quality/style-shapes.ttl
    ./scripts/open-editor.ps1 -List
#>
param(
    [string]$Lesson,
    [string]$File,
    [string]$Shapes,
    [string]$Editor = "https://semantechs.co.uk/turtle-editor-viewer/",
    [string]$Repo = "https://raw.githubusercontent.com/pwin/Ontology_Course",
    [string]$Branch = "main",
    [switch]$List
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$lessonsDir = Join-Path $root "lessons"

function Raw([string]$relative) { return "$Repo/$Branch/$relative" }

function Link([string]$fileRelative, [string]$shapesRelative) {
    $url = $Editor + "?dot=" + [uri]::EscapeDataString((Raw $fileRelative))
    if ($shapesRelative) { $url += "&shapes=" + [uri]::EscapeDataString((Raw "lessons/$shapesRelative")) }
    return $url
}

function LessonInfo([System.IO.FileInfo]$f) {
    $text = Get-Content -Raw -LiteralPath $f.FullName
    $load = if ($text -match '(?m)^#  LOAD IT\s+(\S+)') { $Matches[1] } else { "" }
    $rel = $f.FullName.Substring($lessonsDir.Length + 1).Replace("\", "/")
    return @{ Id = $f.Name.Substring(0, 3); Title = ($f.BaseName.Substring(4) -replace "-", " "); Rel = $rel; Load = $load }
}

$lessons = Get-ChildItem -LiteralPath $lessonsDir -Recurse -Filter "o*.ttl" | Sort-Object Name | ForEach-Object { LessonInfo $_ }

if ($List) {
    foreach ($l in $lessons) { Write-Host ("{0}  {1}" -f $l.Id, $l.Title); Write-Host ("      " + $l.Load) }
    return
}

if ($Lesson) {
    $match = $lessons | Where-Object { $_.Id -eq $Lesson.ToLower() -or $_.Rel -like "*/$Lesson*" } | Select-Object -First 1
    if (-not $match) { throw "No lesson matches '$Lesson'. Try -List." }
    $url = if ($match.Load) { $match.Load } else { Link ("lessons/" + $match.Rel) $Shapes }
    Write-Host ("{0}  {1}" -f $match.Id, $match.Title)
} elseif ($File) {
    $url = Link $File.Replace("\", "/") $Shapes
} else {
    $first = $lessons | Select-Object -First 1
    $url = $first.Load
    Write-Host ("{0}  {1}   (the first lesson; try -List)" -f $first.Id, $first.Title)
}

Write-Host $url
Start-Process $url
