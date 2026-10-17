# Word COM: ebook_word.html -> PDF（A4 版面）
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$src = "d:\00000___Coding\113--CapoVime\续命指南\awesome-programmer-longevity\ebook_word.html"
$dst = "d:\00000___Coding\113--CapoVime\续命指南\awesome-programmer-longevity\ebook_v1.pdf"
try {
  $doc = $word.Documents.Open($src)
  $doc.PageSetup.PaperSize = 7      # wdPaperA4
  $doc.PageSetup.TopMargin = 40
  $doc.PageSetup.BottomMargin = 40
  $doc.PageSetup.LeftMargin = 42
  $doc.PageSetup.RightMargin = 42
  $doc.SaveAs2($dst, 17)  # wdFormatPDF
  $pages = $doc.ComputeStatistics(2)  # wdStatisticPages
  Write-Output "PDF saved, pages=$pages"
  $doc.Close($false)
} finally {
  $word.Quit()
  [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
