$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $root '..')
$errors = @()

Get-ChildItem -Path . -Filter *.html | Sort-Object Name | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $matches = [regex]::Matches($content, '<link[^>]*href\s*=\s*"(.*?)"', 'IgnoreCase')
    $links = $matches | ForEach-Object { $_.Groups[1].Value }
    Write-Host "`n$($_.Name): found links -> $($links -join ', ')"

    if (-not ($links | Where-Object { $_ -like '*main.css' })) {
        $errors += "$($_.Name) missing link to css/main.css"
    }
    if ($_.Name -eq 'work.html') {
        if (-not ($links | Where-Object { $_ -like '*work.css' })) {
            $errors += 'work.html missing link to css/work.css'
        }
    }
    if ($_.Name -eq 'contact.html') {
        if (-not ($links | Where-Object { $_ -like '*contact.css' })) {
            $errors += 'contact.html missing link to css/contact.css'
        }
    }
}

Write-Host "`nChecking css folder and files..."
if (-not (Test-Path 'css')) {
    $errors += 'Missing css/ folder'
} else {
    foreach ($f in @('css/main.css','css/work.css','css/contact.css')) {
        if (-not (Test-Path $f)) { $errors += "Missing $f" }
    }
}

Write-Host "`nChecking img folder..."
if (-not (Test-Path 'img')) { $errors += 'Missing img/ folder' } else { Write-Host 'img/ folder exists' }

Write-Host "`nSummary:"
if ($errors.Count -gt 0) {
    Write-Host 'Issues found:'
    $errors | ForEach-Object { Write-Host '- ' $_ }
    Write-Host "`nResult: FAIL"
    exit 1
} else {
    Write-Host 'No issues found — all required files and links are present.'
    Write-Host "`nResult: PASS"
    exit 0
}
