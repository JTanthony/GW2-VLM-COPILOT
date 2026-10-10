param([switch]$Preview)
$ErrorActionPreference = 'Stop'
$installRoot = (Resolve-Path -LiteralPath $PSScriptRoot).Path
$manifestPath = Join-Path $installRoot 'PACKAGE-MANIFEST.json'
if (-not (Test-Path -LiteralPath (Join-Path $installRoot 'GW2-VLM-COPILOT.exe'))) { throw 'This is not a packaged copilot folder.' }
$entries = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$targets = @()
foreach ($entry in $entries) {
    $relative = [string]$entry.path
    if ([IO.Path]::IsPathRooted($relative) -or $relative -match '(^|[\\/])\.\.([\\/]|$)') { throw 'Unsafe package manifest path.' }
    $target = [IO.Path]::GetFullPath((Join-Path $installRoot $relative))
    if (-not $target.StartsWith($installRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Package path leaves installation folder.' }
    $ancestor = $target
    while ($ancestor -and $ancestor.Length -ge $installRoot.Length) {
        if ((Test-Path -LiteralPath $ancestor) -and ((Get-Item -LiteralPath $ancestor -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Uninstall does not follow links or junctions.' }
        $ancestor = Split-Path -Parent $ancestor
    }
    if ((Test-Path -LiteralPath $target) -and -not (Test-Path -LiteralPath $target -PathType Leaf)) { throw 'Manifest entry is not a file.' }
    $targets += $target
}
if ($Preview) { Write-Output "Validated $($targets.Count) package file paths. No files changed."; exit }
$running = Get-Process -Name 'GW2-VLM-COPILOT' -ErrorAction SilentlyContinue
if ($running) { throw 'Close GW2 VLM COPILOT and let its engine stop, then run Uninstall again.' }
Write-Host 'This removes packaged app files only. Models, engine downloads and saved user data are kept.'
Write-Host "Folder: $installRoot"
if ((Read-Host 'Type UNINSTALL to continue') -cne 'UNINSTALL') { Write-Host 'Cancelled.'; exit }
# Every target was validated against this installation before any deletion.
foreach ($target in $targets) { if (Test-Path -LiteralPath $target -PathType Leaf) { Remove-Item -LiteralPath $target -Force } }
if (Test-Path -LiteralPath $manifestPath) { Remove-Item -LiteralPath $manifestPath -Force }
Write-Host 'App files removed. Downloaded models and engines are preserved. Empty folders can be removed in Explorer.'
Write-Host 'Saved data is kept in %LOCALAPPDATA%\GW2 VLM COPILOT; protected tokens remain in %LOCALAPPDATA%\Waypoint\credentials.'
Write-Host 'To remove saved data or tokens, use Explorer to delete those locations only if you no longer need them. The token location may be shared with development copies.'
