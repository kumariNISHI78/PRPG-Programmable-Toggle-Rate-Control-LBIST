$cwd = (Get-Location).Path
$pptx = Join-Path $cwd 'VL405_LBIST_Project_Presentation.pptx'
$pdf = Join-Path $cwd 'VL405_LBIST_Project_Presentation.pdf'
$previewDir = Join-Path $cwd 'Slide_Previews'

if (-not (Test-Path $previewDir)) {
    New-Item -ItemType Directory -Path $previewDir | Out-Null
}

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($pptx, 0, 0, 0)

$pres.SaveAs($pdf, 32)
Write-Host "PDF successfully created: $pdf"

for ($i = 1; $i -le $pres.Slides.Count; $i++) {
    $outPng = Join-Path $previewDir ("slide_{0}.png" -f $i)
    $pres.Slides.Item($i).Export($outPng, "PNG", 1920, 1080)
    Write-Host "Exported slide $i to $outPng"
}

$pres.Close()
$ppt.Quit()
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()
Write-Host "PowerPoint export finished successfully."
