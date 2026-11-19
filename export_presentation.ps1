$cwd = (Get-Location).Path
$pptx1 = Join-Path $cwd 'VL405_LBIST_Project_Presentation.pptx'
$pdf1 = Join-Path $cwd 'VL405_LBIST_Project_Presentation.pdf'

$pptx2 = Join-Path $cwd 'VL405_LBIST_Final_Results_Slide.pptx'
$pdf2 = Join-Path $cwd 'VL405_LBIST_Final_Results_Slide.pdf'

$previewDir = Join-Path $cwd 'Slide_Previews'

if (-not (Test-Path $previewDir)) {
    New-Item -ItemType Directory -Path $previewDir | Out-Null
}

$ppt = New-Object -ComObject PowerPoint.Application

# 1. Export 3-slide deck
$pres1 = $ppt.Presentations.Open($pptx1, 0, 0, 0)
$pres1.SaveAs($pdf1, 32)
Write-Host "PDF 1 created: $pdf1"
for ($i = 1; $i -le $pres1.Slides.Count; $i++) {
    $outPng = Join-Path $previewDir ("slide_{0}.png" -f $i)
    $pres1.Slides.Item($i).Export($outPng, "PNG", 1920, 1080)
    Write-Host "Exported slide $i to $outPng"
}
$pres1.Close()

# 2. Export standalone results slide
$pres2 = $ppt.Presentations.Open($pptx2, 0, 0, 0)
$pres2.SaveAs($pdf2, 32)
Write-Host "PDF 2 created: $pdf2"
$outPngRes = Join-Path $previewDir "final_results_slide.png"
$pres2.Slides.Item(1).Export($outPngRes, "PNG", 1920, 1080)
Write-Host "Exported standalone slide to $outPngRes"
$pres2.Close()

$ppt.Quit()
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()
Write-Host "PowerPoint export finished successfully for all presentations."
